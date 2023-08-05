# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import numpy as np
from warnings import warn
from ..utilities import cross_product
from ._base_grf import BaseGRF
from ..utilities import check_inputs
from sklearn.base import BaseEstimator, clone
from sklearn.utils import check_X_y
from ..tree._tree import DTYPE, DOUBLE

from .._ensemble import (BaseEnsemble, _partition_estimators, _get_n_samples_subsample,
                         _accumulate_prediction, _accumulate_prediction_var, _accumulate_prediction_and_var,
                         _accumulate_oob_preds)
from ..utilities import check_inputs, cross_product
from ._base_grftree import GRFTree
from joblib import Parallel, delayed
from scipy.sparse import hstack as sparse_hstack
from sklearn.utils import check_random_state, compute_sample_weight
from sklearn.utils.validation import _check_sample_weight, check_is_fitted


__all__ = ["MultiOutputGRF",
           "CausalForest",
           "CausalIVForest",
           "RegressionForest",
           "BeatForest"
           ]
MAX_INT = np.iinfo(np.int32).max

import numbers
# =============================================================================
# A MultOutputWrapper for GRF classes
# =============================================================================


class MultiOutputGRF(BaseEstimator):
    """ Simple wrapper estimator that enables multiple outcome labels for all the
    grf estimators that only accept a single outcome. Similar to MultiOutputRegressor.
    """

    def __init__(self, estimator):
        self.estimator = estimator

    def fit(self, X, T, y, *, sample_weight=None, **kwargs):
        y, T, X, _ = check_inputs(y, T, X, W=None, multi_output_T=True, multi_output_Y=True)
        y = np.atleast_1d(y)
        if y.ndim == 1:
            y = np.reshape(y, (-1, 1))
        self.estimators_ = [clone(self.estimator) for _ in range(y.shape[1])]
        [estimator.fit(X, T, y[:, [it]], sample_weight=sample_weight, **kwargs)
         for it, estimator in enumerate(self.estimators_)]
        return self

    def predict(self, X, interval=False, alpha=0.05):
        if interval:
            pred, lb, ub = zip(*[estimator.predict(X, interval=interval, alpha=alpha)
                                 for estimator in self.estimators_])
            return np.moveaxis(np.array(pred), 0, 1), np.moveaxis(np.array(lb), 0, 1), np.moveaxis(np.array(ub), 0, 1)
        else:
            pred = [estimator.predict(X, interval=interval, alpha=alpha) for estimator in self.estimators_]
            return np.moveaxis(np.array(pred), 0, 1)

    def predict_and_var(self, X):
        pred, var = zip(*[estimator.predict_and_var(X) for estimator in self.estimators_])
        return np.moveaxis(np.array(pred), 0, 1), np.moveaxis(np.array(var), 0, 1)

    def predict_projection_and_var(self, X, projector):
        pred, var = zip(*[estimator.predict_projection_and_var(X, projector) for estimator in self.estimators_])
        return np.moveaxis(np.array(pred), 0, 1), np.moveaxis(np.array(var), 0, 1)

    def oob_predict(self, Xtrain):
        pred = [estimator.oob_predict(Xtrain) for estimator in self.estimators_]
        return np.moveaxis(np.array(pred), 0, 1)

    def feature_importances(self, max_depth=4, depth_decay_exponent=2.0):
        res = [estimator.feature_importances(max_depth=max_depth, depth_decay_exponent=depth_decay_exponent)
               for estimator in self.estimators_]
        return np.array(res)

    @property
    def feature_importances_(self):
        return self.feature_importances()

    def __len__(self):
        """Return the number of estimators in the ensemble for each target y."""
        return len(self.estimators_[0].estimators_)

    def __getitem__(self, index):
        """Return a list of the index'th estimator in the ensemble for each target y."""
        return [forest[index] for forest in self.estimators_]

    def __iter__(self):
        """Return iterator over tuples of estimators for each target y in the ensemble."""
        return iter(zip(*self.estimators_))

# =============================================================================
# Instantiations of Generalized Random Forest
# =============================================================================


