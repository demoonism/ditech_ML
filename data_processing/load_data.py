# -*- coding: utf-8 -*-
"""
Created on Fri May 20 20:28:32 2016

@author: Demoon
"""

import sys
import os
import numpy as np
import pandas as pd
from datetime import datetime
import time
import math
import config

class Load_data(object):
    def __init__(self,config):
        """
        :type config: Config
        :initializing..
        """
        self.config = config
        
    def train_order_data(self):
        """
        load training order data: numeric or category
        """
        reader = pd.read_csv(self.config.path_train_order_data, header=-1, iterator=False, delimiter='\t', encoding='utf-8')
        order_data = reader
        return np.array(order_data)
        
    def train_weather_data(self):
        """
        load training order data: numeric or category
        """
        reader = pd.read_table(self.config.path_train_weather_data, header=-1, iterator=False, delimiter='\t', encoding='utf-8', names = ['time', 'weather','temperature', 'PM25'])
        weather_data = reader
        return weather_data
        
    def train_cluster_map(self):
        """
        load cluster map
        """
        reader = pd.read_csv(self.config.path_train_cluster_map, header=-1, iterator=False, delimiter='	', encoding='utf-8')
        cluster_map = reader
        return np.array(cluster_map)
        
    def test_set_1_readme1(self):
        """
        timeslot to predict
        """
        reader = pd.read_csv(self.config.path_test_set_1_readme1, header=0, iterator=False, delimiter='	', encoding='utf-8')
        time_arr = reader
        return np.array(time_arr)
        
    def test_order_data(self):
        """
        load test order data: numeric or category
        """
        reader = pd.read_csv(self.config.path_test_set_1_order_data, header=-1, iterator=False, delimiter='	', encoding='utf-8')
        order_data = reader
        return np.array(order_data)
        
    def test_weather_data(self):
        """
        load training order data: numeric or category
        """
        reader = pd.read_table(self.config.path_test_set_1_weather_data, header=-1, iterator=False, delimiter='\t', encoding='utf-8', names = ['time', 'weather','temperature', 'PM25'])
        weather_data = reader
        return weather_data

    def feature_data(self):
        """
        load features:numeric or category
        """
        reader = pd.read_csv(self.config.path_feature_data, header=0, iterator=False, delimiter=',', encoding='utf-8')
        feature_data = reader
        return np.array(feature_data)
        
    def result_data(self):
        """
        load result: numeric or category
        """
        reader = pd.read_csv(self.config.path_result_data, header=-1, iterator=False, delimiter=',', encoding='utf-8')
        result_data = reader
        return np.array(result_data)
        
    def save_file(self, fileName, data):
        path = self.config.output_path_train + fileName
        data.to_csv(path,sep=',',mode='wb',header=True,index=False)
    

def main():
   
    config_instance = config.Config('01-01')
    #load_data_instance = Load_data(config_instance)
    #order = load_data_instance.train_order_data();
    #print order
    
    load_data_instance = Load_data(config_instance)
    weather = load_data_instance.train_weather_data();
    print np.array(weather['time'])
    
if __name__ == '__main__':
    main()
 
 
 