import os
import pandas as pd
import numpy as np
import logging
import logging.handlers

def evaluate(data):
    #计算每一列的缺失率
    row, col = data.shape
    #col_total = data.isnull().sum().sort_values(ascending=False)  # 从大到小按顺序排每个特征缺失的个数
    col_percent = (data.isnull().sum() / data.isnull().count()).sort_values(ascending=False)  # 从大到小按顺序排每个特征缺失率
    total_percent = data.isnull().sum().sum()/(row*col) #总的缺失率
    return col_percent, total_percent


class cleanPolicy:
    def clean(self, data):
        return data

class deletePolicy(cleanPolicy):  #删除含有缺失值的行
    def clean(self, data):
        cleanData = data.dropna(axis=0, how='any')
        return cleanData

class meanPolicy(cleanPolicy):  #使用均值填充缺失值
    def clean(self, data):
        cleanData = data.fillna(data.mean())
        return cleanData

class nearPolicy(cleanPolicy):  #使用相邻值进行填充
    def clean(self, data):
        cleanData = data.fillna(method = 'ffill') #前向后填充
        # data.fillna(method = 'bfill') #后向前填充
        return cleanData

class averagePolicy(cleanPolicy): #采用前后两值的平均值填充
    def clean(self, data):
        rows, columns = data.shape
        for col in range(columns):
            if data.iloc[:,col].count() != rows: #存在空值
                for row in range(rows):
                    if np.isnan(data.iloc[row,col]):
                        if row == 0: #若为第一行
                            data.iloc[row,col] = data.iloc[row+1, col]
                        elif row == rows - 1: #若为最后一行
                            data.iloc[row,col] = data.iloc[row-1, col]
                        else:
                            up = getUpindex(data,col,row)
                            low = getLowindex(data,col,row)
                            data.iloc[row,col] = (data.iloc[row-up,col]+data.iloc[row+low,col])/2
        return data

def getUpindex(data, col, row):
    i = 1
    while np.isnan(data.iloc[row - i, col]):
        i += 1
    return i

def getLowindex(data, col, row):
    i = 1
    while np.isnan(data.iloc[row + i, col]):
        i += 1
    return i


def cleanData(cleanpolicy, data):
    # logger.debug("开始数据清洗！")
    return cleanpolicy.clean(data)


logger = logging.getLogger("logger")
handler1 = logging.StreamHandler()
handler2 = logging.FileHandler(filename="test.log")

logger.setLevel(logging.DEBUG)
handler1.setLevel(logging.WARNING) #文件输出DEBUG级别的日志，控制台输出WARNING级别的日志
handler2.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
handler1.setFormatter(formatter)
handler2.setFormatter(formatter)

logger.addHandler(handler1)
logger.addHandler(handler2)

logger.debug("hhh")