class CausalForest(BaseGRF):
    """
    A Causal Forest [cf1]_. It fits a forest that solves the local moment equation problem:

    .. code-block::

        E[ (Y - <theta(x), T> - beta(x)) (T;1) | X=x] = 0

    Each node in the tree contains a local estimate of the parameter theta(x), for every region of X that
    falls within that leaf.

    Parameters
    ----------
    n_estimators : int, default=100
        Number of trees

    criterion : {``"mse"``, ``"het"``}, default="mse"
        The function to measure the quality of a split. Supported criteria
        are "mse" for the mean squared error in a linear moment estimation tree and "het" for
        heterogeneity score.

        - The "mse" criterion finds splits that minimize the score:

          .. code-block::

            sum_{child} E[(Y - <theta(child), T> - beta(child))^2 | X=child] weight(child)

          Internally, for the case of more than two treatments or for the case of two treatments with
          ``fit_intercept=True`` then this criterion is approximated by computationally simpler variants for
          computational purposes. In particular, it is replaced by::

              sum_{child} weight(child) * rho(child).T @ E[(T;1) @ (T;1).T | X in child] @ rho(child)

          where:

          .. code-block::

            rho(child) := E[(T;1) @ (T;1).T | X in parent]^{-1}
                                    * E[(Y - <theta(x), T> - beta(x)) (T;1) | X in child]

          This can be thought as a heterogeneity inducing score, but putting more weight on scores
          with a large minimum eigenvalue of the child jacobian ``E[(T;1) @ (T;1).T | X in child]``,
          which leads to smaller variance of the estimate and stronger identification of the parameters.

        - The "het" criterion finds splits that maximize the pure parameter heterogeneity score:

          .. code-block::

            sum_{child} weight(child) * rho(child)[:n_T].T @ rho(child)[:n_T]

          This can be thought as an approximation to the ideal heterogeneity score:

          .. code-block::

              weight(left) * weight(right) || theta(left) - theta(right)||_2^2 / weight(parent)^2

          as outlined in [cf1]_

    max_depth : int, default=None
        The maximum depth of the tree. If None, then nodes are expanded until
        all leaves are pure or until all leaves contain less than
        min_samples_split samples.

    min_samples_split : int or float, default=10
        The minimum number of samples required to split an internal node:

        - If int, then consider `min_samples_split` as the minimum number.
        - If float, then `min_samples_split` is a fraction and
          `ceil(min_samples_split * n_samples)` are the minimum
          number of samples for each split.

    min_samples_leaf : int or float, default=5
        The minimum number of samples required to be at a leaf node.
        A split point at any depth will only be considered if it leaves at
        least ``min_samples_leaf`` training samples in each of the left and
        right branches.  This may have the effect of smoothing the model,
        especially in regression.

        - If int, then consider `min_samples_leaf` as the minimum number.
        - If float, then `min_samples_leaf` is a fraction and
          `ceil(min_samples_leaf * n_samples)` are the minimum
          number of samples for each node.

    min_weight_fraction_leaf : float, default=0.0
        The minimum weighted fraction of the sum total of weights (of all
        the input samples) required to be at a leaf node. Samples have
        equal weight when sample_weight is not provided.

    min_var_fraction_leaf : None or float in (0, 1], default=None
        A constraint on some proxy of the variation of the treatment vector that should be contained within each
        leaf as a percentage of the total variance of the treatment vector on the whole sample. This avoids
        performing splits where either the variance of the treatment is small and hence the local parameter
        is not well identified and has high variance. The proxy of variance is different for different criterion,
        primarily for computational efficiency reasons.

        - If ``criterion='het'``, then this constraint translates to:

          .. code-block::

            for all i in {1, ..., T.shape[1]}:
                E[T[i]^2 | X in leaf] > `min_var_fraction_leaf` * E[T[i]^2]

          When ``T`` is the residual treatment (i.e. centered), this translates to a requirement that

          .. code-block::

            for all i in {1, ..., T.shape[1]}:
                Var(T[i] | X in leaf) > `min_var_fraction_leaf` * Var(T[i])

        - If ``criterion='mse'``, because the criterion stores more information about the leaf for
          every candidate split, then this constraint imposes further constraints on the pairwise correlations
          of different coordinates of each treatment, i.e.:

          .. code-block::

            for all i neq j:
              sqrt(Var(T[i]|X in leaf) * Var(T[j]|X in leaf) * (1 - rho(T[i], T[j]| in leaf)^2))
                  > `min_var_fraction_leaf` sqrt(Var(T[i]) * Var(T[j]) * (1 - rho(T[i], T[j])^2))

          where rho(X, Y) is the Pearson correlation coefficient of two random variables X, Y. Thus this
          constraint also enforces that no two pairs of treatments be very co-linear within a leaf. This
          extra constraint primarily has bite in the case of more than two input treatments and also avoids
          leafs where the parameter estimate has large variance due to local co-linearities of the treatments.

    min_var_leaf_on_val : bool, default=False
        Whether the `min_var_fraction_leaf` constraint should also be enforced to hold on the validation set of the
        honest split too. If `min_var_leaf=None` then this flag does nothing. Setting this to True should
        be done with caution, as this partially violates the honesty structure, since the treatment variable
        of the validation set is used to inform the split structure of the tree. However, this is a benign
        dependence as it only uses local correlation structure of the treatment T to decide whether
        a split is feasible.

    max_features : int, float or {"auto", "sqrt", "log2"}, default=None
        The number of features to consider when looking for the best split:

        - If int, then consider `max_features` features at each split.
        - If float, then `max_features` is a fraction and
          `int(max_features * n_features)` features are considered at each
          split.
        - If "auto", then `max_features=n_features`.
        - If "sqrt", then `max_features=sqrt(n_features)`.
        - If "log2", then `max_features=log2(n_features)`.
        - If None, then `max_features=n_features`.

        Note: the search for a split does not stop until at least one
        valid partition of the node samples is found, even if it requires to
        effectively inspect more than ``max_features`` features.

    min_impurity_decrease : float, default=0.0
        A node will be split if this split induces a decrease of the impurity
        greater than or equal to this value.
        The weighted impurity decrease equation is the following::

            N_t / N * (impurity - N_t_R / N_t * right_impurity
                                - N_t_L / N_t * left_impurity)

        where ``N`` is the total number of samples, ``N_t`` is the number of
        samples at the current node, ``N_t_L`` is the number of samples in the
        left child, and ``N_t_R`` is the number of samples in the right child.
        ``N``, ``N_t``, ``N_t_R`` and ``N_t_L`` all refer to the weighted sum,
        if ``sample_weight`` is passed.

    max_samples : int or float in (0, 1], default=.45,
        The number of samples to use for each subsample that is used to train each tree:

        - If int, then train each tree on `max_samples` samples, sampled without replacement from all the samples
        - If float, then train each tree on ceil(`max_samples` * `n_samples`), sampled without replacement
          from all the samples.

        If ``inference=True``, then `max_samples` must either be an integer smaller than `n_samples//2` or a float
        less than or equal to .5.

    min_balancedness_tol: float in [0, .5], default=.45
        How imbalanced a split we can tolerate. This enforces that each split leaves at least
        (.5 - min_balancedness_tol) fraction of samples on each side of the split; or fraction
        of the total weight of samples, when sample_weight is not None. Default value, ensures
        that at least 5% of the parent node weight falls in each side of the split. Set it to 0.0 for no
        balancedness and to .5 for perfectly balanced splits. For the formal inference theory
        to be valid, this has to be any positive constant bounded away from zero.

    honest : bool, default=True
        Whether each tree should be trained in an honest manner, i.e. the training set is split into two equal
        sized subsets, the train and the val set. All samples in train are used to create the split structure
        and all samples in val are used to calculate the value of each node in the tree.

    inference : bool, default=True
        Whether inference (i.e. confidence interval construction and uncertainty quantification of the estimates)
        should be enabled. If `inference=True`, then the estimator uses a bootstrap-of-little-bags approach
        to calculate the covariance of the parameter vector, with am objective Bayesian debiasing correction
        to ensure that variance quantities are positive.

    fit_intercept : bool, default=True
        Whether we should fit an intercept nuisance parameter beta(x). If `fit_intercept=False`, then no (;1) is
        appended to the treatment variable in all calculations in this docstring. If `fit_intercept=True`, then
        the constant treatment of `(;1)` is appended to each treatment vector and the coefficient in front
        of this constant treatment is the intercept beta(x). beta(x) is treated as a nuisance and not returned
        by the predict(X), predict_and_var(X) or the predict_var(X) methods.
        Use predict_full(X) to recover the intercept term too.

    subforest_size : int, default=4,
        The number of trees in each sub-forest that is used in the bootstrap-of-little-bags calculation.
        The parameter `n_estimators` must be divisible by `subforest_size`. Should typically be a small constant.

    n_jobs : int or None, default=-1
        The number of parallel jobs to be used for parallelism; follows joblib semantics.
        ``n_jobs=-1`` means all available cpu cores. ``n_jobs=None`` means no parallelism.

    random_state : int, RandomState instance or None, default=None
        Controls the randomness of the estimator. The features are always
        randomly permuted at each split. When ``max_features < n_features``, the algorithm will
        select ``max_features`` at random at each split before finding the best
        split among them. But the best found split may vary across different
        runs, even if ``max_features=n_features``. That is the case, if the
        improvement of the criterion is identical for several splits and one
        split has to be selected at random. To obtain a deterministic behaviour
        during fitting, ``random_state`` has to be fixed to an integer.

    verbose : int, default=0
        Controls the verbosity when fitting and predicting.

    warm_start : bool, default=``False``
        When set to ``True``, reuse the solution of the previous call to fit
        and add more estimators to the ensemble, otherwise, just fit a whole
        new forest. If ``True``, then `oob_predict` method for out-of-bag predictions is not available.

    Attributes
    ----------
    feature_importances_ : ndarray of shape (n_features,)
        The feature importances based on the amount of parameter heterogeneity they create.
        The higher, the more important the feature.
        The importance of a feature is computed as the (normalized) total heterogeneity that the feature
        creates. Each split that the feature was chosen adds::

            parent_weight * (left_weight * right_weight)
                * mean((value_left[k] - value_right[k])**2) / parent_weight**2

        to the importance of the feature. Each such quantity is also weighted by the depth of the split.
        By default splits below ``max_depth=4`` are not used in this calculation and also each split
        at depth `depth`, is re-weighted by ``1 / (1 + `depth`)**2.0``. See the method ``feature_importances``
        for a method that allows one to change these defaults.

    estimators_ : list of objects of type :class:`~econml.grf.GRFTree`
        The fitted trees.

    References
    ----------
    .. [cf1] Athey, Susan, Julie Tibshirani, and Stefan Wager. "Generalized random forests."
        The Annals of Statistics 47.2 (2019): 1148-1178
        https://arxiv.org/pdf/1610.01271.pdf

    """

    def __init__(self,
                 n_estimators=100, *,
                 criterion="mse",
                 max_depth=None,
                 min_samples_split=10,
                 min_samples_leaf=5,
                 min_weight_fraction_leaf=0.,
                 min_var_fraction_leaf=None,
                 min_var_leaf_on_val=False,
                 max_features="auto",
                 min_impurity_decrease=0.,
                 max_samples=.45,
                 min_balancedness_tol=.45,
                 honest=True,
                 inference=True,
                 fit_intercept=True,
                 subforest_size=4,
                 n_jobs=-1,
                 random_state=None,
                 verbose=0,
                 warm_start=False):
        super().__init__(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth,
                         min_samples_split=min_samples_split,
                         min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf,
                         min_var_fraction_leaf=min_var_fraction_leaf, min_var_leaf_on_val=min_var_leaf_on_val,
                         max_features=max_features, min_impurity_decrease=min_impurity_decrease,
                         max_samples=max_samples, min_balancedness_tol=min_balancedness_tol,
                         honest=honest, inference=inference, fit_intercept=fit_intercept,
                         subforest_size=subforest_size, n_jobs=n_jobs, random_state=random_state, verbose=verbose,
                         warm_start=warm_start)

    def fit(self, X, T, y, *, sample_weight=None):
        """
        Build a causal forest of trees from the training set (X, T, y).

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples. Internally, its dtype will be converted
            to ``dtype=np.float64``.
        T : array-like of shape (n_samples, n_treatments)
            The treatment vector for each sample
        y : array-like of shape (n_samples,) or (n_samples, n_outcomes)
            The outcome values for each sample.
        sample_weight : array-like of shape (n_samples,), default=None
            Sample weights. If None, then samples are equally weighted. Splits
            that would create child nodes with net zero or negative weight are
            ignored while searching for a split in each node.

        Returns
        -------
        self : object
        """
        return super().fit(X, T, y, sample_weight=sample_weight)

    def _get_alpha_and_pointJ(self, X, T, y):
        # Append a constant treatment if `fit_intercept=True`, the coefficient
        # in front of the constant treatment is the intercept in the moment equation.
        if self.fit_intercept:
            T = np.hstack([T, np.ones((T.shape[0], 1))])
        return y * T, cross_product(T, T)

    def _get_n_outputs_decomposition(self, X, T, y):
        n_relevant_outputs = T.shape[1]
        n_outputs = n_relevant_outputs
        if self.fit_intercept:
            n_outputs = n_relevant_outputs + 1
        return n_outputs, n_relevant_outputs


