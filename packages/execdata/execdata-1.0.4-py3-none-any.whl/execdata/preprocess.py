'''
Date         : 2022-10-25 17:21:52
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2022-10-26 11:50:41
LastEditors  : BDFD
Description  : 
FilePath     : \execdata\preprocess.py
Copyright (c) 2022 by BDFD, All Rights Reserved. 
'''


import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def encode(df):
    lable = LabelEncoder()
    for column in df:
        if df[column].dtypes == 'object':
            df[column] = lable.fit_transform(df[column])
    return df

def split(df):
    X = df.iloc[:,1:-1]
    y = df.iloc[:,-1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=66)
    return X_train, X_test, y_train, y_test