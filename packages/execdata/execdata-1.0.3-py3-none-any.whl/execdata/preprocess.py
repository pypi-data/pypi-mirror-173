'''
Date         : 2022-10-25 17:21:52
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2022-10-25 17:27:30
LastEditors  : BDFD
Description  : 
FilePath     : \execdata\preprocess.py
Copyright (c) 2022 by BDFD, All Rights Reserved. 
'''


from numpy import numpy as np
from sklearn.preprocessing import LabelEncoder

def encode(df):
    lable = LabelEncoder()
    for column in df:
        if df[column].dtypes == 'object':
            df[column] = lable.fit_transform(df[column])