import pandas as pd
import numpy as np
import lightgbm as lgb
import xgboost as xgb

def make_prediction(df_train, df_test, columns, column_target, model, \
                   file, file_comment):
    
    model.fit(df_train[columns], df_train[column_target])
    preds = model.predict_proba(df_test[columns])[:, 1]
    
    sample_submission = pd.read_csv('data/sample_submission.csv')
    sample_submission['TARGET'] = preds
    
    sample_submission.to_csv('submissions/{}_{}.csv'.format(file, file_comment), index=False)
    
def predict_submission_lightgbm(df_train, df_test, columns, column_target, 
                                params, num_rounds, file, file_comment):
    
    params.pop('early_stopping_round', None)
    
    X_train = df_train[columns]
    X_test = df_test[columns]
    y_train = df_train[column_target]
    
    dtrain = lgb.Dataset(X_train, label=y_train)
    model = lgb.train(params, dtrain, num_rounds)
    prediction = model.predict(X_test)
    
    sample_submission = pd.read_csv('data/sample_submission.csv')
    sample_submission['TARGET'] = prediction
    
    sample_submission.to_csv('submissions/{}_{}.csv'.format(file, file_comment), index=False)