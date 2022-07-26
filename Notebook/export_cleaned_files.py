from glob import glob
import pandas as pd
import numpy as np
import datetime as dt
import jdatetime as jt
from persiantools import characters
from joblib import Parallel, delayed
import chardet

def export_cleaned_files(df,count):
    path='C:/Users/Sarv/Desktop/vs_code/Git/ETL-pipeline/data/processed/trade_history_h5/'
    return df.to_hdf(path=path+f'trade_history_table_b{count}_cleaned.h5',
                     key='trade_history_table_b1_cleaned',
                     mode='a',
                     complevel=5,
                     index=False,format='table')