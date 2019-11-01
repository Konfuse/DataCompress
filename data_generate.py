import pandas as pd
import random
import numpy as np
import datetime


def get_new_data(old):
    seed = random.randint(1, 8)
    if seed < 3:
        return old + random.random() * 0.1
    elif seed < 7:
        return old
    else:
        return old - random.random() * 0.1


def get_abnormal_data(real_data):
    seed = random.randint(1, 100)
    if seed in (1, 73, 56):
        return real_data + random.randint(10, 30)
    elif seed in (12, 99):
        return ''
    else:
        return real_data


data = pd.read_excel('C:/Users/Konfuse/Desktop/数据压缩/数据格式.xlsx', dtype={'时间': str})
arr = data.iloc[0].values
columns_list = data.columns.values.tolist()

format_str = '%Y%m%d%H%M%S'
now = datetime.datetime.strptime(arr[0], format_str)
delta = datetime.timedelta(minutes=1)

for i in range(2000):
    now = now + delta
    time_now = datetime.datetime.strftime(now, format_str)

    new = [time_now]
    for x in range(1, len(arr)):
        if x in (6, 9, 12, 15, 18, 21, 24, 27, 30, 33):
            new.append(arr[x])
        else:
            arr[x] = get_new_data(arr[x])
            new.append(get_abnormal_data(arr[x]))

    new = np.array(new)
    df = pd.DataFrame(new.reshape(1, len(new)), columns=columns_list)
    data = data.append(df, ignore_index=True)

data.to_excel('C:/Users/Konfuse/Desktop/数据压缩/for_test.xlsx', index=None)
