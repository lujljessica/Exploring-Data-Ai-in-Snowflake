import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from scipy.fft import fft
from multimethod import multimethod 

def create_ts_features(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    """
    Creates time series features from datetime index
    """
    df[date_col] = pd.to_datetime(df[date_col])
    df['Day_of_Week'] = df[date_col].dt.dayofweek
    df['Is_Weekend'] = df['Day_of_Week'].apply(lambda x: 1 if x >= 5 else 0)
    df['Quarter'] = df[date_col].dt.quarter
    df['Month'] = df[date_col].dt.month
    df['Year'] = df[date_col].dt.year
    #df['dayofyear'] = df['Date'].dt.dayofyear
    df['Day_of_Month'] = df[date_col].dt.day
    df['Week_of_year'] = df[date_col].dt.isocalendar().week
    return df


def apply_fourier_transform(df:pd.DataFrame, target : str):
    """    
    Fourier transformation is applied to capture periodic components or seasonality within time-series data.
    convert the target variable values into the frequency domain.
    
    The resulting ‘fourier_transform’ feature contains information about the amplitudes of different frequency components,
    aiding in the identification and modeling of cyclic patterns in the time series.
    """
    values = df[target].values
    fourier_transform = fft(values)
    df['fourier_transform'] = np.abs(fourier_transform)
    return df

"""
Single Time Series lags and rolling stats
"""
@multimethod
def add_lags(df: pd.DataFrame,lags, target)-> pd.DataFrame:
    for lag in lags:
        df[f'{target}_{lag}_lag'] = df[target].shift(lag)
    return df

@multimethod
def add_rolling_mean(df: pd.DataFrame,windows :list,target)-> pd.DataFrame:
    for win in windows:
        df[f'{target}_{win}_mean'] = df[target].rolling(window = win).mean()
    return df

@multimethod
def add_rolling_std(df: pd.DataFrame,windows :list,target)-> pd.DataFrame:
    for win in windows:
        df[f'{target}_{win}_std'] = df[target].rolling(window = win).std()
    return df

@multimethod
def add_rolling_max(df,windows :list,target)-> pd.DataFrame:
    for win in windows:
        df[f'{target}_{win}_max'] = df[target].rolling(window = win).max()
    return df

@multimethod
def add_rolling_min(df: pd.DataFrame,windows :list,target)-> pd.DataFrame:
    for win in windows:
        df[f'{target}_{win}_min'] = df[target].rolling(window = win).min()
    return df

def split_data_set(train_size: float, df: pd.DataFrame, target: list):
    train_size = 0.70
    train_df, test_df = train_test_split(df, test_size=1-train_size, shuffle=False)

    train_df.set_index('Date', inplace=True)
    test_df.set_index('Date', inplace=True)

    X_train = train_df.drop(columns=target)
    y_train = train_df[target]
    X_test = test_df.drop(columns=target)
    y_test = test_df[target]
    return  X_train, y_train, X_test, y_test

"""
multiple time-series lags and rolling stats
"""

@multimethod
def add_lags(df: pd.DataFrame,lags, target: str, ts_group: list)-> pd.DataFrame:
    for lag in lags:
        df[f'{target}_{lag}_lag'] = df.groupby(ts_group)[target].shift(lag)
    return df

@multimethod
def add_rolling_mean(df: pd.DataFrame,windows :list,target: str, ts_group: list)-> pd.DataFrame:
    for win in windows:
        df[f'{target}_{win}_mean'] =df.groupby(ts_group)[target].rolling(window = win).mean()
    return df

@multimethod
def add_rolling_std(df: pd.DataFrame,windows :list,target: str, ts_group: list)-> pd.DataFrame:
    for win in windows:
        df[f'{target}_{win}_std'] = df.groupby(ts_group)[target].rolling(window = win).std()
    return df

@multimethod
def add_rolling_max(df: pd.DataFrame,windows :list,target: str, ts_group: list)-> pd.DataFrame:
    for win in windows:
        df[f'{target}_{win}_max'] = df.groupby(ts_group)[target].rolling(window = win).max()
    return df

@multimethod
def add_rolling_min(df: pd.DataFrame,windows :list,target: str, ts_group: list)-> pd.DataFrame:
    for win in windows:
        df[f'{target}_{win}_min'] = df.groupby(ts_group)[target].rolling(window = win).min()
    return df