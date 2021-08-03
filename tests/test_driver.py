#! python3
# -*- encoding: utf-8 -*-


import unittest
from rtsf.p_executer import TestRunner
from rtsf.p_applog import logger
from webuidriver.driver import LocalDriver, RemoteDriver
from webuidriver.remote.SeleniumJar import SeleniumJar


class TestDriver(unittest.TestCase):
    
    def setUp(self):
        self.case_file = r'data\test_case.yaml'
        self.data_driver_case = r'data\data_driver.yaml'
        self.jar_path = r'D:\auto\buffer\test\test_rtsf_web\selenium-server-standalone-3.14.0.jar'
        self.java_path = "java"

    def test_LocalDriver(self):
        obj = LocalDriver()
        self.assertIsInstance(obj, LocalDriver)
        device_id, driver = obj.drivers[0][0], obj.drivers[0][1]
        self.assertEqual(device_id, "")
        driver.get('http://www.baidu.com')
        driver.close()
        driver.quit()

    def test_LocalDriver_to_be_runner(self):
        runner = TestRunner(runner = LocalDriver).run(self.case_file)
        html_report = runner.gen_html_report()
        print(html_report)
        self.assertIsInstance(html_report, (list, tuple))

    def test_RemoteDriver(self):
        hub = SeleniumJar(self.jar_path, self.java_path).hub(4444)
        hub.start_server()

        node = SeleniumJar(self.jar_path, self.java_path).node(5555, ("localhost", 4444))
        node.start_server()

        obj = RemoteDriver()
        device_id, driver = obj.drivers[0][0], obj.drivers[0][1]
        print("id:{0}, driver:{1}".format(device_id, driver))
        self.assertIn("wdhub", device_id)
        driver.get('http://www.baidu.com')
        driver.close()
        driver.quit()

        hub.stop_server()
        node.stop_server()

    def test_RemoteDriver_to_be_runner(self):
        
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
    # logger.setup_logger("debug")
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(TestDriver("test_LocalDriver"))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)    
