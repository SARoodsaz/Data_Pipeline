import pandas as pd
import numpy as np
import glob
import os
from glob import glob
from operator import itemgetter
from persiantools import characters
from persiantools.jdatetime import JalaliDate
import persiantools
import re
from re import search
import itertools
from statistics import mode
import datetime as dt
import jdatetime as jt
from joblib import Parallel, delayed
import chardet
from pyparsing import Regex

def change_column_name(df):
    columns= df.columns.tolist()
    print(f'column name is: {columns}')
    input_1= input('do you want to change header: (n\y)')
    if input_1=='y':
        for i in columns:
            input_2= input(f'insert new name for {i}: ')
            df.rename(columns={i:input_2},inplace=True)

def column_clustering(df):
    columns= df.columns.tolist()
    print(f'column name is: {columns}')
    string_columns=[]
    code_columns=[]
    price_columns=[]
    input_1=None
    while input_1!='finish':
        input_1= input('choose type of clusters: (string\price\code) ')
        if input_1=='string':
            input_2=None
            while input_2!='finish':
                input_2=input('choose string column')
                string_columns.append(input_2)
            # string_columns.remove('finish')
        if input_1=='code':
            input_2=None
            while input_2!='finish':
                input_2=input('choose code column')
                code_columns.append(input_2)
            code_columns.remove('finish')
        if input_1=='price':
            input_2=None
            while input_2!='finish':
                input_2=input('choose price column')
                price_columns.append(input_2)
            price_columns.remove('finish')

    return string_columns,code_columns,price_columns

def code_clean(df,code_columns):
    for i in code_columns:
        try:
            df[i]= df[i].replace(['nan',np.nan,'NaN'],1000000000001234)
            df[i]=df[i].replace(r'-','',regex=True)
            df[i]=df[i].apply(np.int64)
            df[i]= df[i].astype(str)
            df[i]= df[i].replace(r'1000000000001234',np.nan, regex=True)
        except:
            print(f'error is in {i}')
    return df

def price_clean (df,price_columns):
    for i in price_columns:
        try:
            df[i]= df[i].apply(lambda x: x.astype(str))
            df[i]=df[i].apply(lambda x: x(np.int64))
        except:
            print(f'error is in {i}')
    return df

def string_clean(df,string_columns):
    for i in string_columns:
        try:
            df[i]=df[i].replace(regex=r'\u200c',value=' ')
            df[i]= df[i].apply(lambda x: str(x))
            df[i]=df[i].str.lower()
            df[i]=df[i].str.strip()
            df[i]=df[i].replace('  ',' ')
            df[i]=df[i].replace('(','-')
            df[i]=df[i].replace(')','')
            df[i]=df[i].replace('_',' ')
            df[i]=df[i].apply(lambda x: characters.ar_to_fa(x))
            df[i]=df[i].str.strip(' ')
            df[i]=df[i].replace(regex=['مجتمع','سهامی خاص','شرکت','سهامی عام','موسسه','-سهام'],value='')
        except:
            print(f'error is in {i}')
    return df
