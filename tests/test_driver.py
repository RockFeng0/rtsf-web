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

import unittest
from rtsf.p_executer import TestRunner
from rtsf.p_applog import logger
from webuidriver.driver import LocalDriver ,RemoteDriver
from webuidriver.remote.SeleniumJar import SeleniumJar

class TestDriver(unittest.TestCase):
    
    def setUp(self):
        self.case_file = r'data\test_case.yaml'
        self.data_driver_case = r'data\data_driver.yaml'
        self.jar_path =  r'D:\auto\buffer\test\test_rtsf_web\selenium-server-standalone-3.14.0.jar'
        self.java_path = "java"
    
    def test_LocalDriver(self):
        runner = TestRunner(runner = LocalDriver).run(self.case_file)
        html_report = runner.gen_html_report()
        print(html_report)
        self.assertIsInstance(html_report, (list, tuple))
    
    def test_RemoteDriver(self):        
        
        hub = SeleniumJar(self.jar_path, self.java_path).hub(4444)
        hub.start_server()
        
        node = SeleniumJar(self.jar_path, self.java_path).node(5555,("localhost", 4444))
        node.start_server()        
        
        runner = TestRunner(runner = RemoteDriver).run(self.case_file)
        html_report = runner.gen_html_report()
        print(html_report)
        self.assertIsInstance(html_report, (list, tuple))
        
        hub.stop_server()        
        node.stop_server()
        
    def test_LocalDriver_data_driver(self):
        runner = TestRunner(runner = LocalDriver).run(self.data_driver_case)
        html_report = runner.gen_html_report()
        print(html_report)
        self.assertIsInstance(html_report, (list, tuple))
        
if __name__ == "__main__":
#     logger.setup_logger("debug")
#     unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(TestDriver("test_LocalDriver_data_driver"))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)    
    
    
    