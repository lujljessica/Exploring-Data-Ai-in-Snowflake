import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from pmdarima import auto_arima
import xgboost as xgb
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.model_selection import TimeSeriesSplit

'''
This script contains my commonly used metrics or evaluations used for ML models 
'''
def normalized_rmse(rmse, min, max):
    return round((rmse/ (max - min)),2)

def get_model_metrics(y_test, y_pred):
    '''
    Args: 
    y_test NumPy array:  containing all actuals for the test set
    y_pred NumPy array: containing all the predicted values for the test set
    
    Returns: pd.Dataframe: with RMSE, MAE, MAPE, R2, MSLE
    '''
    # Calculate the evaluation metrics
    mae = mean_absolute_error(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    r2 = r2_score(y_test, y_pred)
    msle = np.mean(np.square(np.log1p(y_test) - np.log1p(y_pred)))
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    metrics = pd.DataFrame({
        "RMSE":[round(rmse,2)],
        "MAE":[round(mae,2)],
        "MAPE":[round(mape,2)],
        "R²":[round(r2,2)],
        "MSLE":[round(msle,2)]})
    
    return metrics

def get_data_stats(col):
    '''
    Args: 
    col:Target Array or pd.DataFrame[col] you want stats
    Returns: pd.Dataframe:  min, max, mean, median and STD
    '''
    test_set_metrics = pd.DataFrame({
        "Min": [round(col.min(),2)],
        "Max": [round(col.max(),2)],
        "Mean":[round(col.mean(),2)],
        "Median": [round(col.median(),2)],
        "STD" :[round(col.std(),2)]
    })
    return test_set_metrics