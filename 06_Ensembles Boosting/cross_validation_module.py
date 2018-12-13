import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import roc_auc_score, roc_curve, auc
from matplotlib import pyplot as plt
import lightgbm as lgb
import xgboost as xgb

def get_cv_folds(df, column_target, n_splits=5):
    ss_split = StratifiedShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
    
    folds = []
    
    for train_index, valid_index in ss_split.split(df, df[column_target].values):
        folds.append((train_index, valid_index))
        
    return folds


def cross_validation(df, columns, column_target, folds, model, metric):
    train_metrics = []
    valid_metrics = []
    
    for i, fold in enumerate(folds):
        train_indices, valid_indices = fold

        X_train = df.loc[train_indices][columns]
        X_valid = df.loc[valid_indices][columns]
        y_train = df.loc[train_indices][column_target].values
        y_valid = df.loc[valid_indices][column_target].values

        model.fit(X_train, y_train)
        
        train_metric = metric(y_train, model.predict_proba(X_train)[:, 1])
        valid_metric = metric(y_valid, model.predict_proba(X_valid)[:, 1])
        train_metrics.append(train_metric)
        valid_metrics.append(valid_metric)
        
    return train_metrics, valid_metrics

def cross_validation_xgboost(df, columns, column_target, folds, params=None, num_rounds=50, metric=None):

    train_metrics = []
    valid_metrics = []
    
    for i, fold in enumerate(folds):
        train_indices, valid_indices = fold

        X_train = df.loc[train_indices][columns]
        X_valid = df.loc[valid_indices][columns]
        y_train = df.loc[train_indices][column_target].values
        y_valid = df.loc[valid_indices][column_target].values    
        
        dtrain = xgb.DMatrix(X_train, label=y_train)
        dvalid = xgb.DMatrix(X_valid, label=y_valid)

        model = xgb.train(params, dtrain, num_rounds)
        
        train_metric = metric(y_train, model.predict(dtrain))
        valid_metric = metric(y_valid, model.predict(dvalid))
        train_metrics.append(train_metric)
        valid_metrics.append(valid_metric)
        
    return train_metrics, valid_metrics

def cross_validation_lightgbm(df, columns, column_target, folds, params=None, num_rounds=50, 
                              metric=None, early_stopping_rounds=None, verbose_eval=True):

    train_metrics = []
    valid_metrics = []
    
    for i, fold in enumerate(folds):
        train_indices, valid_indices = fold

        X_train = df.loc[train_indices][columns]
        X_valid = df.loc[valid_indices][columns]
        y_train = df.loc[train_indices][column_target].values
        y_valid = df.loc[valid_indices][column_target].values    
        
        dtrain = lgb.Dataset(X_train, label=y_train)
        dvalid = lgb.Dataset(X_valid, label=y_valid)
        
        model = lgb.train(params, dtrain, num_boost_round=num_rounds, valid_sets=dvalid, 
                          early_stopping_rounds=early_stopping_rounds, verbose_eval=verbose_eval)
        
        train_metric = metric(y_train, model.predict(X_train))
        valid_metric = metric(y_valid, model.predict(X_valid))
        
        train_metrics.append(train_metric)
        valid_metrics.append(valid_metric)
        
    return train_metrics, valid_metrics

def plot_roc_curve_cv(roc_curve_metrics):
    size = len(roc_curve_metrics)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    for i in range(size):
        fpr = roc_curve_metrics[i][0]
        tpr = roc_curve_metrics[i][1]
        auc_score = auc(fpr, tpr)
        
        plt.plot(fpr, tpr, alpha=0.7, label='roc-auc, cv='+str(i))
    
    plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', label='chance', alpha=.8)
    plt.xlabel('fpr')
    plt.ylabel('tpr')
    plt.title('auc: ' + str(auc_score))
    plt.legend()
    plt.show()
    
