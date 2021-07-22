# auto-test-template

Automated testing template

## Getting started

```bash
# install dependency
pip3 install -r requirements.txt

# for MacOS
brew install allure
# ulimit -c unlimited

# Driver requirements
https://www.selenium.dev/documentation/en/webdriver/driver_requirements/

# run test
pytest -s -v --alluredir=./reports/allure_results --clean-alluredir tests/test_baidu_ddt.py
# pytest -s -v --alluredir=./reports/allure_results --clean-alluredir --browser=Firefox tests/test_baidu_ddt.py

# start allure server
allure serve ./reports/allure_results

# generate html report
#allure generate ./reports/allure_results
allure generate -c -o ./reports/allure-report ./reports/allure_results

# open allure report
allure open ./reports/allure-report


```

## MacOS

```bash

# vim .zshrc

# python B
alias python="/opt/homebrew/bin/python3"
alias pip="/opt/homebrew/bin/pip3"
# alias python2="/System/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7"
alias python2="/usr/bin/python2"
alias pip2="/usr/local/bin/pip2"
# python E

# selenium B
export SELENIUM_DRIVER_HOME=$HOME/workspace/software/selenium_driver
export PATH=$PATH:$SELENIUM_DRIVER_HOME/
# selenium E

# openjdk B
# export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"
# openjdk E

```

## Project Structure

```tree
├── common              # common or lib
├── config              # configs
│    └── allure         # allure config
├── data                # data driven: excel、json、csv
├── docs                # documents
├── logs                # logging files
├── pages               # Page Object Model (POM) 
├── reports             # test reports
├── screenshots         # error screenshots
└── tests               # test cases
    ├── conftest.py     # fixture
├── pytest.ini          # pytest config
├── LICENSE
├── README.md
├── requirements.txt
```

## Documents

- [python](https://github.com/python/cpython)
- [selenium](https://github.com/SeleniumHQ/selenium)
- [pytest](https://github.com/pytest-dev/pytest)
- [allure2](https://github.com/allure-framework/allure2)
- [pandas](https://github.com/pandas-dev/pandas)
