#! python3
# -*- encoding: utf-8 -*-

import time
import unittest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
import webuidriver


class TestDriver(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        opt = webdriver.ChromeOptions()
        # 不加载图片,加快访问速度
        opt.add_argument('--blink-settings=imagesEnabled=false')

        # 无头模式，可不启用界面显示运行
        # opt.add_argument('--headless')

        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        opt.add_experimental_option('excludeSwitches', ['enable-automation'])
        # opt.add_experimental_option("debuggerAddress", "127.0.0.1:9999")
        # opt.add_argument('--proxy--server=127.0.0.1:8080')

        # 禁用浏览器正在被自动化程序控制的提示
        opt.add_argument('--disable-infobars')
        # 隐身模式（无痕模式）
        opt.add_argument('--incognito')

        cls.driver = webuidriver.Chrome(options=opt)
        cls.driver.get('http://www.baidu.com')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.close()
        cls.driver.quit()

    def test_is_selenium_object(self):
        # webuidriver.Chrome 是 webdriver.Chrome 的子类
        self.assertTrue(issubclass(webuidriver.Chrome, webdriver.Chrome))
        self.assertIsInstance(self.driver, webdriver.Chrome)

    def test_property_until_find(self):
        # default timeout=10, wait_displayed=False
        self.driver.until_find.element_by_id("kw", timeout=10, wait_displayed=True).send_keys("hello world.")

        # default index = 0, timeout = 10
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


if __name__ == "__main__":
    unittest.main()
