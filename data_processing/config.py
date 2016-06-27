# -*- coding: utf-8 -*-
"""
Created on Fri May 20 20:28:32 2016

@author: Demoon
"""

import os

"""
class Config
"""
class Config(object):
    def __init__(self,date):
        self.scale_date=date

         #Path
        self.path = 'C:/Users/xians/Desktop/citydata/' #data_dir
        self.path_train = self.path+'training_data/' # training set
        self.path_train_order_data = self.path_train + 'order_data/order_data_2016-'+ self.scale_date   #training order data             
        self.path_train_cluster_map = self.path_train + 'cluster_map/cluster_map'   #training read cluster map
        self.path_train_weather_data = self.path_train + 'weather_data/weather_data_2016-'+ self.scale_date   #training order data  
     
        self.path_test_set_1 = self.path+'test_set_1/' #test set
        self.path_test_set_1_readme1 =  self.path_test_set_1 + 'read_me_1.txt' # timeslot to predict 
        self.path_test_set_1_order_data = self.path_test_set_1 + 'order_data/order_data_2016-' + self.scale_date + '_test' # test order data
        self.path_test_set_1_weather_data = self.path_test_set_1 + 'weather_data/weather_data_2016-' + self.scale_date + '_test' # test order data
        
        self.output_path = self.path+'output/'
        self.output_path_train=self.output_path #training output
        
        self.path_feature_data = self.path+'feature/' + self.scale_date # feature set
        
        self.path_result_data = self.path+'result/' + self.scale_date # result folder


    def init_path(self):
        """
        初始化文件目录
        """
        self.output_path = self.path+'output/'
        self.output_path_train=self.output_path + 'train/' #set output file path
        self.output_path_test =self.output_path + 'test/'
        self.output_path_feature =self.path + 'feature/'
        paths=[self.output_path, self.output_path_train,self.output_path_test,self.output_path_feature]
        for path in paths:
            if not os.path.exists(path):
                os.mkdir(path)
        

def main():
    instance = Config('01-01')
    instance.init_path()
    pass

if __name__ == '__main__':
    main()