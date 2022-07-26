from glob import glob
import pandas as pd
import numpy as np
import datetime as dt
import jdatetime as jt
from persiantools import characters
from joblib import Parallel, delayed
import chardet

def date_to_jdate(df):
    jalalidate = df.date.apply(lambda x: jt.date.fromgregorian(date=x).strftime("%Y-%m-%d"))
    df.insert(6, 'jdate', jalalidate)
    return df