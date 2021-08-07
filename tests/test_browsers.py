#! python3
# -*- encoding: utf-8 -*-

import time
import unittest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException

import webuidriver
from webuidriver.chrome.options import ChromeArguments
from webuidriver.remote.SeleniumJar import SeleniumJar
from webuidriver.remote.SeleniumHatch import SeleniumHatch


class TestDriver(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.java_path = "java"
        cls.jar_path = r'D:\auto\buffer\test\test_rtsf_web\seleniumjar\selenium-server-standalone-3.14.0.jar'

        cls.opt = webuidriver.ChromeOptions()
        cls.opt.add_argument(ChromeArguments.NO_IMAGES)
        cls.opt.add_argument(ChromeArguments.HEADLESS)
        cls.opt.add_argument(ChromeArguments.INCOGNITO)
        cls.opt.add_argument(ChromeArguments.WINDOW_SIZE)
        cls.opt.add_argument(ChromeArguments.DISABLE_GPU)

    def test_webuidriver_chrome(self):
        self.driver = webuidriver.Chrome(options=self.opt)
        self.driver.get('http://www.baidu.com')
        time.sleep(1)

        # webuidriver.Chrome 是 webdriver.Chrome 的子类
        self.assertTrue(issubclass(webuidriver.Chrome, webdriver.Chrome))
        self.assertIsInstance(self.driver, webdriver.Chrome)

        self.assertTrue(issubclass(webuidriver.ChromeOptions, webdriver.ChromeOptions))

        self.driver.close()
        self.driver.quit()

    def test_webuidriver_remote(self):
        """ Selenium grid mode.
            You can use SeleniumJar to start service.
            Also, you can use command lines if you installed rtsf-web, like this:
            wrhub selenium-server-standalone-3.14.0.jar --port 4444
            wrnode selenium-server-standalone-3.14.0.jar --port 5555 --hub-ip 10.154.123.74 --hub-port 4444
        """

        hub = SeleniumJar(self.jar_path, self.java_path).hub(4444)
        hub.start_server()

        node = SeleniumJar(self.jar_path, self.java_path).node(5555, ("localhost", 4444))
        node.start_server()
        executors = SeleniumHatch.get_remote_executors("localhost", 4444)

        # self.driver = webuidriver.Remote(executor, options=self.opt) 与下面语句效果是一样的
        self.driver = webuidriver.Remote(executors[0], desired_capabilities=self.opt.to_capabilities())

        self.driver.get('http://www.baidu.com')
        time.sleep(1)

        # webuidriver.Remote 是 webdriver.Chrome 的子类
        self.assertTrue(issubclass(webuidriver.Chrome, webdriver.Remote))
        self.assertIsInstance(self.driver, webdriver.Remote)

        self.driver.close()
        self.driver.quit()

        hub.stop_server()
        node.stop_server()

    def test_property_until_find(self):

        self.driver = webuidriver.Chrome(options=self.opt)
        self.driver.get('http://www.baidu.com')

        # default timeout=10, wait_displayed=False
        self.driver.until_find.element_by_id("kw", timeout=10, wait_displayed=True).send_keys("hello world.")

        # elements_by_xxx, 默认返回 第一个元素，超时10秒
        try:
            self.driver.until_find.elements_by_css_selector("input.bg.s_btn.not_found", timeout=2)
        except Exception as err:
            self.assertTrue(err, TimeoutException)

        try:
            self.driver.until_find.elements_by_css_selector("input.bg.s_btn", index=100)
        except Exception as err:
            self.assertIsInstance(err, IndexError)

        elm = self.driver.until_find.elements_by_css_selector("input")
        self.assertFalse(isinstance(elm, list))
        self.assertTrue(isinstance(elm, WebElement))

        self.driver.until_find.elements_by_css_selector("input.bg.s_btn").click()

        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
