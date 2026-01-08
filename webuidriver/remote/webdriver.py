#! python3
# -*- encoding: utf-8 -*-

from webuidriver.support.wait_until import WaitUntil
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver


class WebDriver(RemoteWebDriver, WaitUntil):
    def __init__(self, *args, **kwargs):
        RemoteWebDriver.__init__(self, *args, **kwargs)
        WaitUntil.__init__(self)
