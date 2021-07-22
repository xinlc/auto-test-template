"""测试报告数据
处理测试报告数据
"""

__author__ = 'Richard'
__version__ = '2021-07-18'

import ast
import os
import glob

from common import utils
from common import constants


def get_failure_data() -> list[dict]:
    """
    获取失败数据
    需要先运行：allure generate -o ./reports/allure-report ./reports/allure_results
    :return: 失败数据
    """
    join_dir = os.path.join(constants.REPORTS_DIR, 'allure-report', 'data', 'test-cases', '*.json')
    files_path = glob.glob(join_dir)
    data_list = []
    for file in files_path:
        data = utils.read_data_from_json(file)
        # 取测试用例第一个参数值，根据实际情况调整
        pv = data['parameterValues'][0]
        status = data['status']
        if 'passed' != status:
            param = ast.literal_eval(pv)
            data_list.append(param)
    return data_list


if __name__ == '__main__':
    print(get_failure_data())
