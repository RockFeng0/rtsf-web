#! python3
# -*- encoding: utf-8 -*-
'''
Current module: tests.test_driver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      tests.test_driver,  v1.0 2018年8月20日
    FROM:   2018年8月20日
********************************************************************
======================================================================

Provide a function for the automation test

'''

import unittest,os
from rtsf.p_executer import TestRunner
from rtsf.p_report import HtmlReporter
from rtsf.p_testcase import TestCaseParser
from webuidriver.driver import LocalDriver 

case_file = r'data\test_case.yaml'


class TestTestRunner(unittest.TestCase):
    
    def test_run_and_gen_hetml_report(self):
        pass
        
if __name__ == "__main__":
#     unittest.main()
#     logger.setup_logger("debug")
#     runner = TestRunner(runner = Driver).run(r"C:\d_disk\auto\buffer\test\rtsf-http-test\.yaml")    
    runner = TestRunner(runner = LocalDriver).run(case_file)
    html_report = runner.gen_html_report()
    
    