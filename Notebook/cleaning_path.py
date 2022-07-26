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

def excel_to_csv(path,dirr):
    extention='xlsx'
    os.chdir(path)
    for file in os.listdir(path):
        file_xlsx= pd.read_ecxel(file)
        file_xlsx.to_csv(dirr+"\\"+file.split('.')[0]+".csv",index=False)

def csv_to_xlsx(path,dirr):
    for file in os.listdir(path):
        df=pd.read_csv(path+'\\'+file)
        df.to_excel(dirr+'\\'+file.split('.')[0]+'xlsx',index=False)

def read_merge_output(path,dirr=None):
    input_1=input('select the type of file: (csv/xlsx) ')
    all_df=[]
    if input_1=='xlsx':
        input_2=input('insert the number of columns: ')
        input_2= int(input_2)
        for file in os.listdir(path):
            df=pd.read_xlsx(path+'\\'+file)
            file_name= file.split('.')[0]
            column_list= df.columns.tolist()
            len_df= len(column_list)
            if len_df== input_2:
                all_df.append(df)
            else:
                print(f'the number of columns of file {file_name} is {len_df}')
                input_3= input('remove column or add column: (add/remove) ')
                if input_3 == 'add':
                    input_4= input('name of column: ')
                    df[input_4]=None
                    all_df.append(df)
                if input_3=='remove':
                    input_5= input('name of removed column: ')
                    df.drop(columns=input_5)
                    all_df.append(df)
    if input_1=='csv':
        input_2=input('insert the number of columns: ')
        input_2= int(input_2)
        for file in os.listdir(path):
            df=pd.read_csv(path+'\\'+file)
            file_name= file.split('.')[0]
            column_list= df.columns.tolist()
            len_df= len(column_list)
            if len_df== input_2:
                all_df.append(df)
            else:
                print(f'the number of columns of file {file_name} is {len_df}')
                input_3= input('remove column or add column: (add/remove) ')
                if input_3 == 'add':
                    input_4= input('name of column: ')
                    df[input_4]=None
                    all_df.append(df)
                if input_3=='remove':
                    input_5= input('name of removed column: ')
                    df.drop(columns=input_5)
                    all_df.append(df)
    input_6=input('do you want output: (y/n) ')
    if input_6=='y':
        df_raw= pd.concat(all_df,ignore_index=True).reset_index(drop=True)
        input_7=input('file type: (xlsx\csv) ')
        if input_7== 'xlsx':
            input_8= ('file name: ')
            df_raw.to_excel(dirr+'\\'+input_8+'.xlsx',index=False)
        if input_7== 'csv':
            input_8= ('file name: ')
            df_raw.to_csv(dirr+'\\'+input_8+'.csv',index=False)
    if input_6=='n':
        df_raw= pd.concat(all_df,ignore_index=True).reset_index(drop=True)
    return df_raw

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

def code_clean(df, code_columns):
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

def price_clean (df, price_columns):
    input_1= input('type of price: (float/int)')
    if input_1=='int':
        for i in price_columns:
            try:
                df[i]= df[i].apply(lambda x: x.astype(str))
                df[i]=df[i].apply(lambda x: x(np.int64))
            except:
                print(f'error is in {i}')
    if input_1=='float':
        for i in price_columns:
            try:
                df[i]= df[i].apply(lambda x: x.astype(float))
            except:
                print(f'error is in {i}')
    return df

def string_clean(df,string_columns):
    for i in string_columns:
        try:
            df[i]= df[i].apply(lambda x: x.astype(str))
            df[i]=df[i].str.lower()
            df[i]=df[i].str.strip()
            df[i]=df[i].replace('  ',' ')
            df[i]=df[i].replace('(','-')
            df[i]=df[i].replace(')','')
            df[i]=df[i].replace('_',' ')
            df[i]=df[i].apply(lambda x: characters.ar_to_fa(x))
            df[i]=df[i].replace(regex=r'\u200c',value=' ')
            df[i]=df[i].str.strip(' ')
            df[i]=df[i].replace(regex=['مجتمع','سهامی خاص','شرکت','سهامی عام'],value='')
        except:
            print(f'error is in {i}')
    return df

def ar_to_fa(df):
    fa_cols = ['namad']
    df[fa_cols]=df[fa_cols].applymap(lambda x: characters.ar_to_fa(x))
    return df

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

def str_to_date(df):
    year = df.date.astype(str).str.slice_replace(4,)
    month = df.date.astype(str).str.slice_replace(start=6).str.slice_replace(stop=4)
    day = df.date.astype(str).str.slice_replace(stop=6,)
    date=day+'-'+month+'-'+year
    date = pd.to_datetime(date).dt.date
    df.drop(columns='date', inplace=True)
    df.insert(5,'date',date)
    return df

def date_to_jdate(df):
    jalalidate = df.date.apply(lambda x: jt.date.fromgregorian(date=x).strftime("%Y-%m-%d"))
    df.insert(6, 'jdate', jalalidate)
    return df

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

def remove_extra_words (pd_series):
    pd_series= pd_series.astype(str)
    pd_series=pd_series.replace(r'سهامی عام','',Regex=True)
    pd_series=pd_series.replace(r'شرکت','',Regex=True)
    pd_series=pd_series.replace(r'شرکت','',Regex=True)
    pd_series=pd_series.replace(r'مجتمع','',Regex=True)
    pd_series=pd_series.replace(r'سهامی خاص','',Regex=True)
    pd_series=pd_series.str.strip()
    pd_series=pd_series.str.strip(' ')
    return pd_series

def remove_extra_space(pd_series):
    pd_series=pd_series.astype(str)
    pd_series=pd_series.str.strip(' ')
    return pd_series

def remove_space(pd_series):
    pd_series=pd_series.astype(str)
    pd_series=pd_series.replace(r' ','',Regex=True)
    return pd_series

def export_cleaned_files(df,count,path):
    return df.to_hdf(path=path+f'trade_history_table_b{count}_cleaned.h5',
                     key='trade_history_table_b1_cleaned',
                     mode='a',
                     complevel=5,
                     index=False,format='table')

def pipeline (chunk):
    try:
        chunk.pipe(clean_cols).pipe(ar_to_fa).pipe(str_to_date).pipe(date_to_jdate)
        chunk.pipe(export_cleaned_files)
        count+=1
    except:
        print('failed')

