#! python3
# -*- encoding: utf-8 -*-
import time
from typing import Union
from webuidriver import Chrome,Firefox,Ie,Edge,Safari,Remote

class Page(object):
    def __init__(self, driver: Union[Firefox, Chrome, Ie, Edge, Safari, Remote]):
        self.driver = driver

    def find_element(self, *loc, **kwargs):
        _elm_find = self.driver.until_find._element(loc[0])
        return _elm_find(loc[1], **kwargs)

    def find_elements(self, *loc, **kwargs):
        _elm_find = self.driver.until_find._elements(loc[0])
        return _elm_find(loc[1], **kwargs)

    def _mark_element(self, elm, filename):
        """ 使用红框标记元素，并截图，该方法主要用于调试
        :param elm:
        :param filename:
        :return:
        """
        # 使用红框标记元素
        self.driver.execute_script("arguments[0].style.border='3px solid red'", elm)
        self.driver.save_screenshot(filename)

    def _requests_cookies(self, target_domain):
        """ 转换selenium cookie为 requests格式的字典cookie，并排除已过期的 Cookie
        :param target_domain: 保留的目标域名， 如：cpms.hq.cmcc
        """
        requests_cookies = {}
        current_timestamp = time.time()
        cookies_list = self.driver.get_cookies()

        for cookie in cookies_list:
            # 验证域名匹配（处理带.前缀的域名）
            cookie_domain = cookie.get('domain', '')
            domain_match = (
                    cookie_domain == target_domain or
                    cookie_domain == f".{target_domain}"
            )

            # 验证是否过期
            expiry = cookie.get('expiry')
            if expiry:
                expired = expiry < current_timestamp
            else:
                # 如果没有提供过期时间，假设不会过期（如会话 Cookie）
                expired = False

            # 添加未过期的目标域名 Cookie
            if domain_match and not expired:
                requests_cookies[cookie['name']] = cookie['value']

        # 添加日志用于调试
        # print(f"转换后的有效 Cookie 数量: {len(requests_cookies)}/{len(cookies_list)}")
        return requests_cookies