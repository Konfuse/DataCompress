import math
from cleantool import cleanAndEvaluate as cae
from enum import IntEnum,unique


@unique
class rangeLimiEnum(IntEnum):
    time = 0
    pres = 1
    temper = 2
    humi = 3
    spark = 4
    tec = 5
    sta = 6
    code = 7
    pha = 8
    size = 9                  #size放最后


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

def checkExceedRange(rangeLimit,data):   #检测越界数据
    rangeLimitMin = rangeLimit[0][rangeLimiEnum.time:rangeLimiEnum.sta]+rangeLimit[0][rangeLimiEnum.sta : rangeLimiEnum.pha+1]*10
    rangeLimitMax = rangeLimit[1][rangeLimiEnum.time:rangeLimiEnum.sta]+rangeLimit[1][rangeLimiEnum.sta : rangeLimiEnum.pha+1]*10
    rows, columns = data.shape
    for row in range(rows):
        for col in range(columns):
            if data.iloc[row,col]<rangeLimitMin[col]:
                data.iloc[row,col]= math.nan
            if data.iloc[row,col]>rangeLimitMax[col]:
                data.iloc[row,col]= math.nan
    return data


def checkJumpData(rangeLimit,data):     #检测跳变数据
    Mid_Len=10  #10个数据取一次中位数
    rangeLimitChangeTres = rangeLimit[2][rangeLimiEnum.time:rangeLimiEnum.sta]+rangeLimit[2][rangeLimiEnum.sta : rangeLimiEnum.pha+1]*10
    rows, columns = data.shape
    for row in range(rows):
        for col in range(columns):
            end_row=min(row+Mid_Len,rows)   #不做双向，保证了空值填充不会影响下一个
            if abs(data.iloc[row,col]-data.iloc[row:end_row,col].median()) > rangeLimitChangeTres[col]:
                data.iloc[row,col]= math.nan
    return data

def clean_range_jump(rangeLimit,data,policy):
    tmp_data=checkExceedRange(rangeLimit,data) 
    error_rate=cae.evaluate(tmp_data)[1]
    elim_range_data=cae.cleanData(policy,tmp_data)
    tmp_data=checkJumpData(rangeLimit,elim_range_data) 
    error_rate+=cae.evaluate(tmp_data)[1]
    elim_range_jump_data=cae.cleanData(policy,tmp_data)
    return [elim_range_jump_data,error_rate]