class CausalIVForest(BaseGRF):
    """A Causal IV Forest [cfiv1]_. It fits a forest that solves the local moment equation problem:

    .. code-block

        E[ (Y - <theta(x), T> - beta(x)) (Z;1) | X=x] = 0

    Each node in the tree contains a local estimate of the parameter theta(x), for every region of X that
    falls within that leaf.

    Parameters
    ----------
    n_estimators : int, default=100
        Number of trees

    criterion : {``"mse"``, ``"het"``}, default="mse"
        The function to measure the quality of a split. Supported criteria
        are "mse" for the mean squared error in a linear moment estimation tree and "het" for
        heterogeneity score.

        - The "mse" criterion finds splits that approximately minimize the score:

          .. code-block::

            sum_{child} E[(Y - <theta(child), E[T|Z]> - beta(child))^2 | X=child] weight(child)

          Though we note that the local estimate is still estimated by solving the local moment equation for samples
          that fall within the node and not by minimizing this loss. Internally, for the case of more than two
          treatments or for the case of one treatment with `fit_intercept=True` then this criterion is approximated
          by computationally simpler variants for computationaly purposes. In particular, it is replaced by:

          .. code-block::

              sum_{child} weight(child) * rho(child).T @ E[(T;1) @ (Z;1).T | X in child] @ rho(child)

          where:

          .. code-block::

              rho(child) := E[(T;1) @ (Z;1).T | X in parent]^{-1}
                                * E[(Y - <theta(x), T> - beta(x)) (Z;1) | X in child]

          This can be thought as a heterogeneity inducing score, but putting more weight on scores
          with a large minimum eigenvalue of the child jacobian E[(T;1) @ (Z;1).T | X in child], which leads to smaller
          variance of the estimate and stronger identification of the parameters.

        - The ``"het"`` criterion finds splits that maximize the pure parameter heterogeneity score:

          .. code-block::

            sum_{child} weight(child) * rho(child)[:n_T].T @ rho(child)[:n_T]

          This can be thought as an approximation to the ideal heterogeneity score:

          .. code-block::

              weight(left) * weight(right) || theta(left) - theta(right)||_2^2 / weight(parent)^2

          as outlined in [cfiv1]_

    max_depth : int, default=None
        The maximum depth of the tree. If None, then nodes are expanded until
        all leaves are pure or until all leaves contain less than
        min_samples_split samples.

    min_samples_split : int or float, default=10
        The minimum number of samples required to split an internal node:

        - If int, then consider `min_samples_split` as the minimum number.
        - If float, then `min_samples_split` is a fraction and
          `ceil(min_samples_split * n_samples)` are the minimum
          number of samples for each split.

    min_samples_leaf : int or float, default=5
        The minimum number of samples required to be at a leaf node.
        A split point at any depth will only be considered if it leaves at
        least ``min_samples_leaf`` training samples in each of the left and
        right branches.  This may have the effect of smoothing the model,
        especially in regression.

        - If int, then consider `min_samples_leaf` as the minimum number.
        - If float, then `min_samples_leaf` is a fraction and
          `ceil(min_samples_leaf * n_samples)` are the minimum
          number of samples for each node.

    min_weight_fraction_leaf : float, default=0.0
        The minimum weighted fraction of the sum total of weights (of all
        the input samples) required to be at a leaf node. Samples have
        equal weight when sample_weight is not provided.

    min_var_fraction_leaf : None or float in (0, 1], default=None
        A constraint on some proxy of the variation of the covariance of the treatment vector with the instrument
        vector that should be contained within each leaf as a percentage of the total cov-variance of the treatment
        and instrument on the whole sample. This avoids performing splits where either the variance of the treatment
        is small or the variance of the instrument is small or the strength of the instrument on the treatment is
        locally weak and hence the local parameter is not well identified and has high variance.
        The proxy of variance is different for different criterion, primarily for computational efficiency reasons.

        - If ``criterion='het'``, then this constraint translates to:

          .. code-block::

            for all i in {1, ..., T.shape[1]}:
                E[T[i] Z[i] | X in leaf] > `min_var_fraction_leaf` * E[T[i] Z[i]]

          When `T` is the residual treatment and `Z` the residual instrument (i.e. centered),
          this translates to a requirement that:

          .. code-block::

            for all i in {1, ..., T.shape[1]}:
                Cov(T[i], Z[i] | X in leaf) > `min_var_fraction_leaf` * Cov(T[i], Z[i])

        - If ``criterion='mse'``, because the criterion stores more information about the leaf for
          every candidate split, then this constraint imposes further constraints on the pairwise correlations
          of different coordinates of each treatment. For instance, when the instrument and treatment are both
          residualized (centered) then this constraint translates to:

          .. code-block::

            for all i neq j:
                E[T[i]Z[i]] E[T[j]Z[j]] - E[T[i] Z[j]]
                sqrt(Cov(T[i], Z[i] |X in leaf) * Cov(T[j], Z[j]|X in leaf)
                        * (1 - rho(T[i], Z[j]|X in leaf) * rho(T[j], Z[i]|X in leaf)))
                  > `min_var_fraction_leaf` * sqrt(Cov(T[i], Z[i]) * Cov(T[j], Z[j])
                                                    * (1 - rho(T[i], Z[j]) * rho(T[j], Z[i])))

          where rho(X, Y) is the Pearson correlation coefficient of two random variables X, Y. Thus this
          constraint also enforces that no two pairs of treatments and instruments be very co-linear within a leaf.
          This extra constraint primarily has bite in the case of more than two input treatments and also avoids
          leafs where the parameter estimate has large variance due to local co-linearities of the treatments.

    min_var_leaf_on_val : bool, default=False
        Whether the `min_var_fraction_leaf` constraint should also be enforced to hold on the validation set of the
        honest split too. If `min_var_leaf=None` then this flag does nothing. Setting this to True should
        be done with caution, as this partially violates the honesty structure, since parts of the variables
        other than the X variable (e.g. the variables that go into the jacobian J of the linear model) are
        used to inform the split structure of the tree. However, this is a benign dependence as it only uses
        the treatment T its local correlation structure to decide whether a split is feasible.

    max_features : int, float or {"auto", "sqrt", "log2"}, default=None
        The number of features to consider when looking for the best split:

        - If int, then consider `max_features` features at each split.
        - If float, then `max_features` is a fraction and
          `int(max_features * n_features)` features are considered at each
          split.
        - If "auto", then `max_features=n_features`.
        - If "sqrt", then `max_features=sqrt(n_features)`.
        - If "log2", then `max_features=log2(n_features)`.
        - If None, then `max_features=n_features`.

        Note: the search for a split does not stop until at least one
        valid partition of the node samples is found, even if it requires to
        effectively inspect more than ``max_features`` features.

    min_impurity_decrease : float, default=0.0
        A node will be split if this split induces a decrease of the impurity
        greater than or equal to this value.
        The weighted impurity decrease equation is the following::

            N_t / N * (impurity - N_t_R / N_t * right_impurity
                                - N_t_L / N_t * left_impurity)

        where ``N`` is the total number of samples, ``N_t`` is the number of
        samples at the current node, ``N_t_L`` is the number of samples in the
        left child, and ``N_t_R`` is the number of samples in the right child.
        ``N``, ``N_t``, ``N_t_R`` and ``N_t_L`` all refer to the weighted sum,
        if ``sample_weight`` is passed.

    max_samples : int or float in (0, 1], default=.45,
        The number of samples to use for each subsample that is used to train each tree:

        - If int, then train each tree on `max_samples` samples, sampled without replacement from all the samples
        - If float, then train each tree on ceil(`max_samples` * `n_samples`), sampled without replacement
          from all the samples.

        If ``inference=True``, then `max_samples` must either be an integer smaller than `n_samples//2` or a float
        less than or equal to .5.

    min_balancedness_tol: float in [0, .5], default=.45
        How imbalanced a split we can tolerate. This enforces that each split leaves at least
        (.5 - min_balancedness_tol) fraction of samples on each side of the split; or fraction
        of the total weight of samples, when sample_weight is not None. Default value, ensures
        that at least 5% of the parent node weight falls in each side of the split. Set it to 0.0 for no
        balancedness and to .5 for perfectly balanced splits. For the formal inference theory
        to be valid, this has to be any positive constant bounded away from zero.

    honest : bool, default=True
        Whether each tree should be trained in an honest manner, i.e. the training set is split into two equal
        sized subsets, the train and the val set. All samples in train are used to create the split structure
        and all samples in val are used to calculate the value of each node in the tree.

    inference : bool, default=True
        Whether inference (i.e. confidence interval construction and uncertainty quantification of the estimates)
        should be enabled. If ``inference=True``, then the estimator uses a bootstrap-of-little-bags approach
        to calculate the covariance of the parameter vector, with am objective Bayesian debiasing correction
        to ensure that variance quantities are positive.

    fit_intercept : bool, default=True
        Whether we should fit an intercept nuisance parameter beta(x). If `fit_intercept=False`, then no (;1) is
        appended to the treatment variable in all calculations in this docstring. If `fit_intercept=True`, then
        the constant treatment of `(;1)` is appended to each treatment vector and the coefficient in front
        of this constant treatment is the intercept beta(x). beta(x) is treated as a nuisance and not returned
        by the predict(X), predict_and_var(X) or the predict_var(X) methods.
        Use predict_full(X) to recover the intercept term too.

    subforest_size : int, default=4,
        The number of trees in each sub-forest that is used in the bootstrap-of-little-bags calculation.
        The parameter `n_estimators` must be divisible by `subforest_size`. Should typically be a small constant.

    n_jobs : int or None, default=-1
        The number of parallel jobs to be used for parallelism; follows joblib semantics.
        `n_jobs=-1` means all available cpu cores. `n_jobs=None` means no parallelism.

    random_state : int, RandomState instance or None, default=None
        Controls the randomness of the estimator. The features are always
        randomly permuted at each split. When ``max_features < n_features``, the algorithm will
        select ``max_features`` at random at each split before finding the best
        split among them. But the best found split may vary across different
        runs, even if ``max_features=n_features``. That is the case, if the
        improvement of the criterion is identical for several splits and one
        split has to be selected at random. To obtain a deterministic behaviour
        during fitting, ``random_state`` has to be fixed to an integer.

    verbose : int, default=0
        Controls the verbosity when fitting and predicting.

    warm_start : bool, default=False
        When set to ``True``, reuse the solution of the previous call to fit
        and add more estimators to the ensemble, otherwise, just fit a whole
        new forest. If ``True``, then `oob_predict` method for out-of-bag predictions is not available.

    Attributes
    ----------
    feature_importances_ : ndarray of shape (n_features,)
        The feature importances based on the amount of parameter heterogeneity they create.
        The higher, the more important the feature.
        The importance of a feature is computed as the (normalized) total heterogeneity that the feature
        creates. Each split that the feature was chosen adds::

            parent_weight * (left_weight * right_weight)
                * mean((value_left[k] - value_right[k])**2) / parent_weight**2

        to the importance of the feature. Each such quantity is also weighted by the depth of the split.
        By default splits below `max_depth=4` are not used in this calculation and also each split
        at depth `depth`, is re-weighted by ``1 / (1 + `depth`)**2.0``. See the method ``feature_importances``
        for a method that allows one to change these defaults.

    estimators_ : list of objects of type :class:`~econml.grf.GRFTree`
        The fitted trees.

    References
    ----------
    .. [cfiv1] Athey, Susan, Julie Tibshirani, and Stefan Wager. "Generalized random forests."
        The Annals of Statistics 47.2 (2019): 1148-1178
        https://arxiv.org/pdf/1610.01271.pdf

    """

    def __init__(self,
                 n_estimators=100, *,
                 criterion="mse",
                 max_depth=None,
                 min_samples_split=10,
                 min_samples_leaf=5,
                 min_weight_fraction_leaf=0.,
                 min_var_fraction_leaf=None,
                 min_var_leaf_on_val=False,
                 max_features="auto",
                 min_impurity_decrease=0.,
                 max_samples=.45,
                 min_balancedness_tol=.45,
                 honest=True,
                 inference=True,
                 fit_intercept=True,
                 subforest_size=4,
                 n_jobs=-1,
                 random_state=None,
                 verbose=0,
                 warm_start=False):
        super().__init__(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth,
                         min_samples_split=min_samples_split,
                         min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf,
                         min_var_fraction_leaf=min_var_fraction_leaf, min_var_leaf_on_val=min_var_leaf_on_val,
                         max_features=max_features, min_impurity_decrease=min_impurity_decrease,
                         max_samples=max_samples, min_balancedness_tol=min_balancedness_tol,
                         honest=honest, inference=inference, fit_intercept=fit_intercept,
                         subforest_size=subforest_size, n_jobs=n_jobs, random_state=random_state, verbose=verbose,
                         warm_start=warm_start)

    def fit(self, X, T, y, *, Z, sample_weight=None):
        """
        Build an IV forest of trees from the training set (X, T, y, Z).

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples. Internally, its dtype will be converted
            to ``dtype=np.float64``.
        T : array-like of shape (n_samples, n_treatments)
            The treatment vector for each sample
        y : array-like of shape (n_samples,) or (n_samples, n_outcomes)
            The outcome values for each sample.
        Z : array-like of shape (n_samples, n_treatments)
            The instrument vector. This method requires an equal amount of instruments and
            treatments, i.e. an exactly identified IV regression. For low variance, use
            the optimal instruments by project the instrument on the treatment vector, i.e.
            Z -> E[T | Z], in a first stage estimation.
        sample_weight : array-like of shape (n_samples,), default=None
            Sample weights. If None, then samples are equally weighted. Splits
            that would create child nodes with net zero or negative weight are
            ignored while searching for a split in each node.

        Returns
        -------
        self : object
        """
        return super().fit(X, T, y, Z=Z, sample_weight=sample_weight)

    def _get_alpha_and_pointJ(self, X, T, y, *, Z):
        # Append a constant treatment and constant instrument if `fit_intercept=True`,
        # the coefficient in front of the constant treatment is the intercept in the moment equation.
        _, Z = check_X_y(X, Z, y_numeric=True, multi_output=True, accept_sparse=False)
        Z = np.atleast_1d(Z)
        if Z.ndim == 1:
            Z = np.reshape(Z, (-1, 1))

        if not Z.shape[1] == T.shape[1]:
            raise ValueError("The dimension of the instrument should match the dimension of the treatment. "
                             "This method handles only exactly identified instrumental variable regression. "
                             "Preprocess your instrument by projecting it to the treatment space.")

        if self.fit_intercept:
            T = np.hstack([T, np.ones((T.shape[0], 1))])
            Z = np.hstack([Z, np.ones((Z.shape[0], 1))])

        return y * Z, cross_product(Z, T)

    def _get_n_outputs_decomposition(self, X, T, y, *, Z):
        n_relevant_outputs = T.shape[1]
        n_outputs = n_relevant_outputs
        if self.fit_intercept:
            n_outputs = n_relevant_outputs + 1
        return n_outputs, n_relevant_outputs


