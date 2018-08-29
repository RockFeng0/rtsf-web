#! python3
# -*- encoding: utf-8 -*-
'''
Current module: tt

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      tt,v 1.0 2018年8月21日
    FROM:   2018年8月21日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
 
from selenium import webdriver

class Driver(object):
    def __init__(self):
        self.__driver = None
    
    @property
    def driver(self):
        return self.__driver
    
    @driver.setter
    def driver(self, driver_object):
#         if not isinstance(driver_object, (webdriver.Remote, webdriver.Chrome, webdriver.Firefox)):
#             raise TypeError('{} must be an instatnce in (webdriver.Remote, webdriver.Chrome, webdriver.Firefox)'.format(driver_object))
        self.__driver=driver_object
        
class Ttt(Driver):
    
    @classmethod
    def test(cls):
        cls.driver = 2
        print(cls.driver)
        
    @classmethod
    def test2(cls):
        print(cls.driver)
        
    
if __name__ == "__main__":
    print(Driver().driver)