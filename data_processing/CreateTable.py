# -*- coding: utf-8 -*-
"""
Created on Sat May 21 00:23:54 2016
@author: Demoon
"""

import sys
import os
import numpy as np
import pandas as pd
from datetime import datetime
import time
import math
from collections import defaultdict


from config import Config
import load_data

class Table(object):
    def __init__(self,config):

        self.config = config

    def timeConvert(self,date):

        strDate = date.split()
        t = strDate[1].split(':')
        num = int(t[0])*6+math.ceil((int(t[1])+(0 if int(t[2])==0 else 1))/10.0)
        return int(num)
            
        
    def constructTable(self, dataType):
        """
        66 by 144
        """
        loadDataInstance = load_data.Load_data(self.config)
        
        # dataType: 0????,1????
        if dataType == 0:
            orderData = loadDataInstance.train_order_data()
            weatherData = loadDataInstance.train_weather_data()
        else:
            orderData = loadDataInstance.test_order_data()
            weatherData = loadDataInstance.test_weather_data()
        
        
        for index, row in weatherData.iterrows():
            weatherData.ix[index, 'time']=self.timeConvert(row['time'])
        
        clusterMap = loadDataInstance.train_cluster_map()
        clusterDict = pd.Series(clusterMap[:,1], index=clusterMap[:,0])
        n = 66
        m = 144
        tableReq = np.zeros((n, m)) # ???
        tableAns = np.zeros((n, m)) # ???
        tableGap = np.zeros((n, m)) # ???
        
        tablePassenger = np.zeros((n, m)) # ???
        tableDriver = np.zeros((n, m)) # ???
        tableStart = np.zeros((n, m)) # ????       
        tablePriceMax = np.zeros((n, m)) # ????
        tablePriceMin = np.zeros((n, m)) # ????
        tablePriceSum = np.zeros((n, m)) # ???
        tablePriceMean = np.zeros((n, m)) # ????
        
        driverSet = [[set() for col in range(m)] for row in range(n)] #????
        passengerSet = [[set() for col in range(m)] for row in range(n)] #???? 
        startSet = [[set() for col in range(m)] for row in range(n)] #?????             
        priceSet = [[set() for col in range(m)] for row in range(n)] #???? 
        
        for i in range(len(orderData)):
            d = clusterDict[orderData[i][3]]
            r = self.timeConvert(orderData[i][6])
                      
            driverId = orderData[i][1]
            passengerId = orderData[i][2]
            start =  orderData[i][3]
            price = orderData[i][5]                         

            tableReq[d-1][r-1]+=1  
            tablePriceSum[d-1][r-1]+=price            
                        
            passengerSet[d-1][r-1].add(passengerId)
            startSet[d-1][r-1].add(start)
            priceSet[d-1][r-1].add(price)

            if pd.isnull(driverId):
                tableGap[d-1][r-1]+=1
            else:
                tableAns[d-1][r-1]+=1
                driverSet[d-1][r-1].add(driverId)
                
        for i in range(n):
            for j in range(m):
                tablePassenger[i][j]=len(passengerSet[i][j])
                tableDriver[i][j]=len(driverSet[i][j])
                tableStart[i][j]=len(startSet[i][j])
                tablePriceMax[i][j]=max(priceSet[i][j] or [0])
                tablePriceMin[i][j]=min(priceSet[i][j] or [0])
                

        return tableReq, tableAns, tableGap, tableStart, weatherData


def constructTime():
    """
    
    """
    date = list()
    week = list()
    for i in range(1,22):
        date.append('01-%02d'%(i))
        week.append(datetime(2016,1,i).weekday())
    return date, week
    

def constructTrain():

    date, week = constructTime()
    n = 66
    m = 144

    dateLen = len(date)
    
    
    #dateLen = 1  # uncomment this
    
    for i in range(dateLen):
        configInstance = Config(date[i])
        tableInstance = Table(configInstance)
        tableReq, tableAns, tableGap, tableDest,  tableWeather = tableInstance.constructTable(0)
        
        disList = list()    
        timeList = list() # ???
        dateList = list() # ??
        weekList = list() # ??
        reqList = list()
        ansList = list()
        gapList = list()
        for j in range(n):
            for k in range(m):
                disList.append(j+1)
                timeList.append(k+1)
                dateList.append(date[i])
                weekList.append(week[i])
                reqList.append(tableReq[j][k])
                ansList.append(tableAns[j][k])
                gapList.append(tableGap[j][k])
                #destList.append(tableDest[j][k])
        
        tableData = pd.DataFrame({'districtID':disList, 'time':timeList,'date':dateList,'week':weekList,'req':reqList,'ans':ansList, 'gap':gapList},columns=['districtID', 'time', 'date', 'week', 'req', 'ans', 'gap'])
        fileName = 'train/train_data_'+date[i]+'.csv'
        
        #tableWeather.loc[tableWeather['time'], 'time'] = 
        
        ResultTable = pd.merge(tableWeather,tableData, on = ['time'])
        #print ResultTable
        #ResultTable.head()
        loadInstance = load_data.Load_data(configInstance)
        loadInstance.save_file(fileName, ResultTable)
        
def constructTest():

  

    configInstance = Config('01-22')
    loadInstance = load_data.Load_data(configInstance)

    timeArr = loadInstance.test_set_1_readme1()
    TestLength = len(timeArr)
    #TestLength = 1
    
    dateDict  = defaultdict(list)

    for j in range(TestLength):   
        strTime = timeArr[j][0]
        tmp = strTime.split('-')
        ind = int(tmp[3])-1
        day = int(tmp[2])
        date = ('01-%02d')%(day)
        dateDict[date].append(ind-3)
        dateDict[date].append(ind-2)
        dateDict[date].append(ind-1)
           
    n = 66


    
    for date in dateDict:
        configInstance = Config(date)
        tableInstance = Table(configInstance)
        tableReq, tableAns, tableGap, tableDest, tableWeather= tableInstance.constructTable(1)
        
        disList = list()    
        timeList = list() # ???
        dateList = list() # ??
        weekList = list() # ??
        reqList = list()
        ansList = list()
        gapList = list()
        destList = list()

        
        tmp = date.split('-')
        week = datetime(2016,1,int(tmp[1])).weekday()
        
        for j in range(n):
            for k in dateDict[date]:
                disList.append(j+1)
                timeList.append(k+1)
                dateList.append(date)
                weekList.append(week)
                reqList.append(tableReq[j][k])
                ansList.append(tableAns[j][k])
                gapList.append(tableGap[j][k])
                destList.append(tableDest[j][k])
        
        tableData = pd.DataFrame({'districtID':disList, 'time':timeList,'date':dateList,'week':weekList,'req':reqList,'ans':ansList, 'gap':gapList},columns=['districtID', 'time', 'date', 'week', 'req', 'ans', 'gap'])
        fileName = 'test/test_data_'+date+'.csv'
        
        
        ResultTable = pd.merge(tableWeather,tableData, on = ['time'])
        
        loadInstance = load_data.Load_data(configInstance)
        loadInstance.save_file(fileName, ResultTable)
            
def testing(date):

        strDate = date.split()
        t = strDate[1].split(':')
        num = int(t[0])*6+math.ceil((int(t[1])+(0 if int(t[2])==0 else 1))/10.0)
        return int(num)   
            
def main():

   
    constructTrain()
    
    #constructTest()

    


    




if __name__ == '__main__':
    main()
