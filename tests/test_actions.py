#! python3
# -*- encoding: utf-8 -*-
'''
Current module: tests.test_actions

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      tests.test_actions,  v1.0 2018年8月22日
    FROM:   2018年8月22日
********************************************************************
======================================================================

Provide a function for the automation test

'''

import unittest,os,re

from webuidriver.actions import Web, WebElement, WebActions, WebContext, WebVerify, WebWait
from webuidriver.remote.SeleniumHatch import SeleniumHatch
from rtsf.p_common import ModuleUtils
import time

class TestActions(unittest.TestCase):
    
    def setUp(self):
        self.driver = Web.driver = SeleniumHatch.gen_local_driver("chrome", SeleniumHatch.get_remote_browser_capabilities("chrome"))        
        Web.NavigateTo('https://www.baidu.com')
        
        self.test_tmp_path = "./data/test_tmp"
        if not os.path.exists(self.test_tmp_path):
            os.makedirs(self.test_tmp_path)
        
    def tearDown(self):
        WebWait.TimeSleep(1)
        Web.WebQuit()
    
    def test_WebWait(self):
        WebWait.SetControl(by = "id", value = 'kw', index = 0, timeout = 5)
        self.assertEqual(WebWait.TimeSleep(1), None)
        self.assertEqual(WebWait.WaitForDisappearing(), False)
        self.assertEqual(WebWait.WaitForAppearing(), True)
        self.assertEqual(WebWait.WaitForVisible(), True)
    
    def test_WebElement(self):
        control = {"by":"111", "value" : "!!!", "index":22, "timeout":10}
        WebElement.SetControl(**control)
        self.assertEqual(WebElement.GetControl(), control)
        
        WebElement.SetControl(index = 0)
        self.assertEqual(WebElement.GetControl().get("index"), 0)
    
    def test_WebContext(self):
        url = "https://www.baidu.com"
        WebContext.SetVar("url", url)        
        self.assertEqual(WebContext.GetVar("url"), url)
        
        Web.NewTab(url)
        
        title = "百度一下，你就知道"
        WebContext.DyStrData("title", re.compile(title))        
        
        WebElement.SetControl(by = "id", value = "su")        
        WebContext.DyAttrData("su", "value")        
        
        Web.NavigateTo("http://bztest.djtest.cn/background/pass/247686389303191")        
        WebContext.DyJsonData("desc", "desc")
        
        self.assertEqual(WebContext.glob, {'url': 'https://www.baidu.com', 'title': '百度一下，你就知道', 'su': '百度一下', 'desc': '成功'})        
        Web.WebClose()
    
    def test_WebVerify(self):
        Web.NewTab('https://www.baidu.com')
        
        self.assertEqual(WebVerify.VerifyURL("https://www.baidu.com/"), True)
        self.assertEqual(WebVerify.VerifyTitle("百度一下，你就知道"), True)
        
        WebElement.SetControl(by = "id", value = "su", index = 0, timeout = 10)
        self.assertEqual(WebVerify.VerifyElemAttr("value", "百度一下"), True)
        self.assertEqual(WebVerify.VerifyElemCounts(1), True)
        self.assertEqual(WebVerify.VerifyElemEnabled(), True)
        self.assertEqual(WebVerify.VerifyElemNotEnabled(), False)
        self.assertEqual(WebVerify.VerifyElemVisible(), True)
        self.assertEqual(WebVerify.VerifyElemNotVisible(), False)
        
        WebElement.SetControl(by = "id", value = "form")
        self.assertEqual(WebVerify.VerifyElemInnerHtml("百度一下"), True)        
        Web.WebClose()
            
    def test_Web(self):
        Web.NewTab('https://www.sina.com.cn')        
        Web.Maximize()
        self.assertEqual(WebVerify.VerifyURL("https://www.sina.com.cn/"), True)
        WebWait.TimeSleep(1)
        
        Web.SetWindowSize(500, 500)
        Web.ScrollTo(0, 10000)
        WebWait.TimeSleep(1)
          
        Web.Refresh()
        Web.NavigateTo("https:/www.baidu.com")
        self.assertEqual(WebVerify.VerifyTitle("百度一下，你就知道"), True)
        WebWait.TimeSleep(1)
          
        Web.Back()
        WebWait.TimeSleep(1)
          
        Web.Forward()
        WebWait.TimeSleep(1)
        
        p = os.path.join(self.test_tmp_path, "t.png")
        Web.ScreenShoot(p)
        self.assertEqual(os.path.isfile(p), True)      
        
        Web.WebClose()
        m = re.search("百度一下，你就知道", Web.PageSource())
        self.assertIsNotNone(m)
    
    def test_WebAction(self):
        Web.NavigateTo('https:/www.sina.com')
        Web.ScrollTo(0, 1000)
        WebWait.TimeSleep(1)
        Web.Refresh()
        
        Web.NewTab('https://www.baidu.com')
        WebActions.SetControl(by = "css selector", value = "#kw")
        WebActions.SendKeys("123456")
        WebWait.TimeSleep(1)
        Web.WebClose()
    
    def test_WebAction_rtsf(self):  
        Actions = ModuleUtils.get_imported_module("webuidriver.actions")
        Actions.Web.driver = self.driver
            
        functions = {}
        web_functions = ModuleUtils.get_callable_class_method_names(Actions.Web)
        web_element_functions = ModuleUtils.get_callable_class_method_names(Actions.WebElement)
        web_context_functions = ModuleUtils.get_callable_class_method_names(Actions.WebContext)
        web_wait_functions = ModuleUtils.get_callable_class_method_names(Actions.WebWait)
        web_verify_functions = ModuleUtils.get_callable_class_method_names(Actions.WebVerify)
        web_actions_functions = ModuleUtils.get_callable_class_method_names(Actions.WebActions)
        functions.update(web_functions)
        functions.update(web_element_functions)
        functions.update(web_context_functions)
        functions.update(web_wait_functions)
        functions.update(web_verify_functions)
        functions.update(web_actions_functions)  
        self.assertNotEqual(functions, {})        
        
        print(functions)
        functions.get("NavigateTo")("http://www.baidu.com")
        functions.get("SetControl")(by = 'id', value = "kw")
        functions.get("SendKeys")(123456)
        time.sleep(1)
        functions.get("WebClose")()
        functions.get("WebQuit")()
        
    
    
if __name__ == "__main__":
    unittest.main(verbosity=2)

#     suite = unittest.TestSuite()
# #     suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestActions))
#     suite.addTest(TestActions("test_WebAction_rtsf"))    
#     runner = unittest.TextTestRunner(verbosity=2)
#     runner.run(suite)

    