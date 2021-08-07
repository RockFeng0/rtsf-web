#! python3
# -*- encoding: utf-8 -*-

import time
import unittest
from webuidriver.remote.SeleniumHatch import SeleniumHatch
from webuidriver.remote.SeleniumJar import SeleniumJar
from selenium import webdriver


class TestSeleniumHatch(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        jar_path = r'D:\auto\buffer\test\test_rtsf_web\seleniumjar\selenium-server-standalone-3.14.0.jar'
        java_path = "java"
        cls.hub = SeleniumJar(jar_path, java_path).hub(4444)
        cls.node = SeleniumJar(jar_path, java_path).node(5555, ("localhost", 4444))
                    
    @classmethod
    def tearDownClass(cls): 
        try:       
            cls.hub.stop_server()        
            cls.node.stop_server()
        except:
            pass
    
    def test_gen_remote_driver(self):
        self.hub.start_server()
        self.node.start_server()
        
        executors = SeleniumHatch.get_remote_executors("localhost", 4444)
        self.assertIsInstance(executors, (tuple, list))
        
        chrome_capabilities = SeleniumHatch.get_remote_browser_capabilities()
        self.assertIsInstance(chrome_capabilities, dict)
        self.assertIn("ignore-certificate-errors", chrome_capabilities["goog:chromeOptions"]["excludeSwitches"])
        self.assertIn("enable-automation", chrome_capabilities["goog:chromeOptions"]["excludeSwitches"])
        
        driver = SeleniumHatch.gen_remote_driver(executors[0], chrome_capabilities)
        self.assertIsInstance(driver, webdriver.Remote)

        driver.get("http://www.baidu.com")
        time.sleep(1)
        driver.quit()
        
    def test_gen_local_driver(self):
        chrome_capabilities = SeleniumHatch.get_remote_browser_capabilities()
        self.assertIsInstance(chrome_capabilities, dict)
        self.assertIn("ignore-certificate-errors", chrome_capabilities["goog:chromeOptions"]["excludeSwitches"])
        self.assertIn("enable-automation", chrome_capabilities["goog:chromeOptions"]["excludeSwitches"])

        driver = SeleniumHatch.gen_local_driver(browser="chrome", capabilities=chrome_capabilities)
        self.assertIsInstance(driver, webdriver.Chrome)

        driver.get("http://www.baidu.com")
        time.sleep(1)
        driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)
    # suite = unittest.TestSuite()
    # suite.addTest(TestSeleniumHatch("test_gen_local_driver"))
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(suite)
