[![Build Status](https://dev.azure.com/ms/EconML/_apis/build/status/Microsoft.EconML?branchName=main)](https://dev.azure.com/ms/EconML/_build/latest?definitionId=49&branchName=main)
[![PyPI version](https://img.shields.io/pypi/v/econml.svg)](https://pypi.org/project/econml/)
[![PyPI wheel](https://img.shields.io/pypi/wheel/econml.svg)](https://pypi.org/project/econml/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/econml.svg)](https://pypi.org/project/econml/)



<h1><img src="doc/econml-logo-icon.png" width="80px" align="left" style="margin-right: 10px;"> BEAT: A Python Package for ML-Based Heterogeneous Treatment Effects Estimation</h1>

**BEAT** is a Python package for estimating heterogeneous treatment effects from observational data via machine learning:

* All arguments are the same as the original package, but there are two new inputs: target.weight.penalty indicates the penalty assigned to the protected attributes. target.weights is a matrix that includes the protected characteristics. X should not inlcude the protected characteristics. 
* See full details about the BEAT method in the original paper: Eliminating unintended bias in personalized policies using bias-eliminating adapted trees (BEAT)
* Forked from https://github.com/Microsoft/EconML


# Getting Started

## Installation

Install the latest release from [PyPI](https://pypi.org/project/BEAT_TEST/):
```
pip install BEAT_TEST
```
## Usage Examples
### Estimation Methods

  ```Python
  from econml.grf import BeatForest
  #Setting Training treatment and outcome 
  treatment = ['W']
  outcome = ['Y']
  Y = train[outcome]
  T = train[treatment]
  #Setting Unprotected variables
  unprotected_covariate = ['X.V1', 'X.V2', 'X.V3', 'X.V4', 'X.V5', 'Z.V1', 'Z.V2', 'Z.V3', 'Z.V4']
  X1 = train[unprotected_covariate]
  #set parameters for BEAT and Fit in training values
  BEAT = BeatForest(alpha = 10, demean = 0, n_estimators = 8)                     
  BEAT.fit(X1, T, Y) 
  #Get prediction from test dataset
  prediction = BEAT.predict(X_test)
```

# References
Ascarza, E., &amp; Israeli, A. (2022). Eliminating unintended bias in personalized policies using bias-eliminating adapted trees (beat). Proceedings of the National Academy of Sciences, 119(11). https://doi.org/10.1073/pnas.2115293119 


