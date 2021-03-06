from __future__ import division
"""
Baysian hyperparameter optimization [https://github.com/fmfn/BayesianOptimization]
for Mean Absoulte Error objective
on default features for https://www.kaggle.com/c/allstate-claims-severity
"""

__author__ = "Vladimir Iglovikov"

import pandas as pd
from sklearn.metrics import mean_absolute_error
from bayes_opt import BayesianOptimization
from tqdm import tqdm
import numpy as np
from scipy.stats import skew, boxcox
import os
import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import KFold, cross_val_score

from sklearn.metrics import make_scorer
from pylab import *
import clean_data
from sklearn.linear_model import ElasticNet, Ridge


RANDOM_STATE = 2016
n_folds = 5


def evalerror(preds, dtrain):
    return mean_absolute_error(np.exp(preds), np.exp(dtrain))


def en_evaluate(alpha):

    # clf = ElasticNet(alpha=alpha, l1_ratio=l1_ratio)
    clf = Ridge(alpha=alpha)

    kf = KFold(n_folds, shuffle=True, random_state=RANDOM_STATE).get_n_splits(X_train)

    return -cross_val_score(clf, X_train, y_train, cv=kf, scoring=make_scorer(evalerror), n_jobs=-1).mean()


if __name__ == '__main__':
    num_rounds = 10000
    random_state = 2016
    num_iter = 100
    init_points = 10
    shift = 200

    # X_train, y_train, _, _, _, _ = clean_data.one_hot_categorical()
    X_train, y_train, _, _, _, _ = clean_data.one_hot_categorical(shift=shift, quadratic=True)

    print X_train.shape, y_train.shape

    # previous_points = pd.read_csv('params/parameters.csv')

    lrBO = BayesianOptimization(en_evaluate, {'alpha': (0, 1000)})

    # xgbBO.initialize_df(previous_points)

    lrBO.maximize(init_points=init_points, n_iter=num_iter)

    # Save results
    param_cache_path = 'params'
    try:
        os.mkdir(param_cache_path)
    except:
        pass

    file_name = 'params/lr_parameters.csv'
    lrBO.points_to_csv(file_name)
