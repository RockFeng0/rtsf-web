#! python3
# -*- encoding: utf-8 -*-

import os
from selenium.webdriver import ChromeOptions


class ChromeArguments(object):
    HEADLESS = "--headless"  # 无界面模式
    NO_IMAGES = "--blink-settings=imagesEnabled=false"  # 禁用图片加载
    INCOGNITO = "--incognito"  # 隐身模式
    DISABLE_GPU = "--disable-gpu"  # 禁用gpu渲染
    FULL_SCREEN = "--start-fullscreen"  # 全屏启动
    KIOSK = "--kiosk"  # 全屏启动，无地址栏
    WINDOW_SIZE = "--window-size=1024,650"  # 置窗口尺寸(宽高)


class ChromeExperiments(object):
    EXCLUDE_SWITCHES = {
        "name": "excludeSwitches",
        "value": [
            "ignore-certificate-errors",  # 忽略证书错误
            "enable-automation",  # 防止网站识别检测到Selenium爬虫代码
        ]
    }

    PREFS = {
        "name": "prefs",
        "value": {
            "download.default_directory": "",  # 设置下载路径
            "profile.default_content_settins.popups": 0,  # 设置为0禁止弹出窗口
        }
    }

    @classmethod
    def preferences(cls, download_path):
        prefs = {
            "name": "prefs",
            "value": {
                "download.default_directory": "",  # 设置下载路径
                "profile.default_content_settins.popups": 0,  # 设置为0禁止弹出窗口
            }
        }

        if os.path.isdir(download_path):
            prefs["value"]["download.default_directory"] = download_path
            return prefs
        else:
            raise ValueError("Download path is not a valid directory path.")


class Options(ChromeOptions):

    def __init__(self, download_path=None):
        super(ChromeOptions, self).__init__()

        self.add_experimental_option(
            ChromeExperiments.EXCLUDE_SWITCHES["name"], ChromeExperiments.EXCLUDE_SWITCHES["value"]
        )

        if os.path.isdir(download_path):
            ChromeExperiments.PREFS["value"]["download.default_directory"] = download_path
            self.add_experimental_option(
                ChromeExperiments.PREFS["name"], ChromeExperiments.PREFS["value"]
            )

