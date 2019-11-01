import zlib
import pandas as pd
import numpy as np
import math
import time


def asMinutes(s):
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)


def Data_compress(df, out_path, level=-1):
    # df,DataFrame,待压缩数据
    # out_path,str，绝对路径+文件名(*.zlib)，压缩后的存储路径
    # level，int，压缩率，-1至9,0为最低（不压缩），9为最高，-1为适中（5或6）
    start = time.time()
    print("Start compressing...")
    string_data = df.to_string()
    bytes_data = bytes(string_data, encoding='utf-8')
    compress_data = zlib.compress(bytes_data, level)

    with open(out_path, 'wb+') as f:
        f.write(compress_data)

    end = time.time()
    print('Finish compressing...elapsed time:  ', asMinutes(end - start))
    print('-' * 50)


def Data_decompress(input_path, output_path):
    # input_path，str,待解压文件路径(*.zlib)
    # output_path,str, 解压后文件存储路径(*.xlsx)
    start = time.time()
    print("Start decompressing...")

    with open(input_path, 'rb+') as f:
        compress_data = f.read()
    decompress_data = zlib.decompress(compress_data)
    list_data = str(decompress_data, encoding='utf-8').split()
    list_data = [list_data[x] for x in range(len(list_data)) if
                 (x - 36) % 37 != 0]  # delete the index which pd auto added
    array_data = np.array(list_data).reshape(-1, 36)
    columns_list = array_data[0]
    data = pd.DataFrame(array_data, columns=columns_list).drop(0).reset_index(drop=True)
    data.to_excel(output_path, index=None, header=None)
    end = time.time()
    print('Finish decompressing...elapsed time:    ', asMinutes(end - start))
    return data


if __name__ == '__main__':
    start = time.time()
    print("Start reading...")
    df = pd.DataFrame(pd.read_excel(r'E:\数据压缩\data\test.xlsx'), index=None)
    print(df[:2])
    end = time.time()
    print('Finish reading...elapsed time:   ', asMinutes(end - start))
    print('-' * 50)

    Data_compress(df, r'E:\数据压缩\data\fake.zlib')
    Data_decompress(r'E:\数据压缩\data\fake.zlib', r'E:\数据压缩\data\fake-decompress.xlsx')
