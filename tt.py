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
from webuidriver.remote.SeleniumHatch import SeleniumHatch
from multiprocessing import Pool,freeze_support

class Test():
    def __init__(self):
        self.tracer = []
        
        
    def test(self):
#         return {"0":"1"}
#         return {"0":webdriver.Chrome()}

        executors = SeleniumHatch.get_remote_executors("localhost", 4444)                
        chrome_capabilities = SeleniumHatch.get_remote_browser_capabilities()
        return SeleniumHatch.gen_remote_driver(executors[0], chrome_capabilities)
        

    
class RunPool:
    @classmethod
    def Start(cls,callable_function,test):
        print("1",test)
        freeze_support()
        pool = Pool()
        # for i in executers:
            # result = pool.apply_async(runnCase, args=(params,));#异步
            # print result.get()
        result = pool.map(callable_function, {test:test.test()}.items());#并行
        pool.close()
        pool.join()
        
        return result


def case2(edriver):         
    exector,BROWSER = edriver[0],edriver[1]
    print("3",exector)
    print(BROWSER)        
    BROWSER.quit()
    exector.tracer = [1,2,3]
    return exector    
    
    

def simple_example_3():  
    te = Test()
    result = RunPool.Start(case2, te)
    print("2",te)
    print(te.tracer)
    print(result, result[0].tracer)
    
if __name__ == "__main__":
    simple_example_3()
    