#! python3
# -*- encoding: utf-8 -*-

from selenium.webdriver import ChromeOptions


class ChromeArguments(ChromeOptions):
    HEADLESS = "--headless"  # 无界面模式
    NO_IMAGES = "--blink-settings=imagesEnabled=false"  # 禁用图片加载
    INCOGNITO = "--incognito"  # 隐身模式
    DISABLE_GPU = "--disable-gpu"  # 禁用gpu渲染
    FULL_SCREEN = "--start-fullscreen"  # 全屏启动
    KIOSK = "--kiosk"  # 全屏启动，无地址栏
    WINDOW_SIZE = "--window-size=1024,650"  # 置窗口尺寸(宽高)

    def __init__(self):
        super(ChromeArguments, self).__init__()





