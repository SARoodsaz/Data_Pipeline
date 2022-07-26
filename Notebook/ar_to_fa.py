from glob import glob
import pandas as pd
import numpy as np
import datetime as dt
import jdatetime as jt
from persiantools import characters
from joblib import Parallel, delayed
import chardet

def ar_to_fa(df):
    fa_cols = ['namad']
    df[fa_cols]=df[fa_cols].applymap(lambda x: characters.ar_to_fa(x))
    return df