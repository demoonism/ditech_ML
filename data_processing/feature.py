# -*- coding: utf-8 -*-
"""
Created on Tue May 24 18:20:28 2016

@author: q
"""

import sys
import os
import numpy as np
import pandas as pd
from datetime import datetime
import time
import math
from collections import defaultdict
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder

from config import Config
import load_data

        
def featureConstruct(flag):
    """
    construct feature
    one hot encoding for feature category
    for continuous features: 
        flag=0, no nomarlization
        flag=1, normalize
    """
            
    configInstanceTrain = Config('feature.csv')
    loadInstanceTrain = load_data.Load_data(configInstanceTrain)
    data_train = loadInstanceTrain.feature_data()

    configInstanceTest = Config('feature_test.csv')
    loadInstanceTest = load_data.Load_data(configInstanceTest)
    data_test = loadInstanceTest.feature_data()
    
    
    if flag ==1:
        data_train_continuous = data_train[:, 3:]
        data_test_continuous = data_test[:, 3:]
        scaler = preprocessing.StandardScaler().fit(data_train_continuous)
        feature_train_continuous = scaler.transform(data_train_continuous) 
        feature_test_continuous = scaler.transform(data_test_continuous)
        data_train[:, 3:] = feature_train_continuous
        data_test[:, 3:] = feature_test_continuous

    enc = OneHotEncoder( categorical_features=np.array([0, 1, 2]), n_values=[67, 145, 7])
    
    enc.fit(data_train)  
    feature_train = enc.transform(data_train).toarray()  
    feature_test = enc.transform(data_test).toarray()
    

        
    
    filename_train = "feature_train_processed.csv"
    filename_test = "feature_test_processed.csv"
    
    loadInstanceTrain.save_file(filename_train, pd.DataFrame(feature_train))
    loadInstanceTrain.save_file(filename_test, pd.DataFrame(feature_test))
    

    
        
def main():
    """
  
    """
    
    flag = 1 
    featureConstruct(flag)    
    

    
    

if __name__ == '__main__':
    main()        