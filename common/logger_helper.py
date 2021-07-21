"""
日志工具类
"""

__author__ = 'Richard'
__version__ = '2021-07-18'

import logging
import os
import time
from common import constants

LOG_FORMAT = '[%(asctime)s] - %(filename)s[line:%(lineno)d] - fuc:%(funcName)s- %(levelname)s: %(message)s'


# LOG_CLI_FORMAT = '%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)'
# LOG_FILE_FORMAT = '%(filename)s:%(lineno)s %(asctime)s %(levelname)s %(message)s'

class LoggerHelper:
    def __init__(self, path=None, level=logging.DEBUG, log_format=LOG_FORMAT):
        """
        :param path: 文件输出路径，默认项目根目录下 logs 文件夹
        """
        if path is None:
            self.log_path = constants.LOGS_DIR

        # 文件名：取当天日期
        self.log_name = os.path.join(self.log_path, 'log-%s.log' % time.strftime("%Y-%m-%d"))  # 日志地址
        self.logger = logging.getLogger()

        # 设置日志级别
        self.level = level
        self.logger.setLevel(level)

        # 日志输出格式
        self.formatter = logging.Formatter(log_format)

        # 初始化 handler
        # fh = self.__add_file_handler()
        # ch = self.__add_cli_handler()

    def __add_file_handler(self):
        """添加file handler"""
        # 创建一个FileHandler，用于写到本地, a 追加模式
        fh = logging.FileHandler(self.log_name, 'a')
        fh.setLevel(self.level)
        fh.setFormatter(self.formatter)
        # 添加一个日志
        self.logger.addHandler(fh)
        return fh

    def __add_cli_handler(self):
        """添加控制台 handler"""
        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(self.level)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)
        return ch

    def __console(self, level, message):

        # 添加 handler
        fh = self.__add_file_handler()
        ch = self.__add_cli_handler()

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)

        # 移除 handler
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)

        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)

    def get_logger(self):
        return self.logger


if __name__ == '__main__':
    # log = LoggerHelper(level=logging.INFO)
    log = LoggerHelper()
    log.debug("---测试开始 debug----")
    log.info("---测试开始----")
    log.info("输入密码")
    log.warning("----测试结束----")
    log.error("----测试异常----")