class RegressionForest(BaseGRF):
    """
    An implementation of a subsampled honest random forest regressor on top of an sklearn
    regression tree. Implements subsampling and honesty as described in [rf3]_,
    but uses a scikit-learn regression tree as a base. It provides confidence intervals based on ideas
    described in [rf3]_ and [rf4]_

    A random forest is a meta estimator that fits a number of classifying
    decision trees on various sub-samples of the dataset and uses averaging
    to improve the predictive accuracy and control over-fitting.
    The sub-sample size is smaller than the original size and subsampling is
    performed without replacement. Each decision tree is built in an honest
    manner: half of the sub-sampled data are used for creating the tree structure
    (referred to as the splitting sample) and the other half for calculating the
    constant regression estimate at each leaf of the tree (referred to as the estimation sample).
    One difference with the algorithm proposed in [rf3]_ is that we do not ensure balancedness
    and we do not consider poisson sampling of the features, so that we guarantee
    that each feature has a positive probability of being selected on each split.
    Rather we use the original algorithm of Breiman [rf1]_, which selects the best split
    among a collection of candidate splits, as long as the max_depth is not reached
    and as long as there are not more than max_leafs and each child contains
    at least min_samples_leaf samples and total weight fraction of
    min_weight_fraction_leaf. Moreover, it allows the use of both mean squared error (MSE)
    and mean absoulte error (MAE) as the splitting criterion. Finally, we allow
    for early stopping of the splits if the criterion is not improved by more than
    min_impurity_decrease. These techniques that date back to the work of [rf1]_,
    should lead to finite sample performance improvements, especially for
    high dimensional features.

    The implementation also provides confidence intervals
    for each prediction using a bootstrap of little bags approach described in [rf3]_:
    subsampling is performed at hierarchical level by first drawing a set of half-samples
    at random and then sub-sampling from each half-sample to build a forest
    of forests. All the trees are used for the point prediction and the distribution
    of predictions returned by each of the sub-forests is used to calculate the standard error
    of the point prediction.

    Parameters
    ----------
    n_estimators : int, default=100
        Number of trees

    max_depth : int, default=None
        The maximum depth of the tree. If None, then nodes are expanded until
        all leaves are pure or until all leaves contain less than
        min_samples_split samples.

    min_samples_split : int or float, default=10
        The minimum number of samples required to split an internal node:

        - If int, then consider `min_samples_split` as the minimum number.
        - If float, then `min_samples_split` is a fraction and
          `ceil(min_samples_split * n_samples)` are the minimum
          number of samples for each split.

    min_samples_leaf : int or float, default=5
        The minimum number of samples required to be at a leaf node.
        A split point at any depth will only be considered if it leaves at
        least ``min_samples_leaf`` training samples in each of the left and
        right branches.  This may have the effect of smoothing the model,
        especially in regression.

        - If int, then consider `min_samples_leaf` as the minimum number.
        - If float, then `min_samples_leaf` is a fraction and
          `ceil(min_samples_leaf * n_samples)` are the minimum
          number of samples for each node.

    min_weight_fraction_leaf : float, default=0.0
        The minimum weighted fraction of the sum total of weights (of all
        the input samples) required to be at a leaf node. Samples have
        equal weight when sample_weight is not provided.

    max_features : int, float or {"auto", "sqrt", "log2"}, default=None
        The number of features to consider when looking for the best split:

        - If int, then consider `max_features` features at each split.
        - If float, then `max_features` is a fraction and
          `int(max_features * n_features)` features are considered at each
          split.
        - If "auto", then `max_features=n_features`.
        - If "sqrt", then `max_features=sqrt(n_features)`.
        - If "log2", then `max_features=log2(n_features)`.
        - If None, then `max_features=n_features`.

        Note: the search for a split does not stop until at least one
        valid partition of the node samples is found, even if it requires to
        effectively inspect more than ``max_features`` features.

    min_impurity_decrease : float, default=0.0
        A node will be split if this split induces a decrease of the impurity
        greater than or equal to this value.
        The weighted impurity decrease equation is the following::

            N_t / N * (impurity - N_t_R / N_t * right_impurity
                                - N_t_L / N_t * left_impurity)

        where ``N`` is the total number of samples, ``N_t`` is the number of
        samples at the current node, ``N_t_L`` is the number of samples in the
        left child, and ``N_t_R`` is the number of samples in the right child.
        ``N``, ``N_t``, ``N_t_R`` and ``N_t_L`` all refer to the weighted sum,
        if ``sample_weight`` is passed.

    max_samples : int or float in (0, 1], default=.45,
        The number of samples to use for each subsample that is used to train each tree:

        - If int, then train each tree on `max_samples` samples, sampled without replacement from all the samples
        - If float, then train each tree on ceil(`max_samples` * `n_samples`), sampled without replacement
          from all the samples.

        If `inference=True`, then `max_samples` must either be an integer smaller than `n_samples//2` or a float
        less than or equal to .5.

    min_balancedness_tol: float in [0, .5], default=.45
        How imbalanced a split we can tolerate. This enforces that each split leaves at least
        (.5 - min_balancedness_tol) fraction of samples on each side of the split; or fraction
        of the total weight of samples, when sample_weight is not None. Default value, ensures
        that at least 5% of the parent node weight falls in each side of the split. Set it to 0.0 for no
        balancedness and to .5 for perfectly balanced splits. For the formal inference theory
        to be valid, this has to be any positive constant bounded away from zero.

    honest : bool, default=True
        Whether each tree should be trained in an honest manner, i.e. the training set is split into two equal
        sized subsets, the train and the val set. All samples in train are used to create the split structure
        and all samples in val are used to calculate the value of each node in the tree.

    inference : bool, default=True
        Whether inference (i.e. confidence interval construction and uncertainty quantification of the estimates)
        should be enabled. If `inference=True`, then the estimator uses a bootstrap-of-little-bags approach
        to calculate the covariance of the parameter vector, with am objective Bayesian debiasing correction
        to ensure that variance quantities are positive.

    subforest_size : int, default=4,
        The number of trees in each sub-forest that is used in the bootstrap-of-little-bags calculation.
        The parameter `n_estimators` must be divisible by `subforest_size`. Should typically be a small constant.

    n_jobs : int or None, default=-1
        The number of parallel jobs to be used for parallelism; follows joblib semantics.
        `n_jobs=-1` means all available cpu cores. `n_jobs=None` means no parallelism.

    random_state : int, RandomState instance or None, default=None
        Controls the randomness of the estimator. The features are always
        randomly permuted at each split. When ``max_features < n_features``, the algorithm will
        select ``max_features`` at random at each split before finding the best
        split among them. But the best found split may vary across different
        runs, even if ``max_features=n_features``. That is the case, if the
        improvement of the criterion is identical for several splits and one
        split has to be selected at random. To obtain a deterministic behaviour
        during fitting, ``random_state`` has to be fixed to an integer.

    verbose : int, default=0
        Controls the verbosity when fitting and predicting.

    warm_start : bool, default=False
        When set to ``True``, reuse the solution of the previous call to fit
        and add more estimators to the ensemble, otherwise, just fit a whole
        new forest. If ``True``, then `oob_predict` method for out-of-bag predictions is not available.

    Attributes
    ----------
    feature_importances_ : ndarray of shape (n_features,)
        The feature importances based on the amount of parameter heterogeneity they create.
        The higher, the more important the feature.
        The importance of a feature is computed as the (normalized) total heterogeneity that the feature
        creates. Each split that the feature was chosen adds::

            parent_weight * (left_weight * right_weight)
                * mean((value_left[k] - value_right[k])**2) / parent_weight**2

        to the importance of the feature. Each such quantity is also weighted by the depth of the split.
        By default splits below `max_depth=4` are not used in this calculation and also each split
        at depth `depth`, is re-weighted by ``1 / (1 + `depth`)**2.0``. See the method ``feature_importances``
        for a method that allows one to change these defaults.

    estimators_ : list of objects of type :class:`~econml.grf.GRFTree`
        The fitted trees.


    Examples
    --------

    .. testcode::

        import numpy as np
        from econml.grf import RegressionForest
        from sklearn.datasets import make_regression
        from sklearn.model_selection import train_test_split

        np.set_printoptions(suppress=True)
        np.random.seed(123)
        X, y = make_regression(n_samples=1000, n_features=4, n_informative=2,
                               random_state=0, shuffle=False)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5)
        regr = RegressionForest(max_depth=None, random_state=0,
                                n_estimators=1000)

    >>> regr.fit(X_train, y_train)
    RegressionForest(n_estimators=1000, random_state=0)
    >>> regr.feature_importances_
    array([0.88..., 0.11..., 0.00..., 0.00...])
    >>> regr.predict(np.ones((1, 4)), interval=True, alpha=.05)
    (array([[121.0...]]), array([[103.6...]]), array([[138.3...]]))

    References
    ----------

    .. [rf1] L. Breiman, "Random Forests", Machine Learning, 45(1), 5-32, 2001.

    .. [rf3] S. Athey, S. Wager, "Estimation and Inference of Heterogeneous Treatment Effects using Random Forests",
            Journal of the American Statistical Association 113.523 (2018): 1228-1242.

    .. [rf4] S. Athey, J. Tibshirani, and S. Wager, "Generalized random forests",
            The Annals of Statistics, 47(2), 1148-1178, 2019.

    """

