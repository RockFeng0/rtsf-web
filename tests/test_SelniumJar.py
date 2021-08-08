#! python3
# -*- encoding: utf-8 -*-

import unittest
from webuidriver.remote.SeleniumJar import SeleniumJar
from webuidriver.remote.SeleniumHatch import SeleniumHatch


class TestSeleniumJar(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        jar_path = r'D:\auto\buffer\test\test_rtsf_web\seleniumjar\selenium-server-standalone-3.14.0.jar'
        java_path = "java"
        cls.hub = SeleniumJar(jar_path, java_path).hub(4444)
        cls.node = SeleniumJar(jar_path, java_path).node(("", 5555), ("localhost", 4444))

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

        executors = SeleniumHatch.get_remote_executors("localhost", 4444)
        self.assertEqual(len(executors), 1)
        self.assertIn("5555", executors[0])
         
        self.node.re_start_server()
        self.assertEqual(self.node.is_runnnig(), True)
    
    
if __name__ == "__main__":
    unittest.main(verbosity=2)
