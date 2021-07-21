"""定义常量文件
项目目录等
"""

__author__ = 'Richard'
__version__ = '2021-07-18'

import os

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 获取Logs目录路径
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# 获取Reports目录路径
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

# 获取截图目录
PICTURE_DIR = os.path.join(BASE_DIR, 'screenshots')

if __name__ == '__main__':
    print(BASE_DIR)
    print(LOGS_DIR)
    print(REPORTS_DIR)
    print(PICTURE_DIR)
