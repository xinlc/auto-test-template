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
import time
import logging
import logging.handlers
import datetime
import cpca
import pandas as pd
from pandas import DataFrame
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from common import constants


def get_logger(name='myLogger', level=logging.DEBUG):
    """
    获取日志对象
    :param name: 日志名称
    :param level: 日志级别，默认 DEBUG
    :return: Logger
    """
    # import logging
    # import logging.handlers
    # import datetime

    log_format = logging.Formatter(
        '[%(asctime)s] - %(filename)s[line:%(lineno)d] - fuc:%(funcName)s - %(levelname)s: %(message)s')
    date = time.strftime("%Y-%m-%d")
    log_all_path = os.path.join(constants.LOGS_DIR, 'all-%s.log' % date)
    log_info_path = os.path.join(constants.LOGS_DIR, 'info-%s.log' % date)
    log_warn_path = os.path.join(constants.LOGS_DIR, 'warn-%s.log' % date)
    log_error_path = os.path.join(constants.LOGS_DIR, 'error-%s.log' % date)

    # 获取日志对象，设置日志级别
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 控制台日志
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)

    # 全部日志
    all_handler = logging.handlers.TimedRotatingFileHandler(log_all_path, when='midnight', interval=1, backupCount=7,
                                                            atTime=datetime.time(0, 0, 0, 0))
    all_handler.setLevel(logging.DEBUG)
    all_handler.setFormatter(log_format)

    # info 日志
    info_handler = logging.FileHandler(log_info_path)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(log_format)

    # warn 日志
    warn_handler = logging.FileHandler(log_warn_path)
    warn_handler.setLevel(logging.WARN)
    warn_handler.setFormatter(log_format)

    # error 日志
    error_handler = logging.FileHandler(log_error_path)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(log_format)

    # 添加 handler
    logger.addHandler(console_handler)
    logger.addHandler(all_handler)
    logger.addHandler(info_handler)
    logger.addHandler(warn_handler)
    logger.addHandler(error_handler)
    return logger


def gen_random_str():
    """生成随机字符串"""
    rand_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    return rand_str


def save_cookie(driver, path):
    """保存cookie"""
    with open(path, 'wb') as filehandler:
        cookies = driver.get_cookies()
        print(cookies)
        pickle.dump(cookies, filehandler)


def load_cookie(driver, path):
    """获取cookie"""
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)


def read_data_from_excel(excel_file, sheet_name, types=None):
    """读取Excel文件 - list"""
    if not os.path.exists(excel_file):
        raise ValueError("File not exists")
    df = pd.read_excel(excel_file, sheet_name, dtype=types)
    return df.values.tolist()


def read_data_dict_from_excel(excel_file, sheet_name, types=None) -> list[dict]:
    """读取Excel文件"""
    df = read_data_from_excel(excel_file, sheet_name, types)
    return df_to_dict(df)


# def read_data_dic_from_excel(excel_file, sheet_name, types=None):
#     """读取Excel文件 - dic"""
#     if not os.path.exists(excel_file):
#         raise ValueError("File not exists")
#     df = pd.read_excel(excel_file, sheet_name, dtype=types)
#
#     # 转换字典
#
#     # 方式一
#     # 拿到表头: [A, B, C, D]
#     head_list = list(df.columns)
#     list_dic = []
#
#     # i 为每一行的value的列表：[a2, b2, c3, d2]
#     for i in df.values:
#         a_line = dict(zip(head_list, i))
#         list_dic.append(a_line)
#
#     # 方式二
#     # # 替换Excel表格内的空单元格，否则在下一步处理中将会报错
#     # df.fillna("", inplace=True)
#     # list_dic = []
#     # for i in df.index.values:
#     #     # loc为按列名索引 iloc 为按位置索引，使用的是 [[行号], [列名]]
#     #     df_line = df.loc[i, ['search_string', 'expect_string']].to_dict()
#     #     # 将每一行转换成字典后添加到列表
#     #     list_dic.append(df_line)
#
#     return list_dic


def df_to_dict(df: DataFrame) -> list[dict]:
    """DataFrame 转 dict"""
    # 拿到表头，转换为字典结构
    head_list = list(df.columns)
    list_dic = []
    for i in df.values:
        a_line = dict(zip(head_list, i))
        list_dic.append(a_line)
    return list_dic


def is_null(val):
    """判断是否为null"""
    return pd.isnull(val)


def check_null_and_opt(val, method):
    """方法值不为空，则执行
    :param val: 执行方法参数
    :param method: 不为空执行的方法
    """
    if not is_null(val):
        method(val)


def ignored_exceptions_and_opt(method, ignored_exceptions=(TimeoutException, NoSuchElementException)):
    """执行函数，忽略指定异常
    :param method: 执行方法
    :param ignored_exceptions: 忽略异常
    """
    try:
        method()
    except ignored_exceptions as exc:
        # 记录日志
        get_logger().error(exc)


def ignored_exception_and_opt(method):
    """执行函数，忽略全部异常
    :param method: 执行方法
    """
    return ignored_exceptions_and_opt(method, Exception)


def chinese_location_resolution(location: str):
    """中文地址解析
    :args
        location: "江苏省南京市浦口区雨山西路89号群盛北江豪庭X栋"
    :returns
        province: 江苏省
        city: 南京市
        area: 浦口区
        address：雨山西路89号群盛北江豪庭X栋
        adcode：320111
    """
    location_strs = [location]
    df = cpca.transform(location_strs)
    province_city_area = df_to_dict(df)[0]
    province_city_area['province'] = province_city_area['省']
    province_city_area['city'] = province_city_area['市']
    province_city_area['area'] = province_city_area['区']
    province_city_area['address'] = province_city_area['地址']
    return province_city_area


if __name__ == '__main__':
    log = get_logger(__name__)
    log.info("你好")
    log.error("11111111")
    # log.warning("11111111")
    # log.error("11111111")
