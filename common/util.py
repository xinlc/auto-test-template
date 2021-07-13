""" 通用工具

生成随机字符串
获取日志
"""

__author__ = 'Richard'
__version__ = '2021-07-10'

import pickle
import random
import string
import os
import pandas as pd


# 获取日志
def get_logger():
    import logging
    import logging.handlers
    import datetime

    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)

    rf_handler = logging.handlers.TimedRotatingFileHandler('all.log', when='midnight', interval=1, backupCount=7,
                                                           atTime=datetime.time(0, 0, 0, 0))
    rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    f_handler = logging.FileHandler('error.log')
    f_handler.setLevel(logging.ERROR)
    f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

    logger.addHandler(rf_handler)
    logger.addHandler(f_handler)
    return logger


# 生成随机字符串
def gen_random_str():
    rand_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    return rand_str


def save_cookie(driver, path):
    with open(path, 'wb') as filehandler:
        cookies = driver.get_cookies()
        print(cookies)
        pickle.dump(cookies, filehandler)


def load_cookie(driver, path):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)


# 读取Excel文件 - list
def read_data_from_excel(excel_file, sheet_name):
    if not os.path.exists(excel_file):
        raise ValueError("File not exists")
    df = pd.read_excel(excel_file, sheet_name)
    return df.values.tolist()


# 读取Excel文件 - dic
def read_data_dic_from_excel(excel_file, sheet_name):
    if not os.path.exists(excel_file):
        raise ValueError("File not exists")
    df = pd.read_excel(excel_file, sheet_name)

    # 转换字典

    # 方式一
    # 拿到表头: [A, B, C, D]
    head_list = list(df.columns)
    list_dic = []

    # i 为每一行的value的列表：[a2, b2, c3, d2]
    for i in df.values:
        a_line = dict(zip(head_list, i))
        list_dic.append(a_line)

    # 方式二
    # # 替换Excel表格内的空单元格，否则在下一步处理中将会报错
    # df.fillna("", inplace=True)
    # list_dic = []
    # for i in df.index.values:
    #     # loc为按列名索引 iloc 为按位置索引，使用的是 [[行号], [列名]]
    #     df_line = df.loc[i, ['search_string', 'expect_string']].to_dict()
    #     # 将每一行转换成字典后添加到列表
    #     list_dic.append(df_line)

    return list_dic
