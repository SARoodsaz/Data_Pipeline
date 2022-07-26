from glob import glob
import pandas as pd
import numpy as np
import datetime as dt
import jdatetime as jt
from persiantools import characters
from joblib import Parallel, delayed
import chardet

def str_to_time(df):
    df.time=df.time.astype(str).str.zfill(6)
    hour=df.time.str.slice_replace(2,)
    minute=df.time.str.slice_replace(start=4).str.slice_replace(stop=2)
    second=df.time.str.slice_replace(stop=4)
    time=hour+':'+minute+':'+second
    time=pd.to_datetime(time).dt.time
    df.drop(columns='time', inplace=True)
    df.insert(6, 'time', time)
    timestamp=df.date.astype(str) +" "+ df.time.astype(str)
    timestamp=pd.to_datetime(timestamp)
    df.insert(5,'datetime',timestamp)
    return df