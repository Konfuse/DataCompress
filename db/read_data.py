import os
import pandas as pd
import logging

# 读取文件/目录，得到'.xlsx'文件，返回DataFrame
# logging.basicConfig(filename='logger.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# 得到目录下的所有'.xlsx'文件
def get_all_files(folder, files):
    file_list = os.listdir(folder)
    for file in file_list:
        file_path = os.path.join(folder, file)
        if os.path.isdir(file_path):
            get_all_files(file_path, files)
        else:
            if file.split(".")[-1] in ["xlsx", 'xls', "csv"]:
                files.append(file_path)


def read_file(file):
    if file.split(".")[-1] in ["xlsx", 'xls']:
        return pd.read_excel(file).sort_values(by=u"时间")
    if file.split(".")[-1] == "csv":
        return pd.read_csv(file).sort_values(by=u"时间")


def check(file):
    if not file.split(".")[-1] in ["xlsx", 'xls', 'csv']:
        logging.error(u"文件格式错误")
        return False
    return True


def read_data(file):
    # 判断该文件是目录还是文件
    if os.path.isdir(file):
        file_list = []
        get_all_files(file, file_list)
        if len(file_list) == 0:
            logging.error("文件不存在")
            return
        dfs = read_file(file_list[0])
        if len(file_list) > 1:
            for i in range(1, len(file_list)):
                df = read_file(file_list[i])
                dfs = pd.concat([dfs, df]).sort_values(by=u"时间")
        dfs = dfs.reset_index()
        logging.info(u"{}读取完成".format(file))
        return dfs
    elif check(file):
        dfs = read_file(file)
        logging.info(u"{}读取完成".format(file))
        return dfs
