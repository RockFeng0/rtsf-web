#! python3
# -*- encoding: utf-8 -*-
'''
Current module: webuidriver.driver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      webuidriver.driver,  v1.0 2018年8月20日
    FROM:   2018年8月20日
********************************************************************
======================================================================

Provide a function for the automation test

'''

from rtsf.p_executer import Runner
from rtsf.p_common import CommonUtils,ModuleUtils
from rtsf.p_exception import FunctionNotFound,VariableNotFound
from webuidriver.remote.SeleniumHatch import SeleniumHatch
from multiprocessing import Pool

class LocalDriver(Runner):      
    
    def __init__(self):
        self._Actions = ModuleUtils.get_imported_module("webuidriver.actions")
        
        self.driver = SeleniumHatch.gen_local_driver(browser = "chrome", capabilities = SeleniumHatch.get_remote_browser_capabilities(browser = "chrome", download_path=None, marionette = False))
    
    def run_test(self, testcase_dict):
        
        pool = Pool(len(drivers))
        # for i in executers:
            # result = pool.apply_async(runnCase, args=(params,));#异步
            # print result.get()
        pool.map(callable_function, drivers.items());#并行
        pool.close()
        pool.join()
        
    def case(self):
        parser = self.parser
        parser.bind_functions(ModuleUtils.get_callable_class_method_names(self._Actions.WebElement))
        parser.update_binded_variables(self._Actions.WebElement.glob)        
         
        case_name = testcase_dict["name"]                 
        self.tracer.start(self.proj_info["module"], case_name, testcase_dict.get("responsible","Administrator"), testcase_dict.get("tester","Administrator"))        
        self.tracer.section(case_name)
         
        try:
#             self.tracer.normal("**** bind glob variables")                
#             glob_vars = parser.eval_content_with_bind_actions(testcase_dict.get("glob_var",{}))
#             self.tracer.step("set global variables: {}".format(glob_vars))                
#             self._Actions.WebHttp.glob.update(glob_vars)            
#              
#             self.tracer.normal("**** bind glob regular expression")
#             globregx = {k: re.compile(v) for k,v in testcase_dict.get("glob_regx",{}).items()}
#             self.tracer.step("set global regular: {}".format(globregx))            
#             self._Actions.WebHttp.glob.update(globregx)
                             
            self.tracer.normal("**** precommand")
            precommand = testcase_dict.get("pre_command",[])    
            parser.eval_content_with_bind_actions(precommand)
            for i in precommand:
                self.tracer.step("{}".format(i))
             
            self.tracer.normal("**** steps")
            steps = testcase_dict["steps"]
            for step in steps:
                if not "webdriver" in step:
                    continue
                 
                by = parser.eval_content_with_bind_actions(step["webdriver"].get("by"))
                self.tracer.normal("preparing: by -> {}".format(by))
                
                value = parser.eval_content_with_bind_actions(step["webdriver"].get("value"))
                self.tracer.normal("preparing: value -> {}".format(value))
                
                index = parser.eval_content_with_bind_actions(step["webdriver"].get("index", 0))
                self.tracer.normal("preparing: index -> {}".format(index))
                
                timeout = parser.eval_content_with_bind_actions(step["webdriver"].get("timeout", 10))
                self.tracer.normal("preparing: timeout -> {}".format(timeout))                           
                
                prepare =parser.get_bind_function("Prepare")
                prepare(by = by, value = value, index = index, timeout = timeout)
                
                if not step["webdriver"].get("action"):
                    raise KeyError("webdriver.action")
                
                result = parser.eval_content_with_bind_actions(step["webdriver"]["action"])                
                if result == False:
                    self.tracer.fail(step["action"])
                else:
                    self.tracer.ok(step["action"])
                        
#                 resp_headers = parser.get_bind_function("GetRespHeaders")()
#                 self.tracer.step("response headers: \n\t{}".format(resp_headers))
             
#                 resp_text = parser.get_bind_function("GetRespText")()
#                 self.tracer.step(u"response body: \n\t{}".format(resp_text))                                 
            
            self.tracer.normal("**** postcommand")
            postcommand = testcase_dict.get("post_command", [])        
            parser.eval_content_with_bind_actions(postcommand)
            for i in postcommand:
                self.tracer.step("{}".format(i))
            
            self.tracer.normal("**** verify")
            verify = testcase_dict.get("verify",[])
            result = parser.eval_content_with_bind_actions(verify)
            for v, r in zip(verify,result):
                if r == False:
                    self.tracer.fail(u"{} --> {}".format(v,r))
                else:
                    self.tracer.ok(u"{} --> {}".format(v,r))
                        
        except KeyError as e:
            self.tracer.error("Can't find key[%s] in your testcase." %e)
        except FunctionNotFound as e:
            self.tracer.error(e)
        except VariableNotFound as e:
            self.tracer.error(e)
        except Exception as e:
            self.tracer.error("%s\t%s" %(e,CommonUtils.get_exception_error()))
        finally:
#             self.tracer.normal("globals:\n\t{}".format(parser._variables)) 
            self.tracer.stop()
         
    
        
        
        
            
            