import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import roc_auc_score, roc_curve, auc
from matplotlib import pyplot as plt
import lightgbm as lgb
import xgboost as xgb

def get_nunique_values(df):
    data = df.apply(pd.Series.nunique, axis=0).reset_index()
    data.columns = ['feature', 'count']
    
    return data

def get_nunique_values_train_test(df_train, df_test):
    train = get_nunique_values(df_train)
    test = get_nunique_values(df_test)
    
    table = pd.merge(train, test, on='feature', how='outer')
    table.columns = ['feature', 'count, TRAIN', 'count, TEST']
    return table

def missing_values_table(df, drop_good_columns=False):
        missing_values = df.isnull().sum()
        missing_values_percent = 100 * df.isnull().sum() / len(df)
        
        table = pd.concat([missing_values, missing_values_percent], axis=1)
        table.columns = ['amount', '%']
        
        if drop_good_columns: 
            table = table[table['amount'] != 0]
        
        return table
    
def missing_values_train_test(df_train, df_test, column_target=None, drop_good_columns=True):
    if column_target: 
        df_train = df_train.drop(columns=column_target)
        
    table_train = missing_values_table(df_train)
    table_test = missing_values_table(df_test)
    
    table_train.columns = ['TRAIN, amount', 'TRAIN, %']
    table_test.columns = ['TEST, amount', 'TEST, %']
    
    table = pd.concat([table_train, table_test], axis=1)
    
    if drop_good_columns:
        table = table[table.values.sum(axis=1) != 0]
        
    return table

def plot_binary_feature(df, feature, target):
    data_counts = df[feature].value_counts().reset_index()
    # какой процент людей, имеющих одинаковые значения признака, не выплачивает кредит? 
    data = df.groupby(feature)[target].value_counts(normalize=True).\
            rename('percentage').mul(100).reset_index()
    data = data[data[target]==1]
    
    fig, (axes_counts, axes_percentage) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
    
    sns.barplot(x='index', y=feature, data=data_counts, ax=axes_counts)
    axes_counts.set_xlabel(feature)
    axes_counts.set_ylabel('count')
    
    sns.barplot(x=feature, y='percentage', data=data, ax=axes_percentage)
    axes_percentage.set_title(target+' = 1')
    
    plt.subplots_adjust(wspace=0.5)
    
def plot_category_feature(df, feature, target, orient='v', figsize=(10, 5)):
    data_counts = df[feature].value_counts().reset_index()
    # какой процент людей, имеющих одинаковые значения признака, не выплачивает кредит? 
    data = df.groupby(feature)[target].value_counts(normalize=True).\
            rename('percentage').mul(100).reset_index()
    data = data[data[target]==1]
    data.sort_values('percentage', ascending=False, inplace=True)
    
    fig, (axes_counts, axes_percentage) = plt.subplots(nrows=1, ncols=2, figsize=figsize)
    
    if orient=='v':
        sns.barplot(x='index', y=feature, data=data_counts, ax=axes_counts, orient=orient)
        sns.barplot(x=feature, y='percentage', data=data, ax=axes_percentage, orient=orient)
        
        axes_counts.set_xlabel(feature)
        axes_counts.set_ylabel('count')
        axes_percentage.set_title(target+' = 1')
    else:
        sns.barplot(x=feature, y='index', data=data_counts, ax=axes_counts, orient=orient)
        sns.barplot(x='percentage', y=feature, data=data, ax=axes_percentage, orient=orient)
        
        axes_counts.set_xlabel('count')
        axes_counts.set_ylabel(feature)
        axes_percentage.set_title(target+' = 1')
    
    plt.subplots_adjust(wspace=0.5)
    
def plot_float_feature(df, feature, target, figsize=(12, 6), xlim=None):
    df0 = df[df[target] == 0]
    df1 = df[df[target] == 1]

    fig, axes = plt.subplots(figsize=figsize)
    
    sns.kdeplot(df0[feature].dropna(), label=target+' = 0', color='b', ax=axes)
    sns.kdeplot(df1[feature].dropna(), label=target+' = 1', color='r', ax=axes)

    plt.xlabel(feature)
    plt.ylabel('Density')
    axes.set_xlim(xlim)
    plt.show()