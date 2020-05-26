import os
import math
import copy
import pandas as pd
import numpy as np
from adtk.data import validate_series
from adtk.detector import InterQuartileRangeAD, PersistAD, LevelShiftAD, SeasonalAD
from adtk.visualization import plot
from enum import Enum, IntEnum,unique,Enum
from datetime import datetime
import logging
import logging.handlers


indexes = ["压强", "温度", "湿度", "闪烁指数", "TEC"]
index_names = ["Pressure", "Temperature", "Humidity", "Flicker index", "TEC"]


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

    return [rangeLimitMin,rangeLimitMax]

def checkOutlier(data):
    dataCopy = copy.deepcopy(data)
    # 修改为时间序列索引
    dataCopy['时间'] = pd.to_datetime(dataCopy['时间'], format="%Y%m%d%H%M%S")
    dataCopy.set_index("时间", inplace=True)

    dataCopy = validate_series(dataCopy)
    iqr_ad = InterQuartileRangeAD(c=1.5)
    anomalies = iqr_ad.fit_detect(dataCopy)

    # 可视化异常图，并保存到本地
    for i, index in enumerate(indexes):
        axes = plot(dataCopy[index], anomaly=anomalies[index], ts_linewidth=1, ts_markersize=3, anomaly_markersize=5, anomaly_color='red', anomaly_tag="marker")
        axes[0].set_title(index_names[i], fontsize='xx-large')
        axes[0].legend(['Normal', 'Anomaly'] ,loc='best', fontsize='x-large')
        axes[0].set_xlabel('time', fontsize='x-large')
        axes[0].set_ylabel('value', fontsize='x-large')
        axes[0].figure.savefig(index + ".png")
    logging.log(logging.DEBUG, 'The abnormal curve has been drawn.')

    # 修改数据并统计异常比率
    rows, columns = anomalies.shape
    count = 0
    for row in range(rows):
        for col in range(columns):
            if anomalies.iloc[row,col]:
                count += 1
                data.iloc[row, col + 1] = math.nan
    if count != 0:
        logging.log(logging.DEBUG, 'There are no outliers.')
    outlierRate = float(count) / (rows * columns)
    return data, outlierRate

def checkSpike(data):
    dataCopy = copy.deepcopy(data)
    # 修改为时间序列索引
    dataCopy['时间'] = pd.to_datetime(dataCopy['时间'], format="%Y%m%d%H%M%S")
    dataCopy.set_index("时间", inplace=True)

    dataCopy = validate_series(dataCopy)
    persist_ad = PersistAD(c=3.0, side='positive')
    anomalies = persist_ad.fit_detect(dataCopy)

    # 修改数据并统计异常比率
    rows, columns = anomalies.shape
    count = 0
    for row in range(rows):
        for col in range(columns):
            if anomalies.iloc[row,col]:
                count += 1
                data.iloc[row, col + 1] = math.nan

    if count != 0:
        logging.log(logging.DEBUG, 'There are no spikes.')
    spikeRate = float(count) / (rows * columns)
    return data, spikeRate

def checkLevelShift(data):
    dataCopy = copy.deepcopy(data)
    # 修改为时间序列索引
    dataCopy['时间'] = pd.to_datetime(dataCopy['时间'], format="%Y%m%d%H%M%S")
    dataCopy.set_index("时间", inplace=True)

    dataCopy = validate_series(dataCopy)
    level_shift_ad = LevelShiftAD(c=6.0, side='both', window=5)
    anomalies = level_shift_ad.fit_detect(dataCopy)

    # 修改数据并统计异常比率
    rows, columns = anomalies.shape
    count = 0
    for row in range(rows):
        for col in range(columns):
            if anomalies.iloc[row, col]:
                count += 1
                data.iloc[row, col + 1] = math.nan
    if count != 0:
        logging.log(logging.DEBUG, 'There are no level shifts.')
    levelShiftRate = float(count) / (rows * columns)
    return data, levelShiftRate


def checkSeaonalAD(data):
    dataCopy = copy.deepcopy(data)
    # 修改为时间序列索引
    dataCopy['时间'] = pd.to_datetime(dataCopy['时间'], format="%Y%m%d%H%M%S")
    dataCopy.set_index("时间", inplace=True)

    dataCopy = validate_series(dataCopy)
    seasonal_ad = SeasonalAD(c=3.0, side="both")
    anomalies = seasonal_ad.fit_detect(dataCopy)

    # 修改数据并统计异常比率
    rows, columns = anomalies.shape
    count = 0
    for row in range(rows):
        for col in range(columns):
            if anomalies.iloc[row, col]:
                count += 1
                data.iloc[row, col + 1] = math.nan
    seasonalRate = float(count) / (rows * columns)
    return data, seasonalRate


def checkExceedRange(rangeLimit, data):   #检测越界数据并返回修改后的数据和越界率
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
                count += 1
    if count != 0:
        logging.log(logging.DEBUG, 'There are data that exceed range.')
    exceedRate = float(count)/(rows*columns)
    return data, exceedRate


def checkJumpData(rangeLimit, data):    #检测跳变数据并返回修改后的数据和跳变率
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

