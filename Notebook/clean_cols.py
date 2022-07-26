from glob import glob
import pandas as pd
import numpy as np
import datetime as dt
import jdatetime as jt
from persiantools import characters
from joblib import Parallel, delayed
import chardet

def clean_cols(df):
    dropped_cols = ['nTran','insCode', 'dEven', 'qTitNgJ', 'iSensVarP',
                    'pPhSeaCotJ', 'pPbSeaCotJ', 'iAnuTran',
                    'xqVarPJDrPRf', 'canceledCompony']
    df.insert(0,'trade_id',None)
    new_columns=['trade_id', 'time', 'vol', 'price',
                'national_id', 'date','canceled', 'namad']

    df.drop(columns=dropped_cols, inplace=True)
    df.columns=new_columns
    return df