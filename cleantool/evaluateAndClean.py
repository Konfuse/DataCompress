import os
import math
import pandas as pd
import numpy as np
from enum import Enum, IntEnum,unique,Enum
import logging
import logging.handlers


@unique
class rangeLimiEnum(IntEnum): #枚举每一列
    time=0
    pres=1
    temper=2
    humi =3
    spark =4
    tec =5
    sta =6
    code =7
    pha=8
    size  =9                  #size放最后


def ModifyRangeLimit():
    rangeLimitMin=[float('-inf')]*rangeLimiEnum.size          #范围下界
    rangeLimitMax=[float('-inf')]*rangeLimiEnum.size          #范围上界
    rangeLimitChangeTres=[float('inf')]*rangeLimiEnum.size    #跳变阈值

    rangeLimitMin[rangeLimiEnum.time]=float('-inf')
    rangeLimitMin[rangeLimiEnum.pres]=float('-inf')
    rangeLimitMin[rangeLimiEnum.temper]=float('-inf')
    rangeLimitMin[rangeLimiEnum.humi]=float('-inf')
    rangeLimitMin[rangeLimiEnum.spark]=float('-inf')
    rangeLimitMin[rangeLimiEnum.tec]=float('-inf')
    rangeLimitMin[rangeLimiEnum.sta]=float('-inf')
    rangeLimitMin[rangeLimiEnum.code]=float('-inf')
    rangeLimitMin[rangeLimiEnum.pha]=float('-inf')

    rangeLimitMax[rangeLimiEnum.time]=float('inf')
    rangeLimitMax[rangeLimiEnum.pres]=float('inf')
    rangeLimitMax[rangeLimiEnum.temper]=float('inf')
    rangeLimitMax[rangeLimiEnum.humi]=float('inf')
    rangeLimitMax[rangeLimiEnum.spark]=float('inf')
    rangeLimitMax[rangeLimiEnum.tec]=float('inf')
    rangeLimitMax[rangeLimiEnum.sta]=float('inf')
    rangeLimitMax[rangeLimiEnum.code]=float('inf')
    rangeLimitMax[rangeLimiEnum.pha]=float('inf')

    rangeLimitChangeTres[rangeLimiEnum.time]=float('inf')
    rangeLimitChangeTres[rangeLimiEnum.pres]=float(10)
    rangeLimitChangeTres[rangeLimiEnum.temper]=float(10)
    rangeLimitChangeTres[rangeLimiEnum.humi]=float(10)
    rangeLimitChangeTres[rangeLimiEnum.spark]=float(10)
    rangeLimitChangeTres[rangeLimiEnum.tec]=float(10)
    rangeLimitChangeTres[rangeLimiEnum.sta]=float('inf')
    rangeLimitChangeTres[rangeLimiEnum.code]=float(10)
    rangeLimitChangeTres[rangeLimiEnum.pha]=float(10)
    return [rangeLimitMin,rangeLimitMax,rangeLimitChangeTres]

def checkExceedRange(rangeLimit,data):   #检测越界数据并返回修改后的数据和越界率
    rangeLimitMin = rangeLimit[0][rangeLimiEnum.time:rangeLimiEnum.sta]+rangeLimit[0][rangeLimiEnum.sta : rangeLimiEnum.pha+1]*10
    rangeLimitMax = rangeLimit[1][rangeLimiEnum.time:rangeLimiEnum.sta]+rangeLimit[1][rangeLimiEnum.sta : rangeLimiEnum.pha+1]*10
    rows, columns = data.shape
    count = 0
    for row in range(rows):
        for col in range(columns):
            if data.iloc[row,col]<rangeLimitMin[col]:
                data.iloc[row,col]= math.nan
                count += 1
            if data.iloc[row,col]>rangeLimitMax[col]:
                data.iloc[row,col]= math.nan
                count +=1
    exceedRate = float(count)/(rows*columns)
    return data, exceedRate


def checkJumpData(rangeLimit,data):    #检测跳变数据并返回修改后的数据和跳变率
    Mid_Len=10  #10个数据取一次中位数
    rangeLimitChangeTres = rangeLimit[2][rangeLimiEnum.time:rangeLimiEnum.sta]+rangeLimit[2][rangeLimiEnum.sta : rangeLimiEnum.pha+1]*10
    rows, columns = data.shape
    count = 0
    for row in range(rows):
        for col in range(columns):
            end_row=min(row+Mid_Len,rows)   #不做双向，保证了空值填充不会影响下一个
            if abs(data.iloc[row,col]-data.iloc[row:end_row,col].median()) > rangeLimitChangeTres[col]:
                data.iloc[row,col]= math.nan
                count += 1
    jumpRate = float(count)/(rows*columns)
    return data, jumpRate


def evaluateAndClean(rangeLimit, data, policy):
    #计算每一列的缺失率
    row, col = data.shape
    #col_total = data.isnull().sum().sort_values(ascending=False)  # 从大到小按顺序排每个特征缺失的个数
    # col_percent = (data.isnull().sum() / data.isnull().count()).sort_values(ascending=False)  # 从大到小按顺序排每个特征缺失率
    miss_rate = data.isnull().sum().sum()/(row*col) #总的缺失率

    #补全缺失数据
    data = cleanData(policy, data)

    #统计越界并清洗
    data, exceed_rate = checkExceedRange(rangeLimit, data)
    data = cleanData(policy, data)

    #统计跳变并清洗
    data, jump_rate = checkJumpData(rangeLimit, data)
    data = cleanData(policy, data)

    miss_rate="%.2f%%"%(miss_rate*100)
    exceed_rate = "%.2f%%" % (exceed_rate * 100)
    jump_rate = "%.2f%%" % (jump_rate * 100)
    # 返回清洗后的数据，缺失率，越界率和跳变率
    return data, miss_rate, exceed_rate, jump_rate


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


# logger = logging.getLogger("logger")
# handler1 = logging.StreamHandler()
# handler2 = logging.FileHandler(filename="test.log")
#
# logger.setLevel(logging.DEBUG)
# handler1.setLevel(logging.WARNING) #文件输出DEBUG级别的日志，控制台输出WARNING级别的日志
# handler2.setLevel(logging.DEBUG)
#
# formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
# handler1.setFormatter(formatter)
# handler2.setFormatter(formatter)
#
# logger.addHandler(handler1)
# logger.addHandler(handler2)

# df = readData("fake.xlsx")
# anomaly_data_info=AnomalydataInfo()
# policy = eac.averagePolicy()
# rangeLimit = eac.ModifyRangeLimit()
# data, miss_rate, exceed_rate, jump_rate = eac.evaluateAndClean(rangeLimit,df,policy)
# print("缺失率:" + str(miss_rate))
# print("越界率:" + str(exceed_rate))
# print("跳变率:" + str(jump_rate))
# logger.debug("hhh")
