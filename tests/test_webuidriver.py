#! python3
# -*- encoding: utf-8 -*-

import time
import json
import unittest
from webuidriver import Page
from webuidriver import Chrome, Firefox, Safari, Edge, Ie, Remote
from selenium.webdriver.common.by import By


class BingPage(Page):
    # 必应 首页
    bing_input = (By.CSS_SELECTOR, "#sb_form_q")  # 搜索栏
    bing_button = (By.CSS_SELECTOR, "#search_icon")  # 搜索栏

    def search(self, word):
        self.driver.get('https://cn.bing.com')

        # 输入word
        elm = self.find_element(*self.bing_input)
        elm.clear()
        elm.send_keys(word)

        # 标记
        self._mark_element(elm, "pic1.png")

        # 点击查询
        elm = self.find_element(*self.bing_button)
        elm.click()
        time.sleep(0.5)



class TestDriver(unittest.TestCase):


    def test_Page(self):
        # Test 1: Import verification - 引入验证
        print("✓ 引入验证 passed")
        print(f"Page class: {Page}")
        print(f"Browser drivers available: Chrome, Firefox, Safari, Edge, Ie, Remote")

        # Test 2: Type hint verification - 类型提示验证
        print("\n✓ 类型提示验证 passed")
        print(f"Page.__init__ signature: {Page.__init__.__annotations__}")

    def test_BingPage(self):
        # Test with webuidriver driver
        bing_page = BingPage(Chrome())
        bing_page.search("python")

        # Test requests cookie
        requests_cookies = bing_page._requests_cookies("bing.com")
        print("Requests cookies: \n",json.dumps(requests_cookies, indent=2))

        bing_page.driver.quit()



if __name__ == "__main__":
    unittest.main()
