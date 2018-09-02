#! python3
# -*- encoding: utf-8 -*-
'''
Current module: tests.test_SelniumJar

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      tests.test_SelniumJar,  v1.0 2018年8月27日
    FROM:   2018年8月27日
********************************************************************
======================================================================

Provide a function for the automation test

'''

import unittest
from webuidriver.remote.SeleniumJar import SeleniumJar

class TestSeleniumJar(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        jar_path =  r'D:\auto\buffer\test\test_rtsf_web\selenium-server-standalone-3.14.0.jar'
        java_path = "java"
        cls.hub = SeleniumJar(jar_path, java_path).hub(4444)
        cls.node = SeleniumJar(jar_path, java_path).node(5555,("localhost", 4444))
    
    @classmethod
    def tearDownClass(cls):
        cls.hub.stop_server()        
        cls.node.stop_server()
            
    def test_hub(self):
        self.hub.start_server()
        self.assertEqual(self.hub.is_runnnig(), True)
        
        self.hub.re_start_server()
        self.assertEqual(self.hub.is_runnnig(), True)
                
    def test_node(self):
        self.node.start_server()
        self.assertEqual(self.node.is_runnnig(), True)
         
        self.node.re_start_server()
        self.assertEqual(self.node.is_runnnig(), True)
    
    
if __name__ == "__main__":
    unittest.main(verbosity = 2)
    