import os

# os.system('pytest -s -v tests/test_baidu_ddt.py --alluredir=./reports/allure_results --clean-alluredir')
os.system('pytest --alluredir ./reports/allure_results --clean-alluredir')
os.system('allure serve ./reports/allure_results')