# 计算记录完整性
def completeness(data):
    '''
    :param data: 完整数据
    :return: 元素缺失率, 记录缺失率
    '''
    rows, columns = data.shape
    e_length = rows * columns
    r_length = rows

    dataList = list(np.array(data))

    e_count = 0
    r_count = 0
    # 如果输入数据类型有问题
    if not isinstance(dataList, list):
        logging.log(logging.ERROR, 'completeness: data type is wrong!!!')
        return False
    elif not isinstance(e_length, int):
        logging.log(logging.ERROR, 'completeness: length type is wrong!!!')
        return False
    elif e_length * r_length == 0:
        logging.log(logging.ERROR, 'completeness: length is zero!!!')
        return False
    for record in dataList:
        for element in record:
            # excel 浮点数单元格缺失会变成nan，但是仍占据位置
            if not math.isnan(element):
                e_count += 1
        if len(record) == e_length:
            r_count += 1
    element_missing_rate = e_count / (e_length * r_length)  # 现在的写法认为，缺失了一条记录代表其包含元素全部缺失。
    recording_missing_rate = r_count / r_length
    return element_missing_rate, recording_missing_rate


# 计算时间完整性
def timeliness(data, low_bound, high_bound):
    '''
    :param data: 完整数据
    :param low_bound: 日期下界
    :param high_bound: 日期上届
    :return:
    '''
    dataList = list(np.array(data))
    if not isinstance(dataList, list):
        logging.log(logging.ERROR, 'timeliness: data type is wrong!!!')
        return False
    elif not isinstance(low_bound, float):
        logging.log(logging.ERROR, 'timeliness: low_bound type is wrong!!!')
        return False
    elif not isinstance(high_bound, float):
        logging.log(logging.ERROR, 'timeliness: high_bound type is wrong!!!')
        return False
    count = 0
    for record in dataList:
        stamp = record[0]
        # 日期不在给定范围
        if stamp < low_bound or stamp > high_bound:
            count += 1
        # 日期非法
        elif not time_illegal_judge(stamp):
            count += 1
    return count / len(dataList)

# 判断时间是否合法
def time_illegal_judge(time):
    str_time = str(int(time))
    if len(str_time) != 14:
        return False
    elif int(str_time[0:4]) < 1990:
        return False
    elif int(str_time[4:6]) < 1 or int(str_time[4:6]) > 12:
        return False
    # 月份这里，嗯。。。
    elif int(str_time[6:8]) < 0 or int(str_time[6:8]) > 31:
        return False
    elif int(str_time[8:10]) < 0 or int(str_time[8:10]) > 24:
        return False
    elif int(str_time[10:12]) < 0 or int(str_time[10:12]) > 60:
        return False
    elif int(str_time[12:14]) < 0 or int(str_time[12:14]) > 60:
        return False
    else:
        return True


def evaluateAndClean(rangeLimit, data, policy):
    qualities = []

    # 计算记录完整性
    element_missing_rate, recording_missing_rate = completeness(data)
    qualities.append(element_missing_rate)
    qualities.append(recording_missing_rate)
    #补全缺失数据
    data = cleanData(policy, data)

    # 计算时间完整性
    time_illegal_rate = timeliness(data, float(20180202112100), float(20220202112100))
    qualities.append(time_illegal_rate)

    # 统计各种异常类型并清洗
    data, exceed_rate = checkExceedRange(rangeLimit, data)
    qualities.append(exceed_rate)
    data = cleanData(policy, data)

    data, outlier_rate = checkOutlier(data)
    qualities.append(outlier_rate)
    data = cleanData(policy, data)

    data, spike_rate = checkSpike(data)
    qualities.append(spike_rate)
    cleanData(policy, data)

    data, levelshift_rate = checkLevelShift(data)
    qualities.append(levelshift_rate)
    cleanData(policy, data)

    # 数据不遵循任何季节性变化趋势
    # data, seaonsal_rate = checkSeaonalAD(data)
    # qualities.append(seaonsal_rate)
    # cleanData(policy, data)

    qualities = ["%.2f%%"%(i*100) for i in qualities]

    # 返回清洗后的数据和各类质量评估指标
    # qualities中的元素依次为元素缺失率、记录缺失率、时间违法率、数据越界率、离群值率、毛刺异常率、等级偏移率
    return data, qualities


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
                            if row + low >= rows:
                                data.iloc[row, col] = data.iloc[row-1, col]
                            elif row - up <= 0:
                                data.iloc[row, col] = data.iloc[row+1, col]
                            else:
                                data.iloc[row,col] = (data.iloc[row-up,col]+data.iloc[row+low,col])/2
        return data


def getUpindex(data, col, row):
    i = 1
    while row - i >= 0 and np.isnan(data.iloc[row - i, col]):
        i += 1
    return i


def getLowindex(data, col, row):
    i = 1
    while row + i < data.shape[0] and np.isnan(data.iloc[row + i, col]):
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

if __name__ == '__main__':
    data = pd.read_excel('fake.xlsx')
    policy = averagePolicy()
    rangeLimit = ModifyRangeLimit()
    data, qualities = evaluateAndClean(rangeLimit, data, policy)
    print(qualities)
