from glob import glob
import pandas as pd
import numpy as np
import datetime as dt
import jdatetime as jt
from persiantools import characters
from joblib import Parallel, delayed
import chardet

def str_to_date(df):
    year = df.date.astype(str).str.slice_replace(4,)
    month = df.date.astype(str).str.slice_replace(start=6).str.slice_replace(stop=4)
    day = df.date.astype(str).str.slice_replace(stop=6,)
    date=day+'-'+month+'-'+year
    date = pd.to_datetime(date).dt.date
    df.drop(columns='date', inplace=True)
    df.insert(5,'date',date)
    return df