class BeatForest(BaseGRF):

    def __init__(self,
                 alpha = 0.01, 
                 demean = 1,
                 n_estimators=100, *,
                 criterion="beat",
                 max_depth=None,
                 min_samples_split=10,
                 min_samples_leaf=5,
                 min_weight_fraction_leaf=0.,
                 min_var_fraction_leaf=None,
                 min_var_leaf_on_val=False,
                 max_features="auto",
                 min_impurity_decrease=0.,
                 max_samples=.45,
                 min_balancedness_tol=.45,
                 honest=True,
                 inference=True,
                 fit_intercept=True,
                 subforest_size=4,
                 n_jobs=-1,
                 random_state=None,
                 verbose=0,
                 warm_start=False):
        self.alpha = alpha
        self.demean = demean
        super().__init__(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth,
                         min_samples_split=min_samples_split,
                         min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf,
                         min_var_fraction_leaf=min_var_fraction_leaf, min_var_leaf_on_val=min_var_leaf_on_val,
                         max_features=max_features, min_impurity_decrease=min_impurity_decrease,
                         max_samples=max_samples, min_balancedness_tol=min_balancedness_tol,
                         honest=honest, inference=inference, fit_intercept=fit_intercept,
                         subforest_size=subforest_size, n_jobs=n_jobs, random_state=random_state, verbose=verbose,
                         warm_start=warm_start)

    def fit(self, X, T, y, Z, *, sample_weight=None):
        y, T, X, _ = check_inputs(y, T, X, W=None, multi_output_T=True, multi_output_Y=True)

        if sample_weight is not None:
            sample_weight = _check_sample_weight(sample_weight, X, DOUBLE)

        # Remap output
        n_samples, self.n_features_ = X.shape

        y = np.atleast_1d(y)
        if y.ndim == 1:
            # reshape is necessary to preserve the data contiguity against vs
            # [:, np.newaxis] that does not.
            y = np.reshape(y, (-1, 1))

        self.n_y_ = y.shape[1]

        T = np.atleast_1d(T)
        if T.ndim == 1:
            # reshape is necessary to preserve the data contiguity against vs
            # [:, np.newaxis] that does not.
            T = np.reshape(T, (-1, 1))
        
        
        alpha, pointJ = self._get_alpha_and_pointJ(X, T, y)
        self.n_outputs_, self.n_relevant_outputs_ = self._get_n_outputs_decomposition(X, T, y)
        tmp_alpha = np.ones((n_samples,1))*self.alpha
        tmp_demean = np.ones((n_samples,1))*self.demean
        tmp_Z = Z.copy()
        
        #if (self.demean ==1):
        #    tmp_Z = tmp_Z - np.mean(Z,axis = 0)
        #range_z = np.ones((n_samples,1))*Z.shape[1]
        if (self.n_features_ > tmp_Z.shape[1]):
            tmp_Z = np.hstack([tmp_Z,np.zeros((n_samples,self.n_features_-tmp_Z.shape[1]))])
        self.add_dim = 0
        
        if (self.n_features_ < tmp_Z.shape[1]):
            self.add_dim = -self.n_features_+tmp_Z.shape[1]
            X = np.hstack([X,np.zeros((n_samples,self.add_dim))])
            
        print(self.n_features_,tmp_Z.shape)    
        
        yaug = np.hstack([y, alpha, pointJ, tmp_Z, tmp_alpha, tmp_demean])
        
        if getattr(yaug, "dtype", None) != DOUBLE or not yaug.flags.contiguous:
            yaug = np.ascontiguousarray(yaug, dtype=DOUBLE)

        if getattr(X, "dtype", None) != DTYPE:
            X = X.astype(DTYPE)

        # Get subsample sample size
        n_samples_subsample = _get_n_samples_subsample(
            n_samples=n_samples,
            max_samples=self.max_samples
        )

        # Converting `min_var_fraction_leaf` to an absolute `min_var_leaf` that the GRFTree can handle
        if self.min_var_fraction_leaf is None:
            self.min_var_leaf = None
        elif (not isinstance(self.min_var_fraction_leaf, numbers.Real)) or (not (0 < self.min_var_fraction_leaf <= 1)):
            msg = "`min_var_fraction_leaf` must be in range (0, 1) but got value {}"
            raise ValueError(msg.format(self.min_var_fraction_leaf))
        else:
            # We calculate the min eigenvalue proxy that each criterion is considering
            # on the overall mean jacobian, to determine the absolute level of `min_var_leaf`
            jac = np.mean(pointJ, axis=0).reshape((self.n_outputs_, self.n_outputs_))
            min_var = np.min(np.abs(np.diag(jac)))
            if self.criterion == 'mse':
                for i in range(self.n_outputs_):
                    for j in range(self.n_outputs_):
                        if j != i:
                            det = np.sqrt(np.abs(jac[i, i] * jac[j, j] - jac[i, j] * jac[j, i]))
                            if det < min_var:
                                min_var = det
            self.min_var_leaf = min_var * self.min_var_fraction_leaf

        # Check parameters
        self._validate_estimator()

        random_state = check_random_state(self.random_state)
        # We re-initialize the subsample_random_seed_ only if we are not in warm_start mode or
        # if this is the first `fit` call of the warm start mode.
        if (not self.warm_start) or (not hasattr(self, 'subsample_random_seed_')):
            self.subsample_random_seed_ = random_state.randint(MAX_INT)
        else:
            random_state.randint(MAX_INT)  # just advance random_state
        subsample_random_state = check_random_state(self.subsample_random_seed_)

        if (self.warm_start and hasattr(self, 'inference_') and (self.inference != self.inference_)):
            raise ValueError("Parameter inference cannot be altered in between `fit` "
                             "calls when `warm_start=True`.")
        self.inference_ = self.inference
        self.warm_start_ = self.warm_start

        if not self.warm_start or not hasattr(self, "estimators_"):
            # Free allocated memory, if any
            self.estimators_ = []
            self.slices_ = []
            # the below are needed to replicate randomness of subsampling when warm_start=True
            self.slices_n_samples_ = []
            self.slices_n_samples_subsample_ = []
            self.n_samples_ = []
            self.n_samples_subsample_ = []

        n_more_estimators = self.n_estimators - len(self.estimators_)

        if n_more_estimators < 0:
            raise ValueError('n_estimators=%d must be larger or equal to '
                             'len(estimators_)=%d when warm_start==True'
                             % (self.n_estimators, len(self.estimators_)))

        elif n_more_estimators == 0:
            warn("Warm-start fitting without increasing n_estimators does not "
                 "fit new trees.")
        else:
            if self.inference:
                if not isinstance(self.subforest_size, numbers.Integral):
                    raise ValueError("Parameter `subforest_size` must be "
                                     "an integer but got value {}.".format(self.subforest_size))
                if self.subforest_size < 2:
                    raise ValueError("Parameter `subforest_size` must be at least 2 if `inference=True`, "
                                     "but got value {}".format(self.subforest_size))
                if not (n_more_estimators % self.subforest_size == 0):
                    raise ValueError("The number of estimators to be constructed must be divisible "
                                     "the `subforest_size` parameter. Asked to build `n_estimators={}` "
                                     "with `subforest_size={}`.".format(n_more_estimators, self.subforest_size))
                if n_samples_subsample > n_samples // 2:
                    if isinstance(self.max_samples, numbers.Integral):
                        raise ValueError("Parameter `max_samples` must be in [1, n_samples // 2], "
                                         "if `inference=True`. "
                                         "Got values n_samples={}, max_samples={}".format(n_samples, self.max_samples))
                    else:
                        raise ValueError("Parameter `max_samples` must be in (0, .5], if `inference=True`. "
                                         "Got value {}".format(self.max_samples))

            if self.warm_start and len(self.estimators_) > 0:
                # We draw from the random state to get the random state we
                # would have got if we hadn't used a warm_start.
                random_state.randint(MAX_INT, size=len(self.estimators_))

            trees = [self._make_estimator(append=False,
                                          random_state=random_state).init()
                     for i in range(n_more_estimators)]

            if self.inference:
                if self.warm_start:
                    # Advancing subsample_random_state. Assumes each prior fit call has the same number of
                    # samples at fit time. If not then this would not exactly replicate a single batch execution,
                    # but would still advance randomness enough so that tree subsamples will be different.
                    for sl, n_, ns_ in zip(self.slices_, self.slices_n_samples_, self.slices_n_samples_subsample_):
                        subsample_random_state.choice(n_, n_ // 2, replace=False)
                        for _ in range(len(sl)):
                            subsample_random_state.choice(n_ // 2, ns_, replace=False)

                # Generating indices a priori before parallelism ended up being orders of magnitude
                # faster than how sklearn does it. The reason is that random samplers do not release the
                # gil it seems.
                n_groups = n_more_estimators // self.subforest_size
                new_slices = np.array_split(np.arange(len(self.estimators_),
                                                      len(self.estimators_) + n_more_estimators),
                                            n_groups)
                s_inds = []
                for sl in new_slices:
                    half_sample_inds = subsample_random_state.choice(n_samples, n_samples // 2, replace=False)
                    s_inds.extend([half_sample_inds[subsample_random_state.choice(n_samples // 2,
                                                                                  n_samples_subsample,
                                                                                  replace=False)]
                                   for _ in range(len(sl))])
            else:
                if self.warm_start:
                    # Advancing subsample_random_state. Assumes each prior fit call has the same number of
                    # samples at fit time. If not then this would not exactly replicate a single batch execution,
                    # but would still advance randomness enough so that tree subsamples will be different.
                    for _, n_, ns_ in zip(range(len(self.estimators_)), self.n_samples_, self.n_samples_subsample_):
                        subsample_random_state.choice(n_, ns_, replace=False)
                new_slices = []
                s_inds = [subsample_random_state.choice(n_samples, n_samples_subsample, replace=False)
                          for _ in range(n_more_estimators)]

            # Parallel loop: we prefer the threading backend as the Cython code
            # for fitting the trees is internally releasing the Python GIL
            # making threading more efficient than multiprocessing in
            # that case. However, for joblib 0.12+ we respect any
            # parallel_backend contexts set at a higher level,
            # since correctness does not rely on using threads.
            trees = Parallel(n_jobs=self.n_jobs, verbose=self.verbose, backend='threading')(
                delayed(t.fit)(X[s], yaug[s], self.n_y_, self.n_outputs_, self.n_relevant_outputs_,
                               sample_weight=sample_weight[s] if sample_weight is not None else None,
                               check_input=False)
                for t, s in zip(trees, s_inds))

            # Collect newly grown trees
            self.estimators_.extend(trees)
            self.n_samples_.extend([n_samples] * len(trees))
            self.n_samples_subsample_.extend([n_samples_subsample] * len(trees))
            self.slices_.extend(list(new_slices))
            self.slices_n_samples_.extend([n_samples] * len(new_slices))
            self.slices_n_samples_subsample_.extend([n_samples_subsample] * len(new_slices))

        return self
        
    def _get_alpha_and_pointJ(self, X, T, y):
        # Append a constant treatment if `fit_intercept=True`, the coefficient
        # in front of the constant treatment is the intercept in the moment equation.
        if self.fit_intercept:
            T = np.hstack([T, np.ones((T.shape[0], 1))])
        return y * T, cross_product(T, T)

    def _get_n_outputs_decomposition(self, X, T, y):
        n_relevant_outputs = T.shape[1]
        n_outputs = n_relevant_outputs
        if self.fit_intercept:
            n_outputs = n_relevant_outputs + 1
        return n_outputs, n_relevant_outputs


    def predict(self, X, interval=False, alpha=0.05):
        """ Return the prefix of relevant fitted local parameters for each x in X,
        i.e. theta(x)[1..n_relevant_outputs].

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples. Internally, it will be converted to
            ``dtype=np.float64``.
        interval : bool, default=False
            Whether to return a confidence interval too
        alpha : float in (0, 1), default=0.05
            The confidence level of the confidence interval. Returns a symmetric (alpha/2, 1-alpha/2)
            confidence interval.

        Returns
        -------
        theta(X)[1, .., n_relevant_outputs] : array-like of shape (n_samples, n_relevant_outputs)
            The estimated relevant parameters for each row of X
        lb(x), ub(x) : array-like of shape (n_samples, n_relevant_outputs)
            The lower and upper end of the confidence interval for each parameter. Return value is omitted if
            `interval=False`.
        """
        if (self.add_dim >0):
            X = np.hstack([X, np.zeros((X.shape[0], self.add_dim))])
        
        if interval:
            y_hat, lb, ub = self.predict_full(X, interval=interval, alpha=alpha)
            if self.n_relevant_outputs_ == self.n_outputs_:
                return y_hat, lb, ub
            return (y_hat[:, :self.n_relevant_outputs_],
                    lb[:, :self.n_relevant_outputs_], ub[:, :self.n_relevant_outputs_])
        else:
            y_hat = self.predict_full(X, interval=False)
            if self.n_relevant_outputs_ == self.n_outputs_:
                return y_hat
            return y_hat[:, :self.n_relevant_outputs_]
            
