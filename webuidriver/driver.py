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
from rtsf.p_common import CommonUtils,ModuleUtils,FileSystemUtils
from rtsf.p_exception import FunctionNotFound,VariableNotFound
from webuidriver.remote.SeleniumHatch import SeleniumHatch
from functools import partial
import multiprocessing, re

def eval_case(testcase_dict, parser, tracer, proj_info_module, driver):
    print(testcase_dict, parser, tracer, proj_info_module, driver)

        

        
class Driver(Runner):      
    
    def __init__(self):
        #self._Actions = ModuleUtils.get_imported_module("webuidriver.actions")
        self.drivers = []        
    
    def run_test(self, testcase_dict):
        multiprocessing.freeze_support()
        pool = multiprocessing.Pool()        
        tracers = pool.map(partial(self._eval_case, testcase_dict), self.drivers)
        pool.close()
        pool.join()
        self.tracer = tracers[0]
    
    def _eval_case(self, testcase_dict, driver):
        parser = self.parser
        tracer = self.tracer
        
        _Actions = ModuleUtils.get_imported_module("webuidriver.actions")
        _Actions.Web.driver = driver
        
        functions = {}
        web_functions = ModuleUtils.get_callable_class_method_names(_Actions.Web)
        web_element_functions = ModuleUtils.get_callable_class_method_names(_Actions.WebElement)
        web_context_functions = ModuleUtils.get_callable_class_method_names(_Actions.WebContext)
        web_wait_functions = ModuleUtils.get_callable_class_method_names(_Actions.WebWait)
        web_verify_functions = ModuleUtils.get_callable_class_method_names(_Actions.WebVerify)
        web_actions_functions = ModuleUtils.get_callable_class_method_names(_Actions.WebActions)
        functions.update(web_functions)
        functions.update(web_element_functions)
        functions.update(web_context_functions)
        functions.update(web_wait_functions)
        functions.update(web_verify_functions)
        functions.update(web_actions_functions)   
        parser.bind_functions(functions)
        parser.update_binded_variables(_Actions.WebContext.glob)        
         
        case_name = testcase_dict["name"]
        
        ###  to change tracer
        tracer.start(self.proj_info["module"], case_name, testcase_dict.get("responsible","Administrator"), testcase_dict.get("tester","Administrator"))        
        tracer.section(case_name)
        
        try:
            tracer.normal("**** bind glob variables")                
            glob_vars = parser.eval_content_with_bind_actions(testcase_dict.get("glob_var",{}))
            tracer.step("set global variables: {}".format(glob_vars))                
            _Actions.WebContext.glob.update(glob_vars)            
             
            tracer.normal("**** bind glob regular expression")
            globregx = {k: re.compile(v) for k,v in testcase_dict.get("glob_regx",{}).items()}
            tracer.step("set global regular: {}".format(globregx))            
            _Actions.WebContext.glob.update(globregx)
                             
            tracer.normal("**** precommand")
            precommand = testcase_dict.get("pre_command",[])    
            parser.eval_content_with_bind_actions(precommand)
            for i in precommand:
                tracer.step("{}".format(i))
             
            tracer.normal("**** steps")
            steps = testcase_dict["steps"]
            for step in steps:
                print("---")            
                if not "webdriver" in step:
                    continue
                
                if not step["webdriver"].get("action"):
                    raise KeyError("webdriver.action")            
                
                print(step)
                if step["webdriver"].get("by"):
                    by = parser.eval_content_with_bind_actions(step["webdriver"].get("by"))
                    tracer.normal("preparing: by -> {}".format(by))
                    
                    value = parser.eval_content_with_bind_actions(step["webdriver"].get("value"))
                    tracer.normal("preparing: value -> {}".format(value))
                    
                    index = parser.eval_content_with_bind_actions(step["webdriver"].get("index", 0))
                    tracer.normal("preparing: index -> {}".format(index))
                    
                    timeout = parser.eval_content_with_bind_actions(step["webdriver"].get("timeout", 10))
                    tracer.normal("preparing: timeout -> {}".format(timeout))                           
                
                    prepare =parser.get_bind_function("SetControl")
                    prepare(by = by, value = value, index = index, timeout = timeout)
                                
                result = parser.eval_content_with_bind_actions(step["webdriver"]["action"])
                print(":",result)           
                if result == False:
                    tracer.fail(step["webdriver"]["action"])
                else:
                    tracer.ok(step["webdriver"]["action"])
                        
            tracer.normal("**** postcommand")
            postcommand = testcase_dict.get("post_command", [])        
            parser.eval_content_with_bind_actions(postcommand)
            for i in postcommand:
                tracer.step("{}".format(i))
            
            tracer.normal("**** verify")
            verify = testcase_dict.get("verify",[])
            result = parser.eval_content_with_bind_actions(verify)
            for v, r in zip(verify,result):
                if r == False:
                    tracer.fail(u"{} --> {}".format(v,r))
                else:
                    tracer.ok(u"{} --> {}".format(v,r))
                        
        except KeyError as e:
            tracer.error("Can't find key[%s] in your testcase." %e)
        except FunctionNotFound as e:
            tracer.error(e)
        except VariableNotFound as e:
            tracer.error(e)
        except Exception as e:
            tracer.error("%s\t%s" %(e,CommonUtils.get_exception_error()))
        finally:
    #             tracer.normal("globals:\n\t{}".format(parser._variables)) 
            tracer.stop()
        return tracer         
            
class LocalDriver(Driver):
    
    def __init__(self):
        super(Driver, self).__init__()
        
        self.drivers = [SeleniumHatch.gen_local_driver(browser = "chrome", capabilities = SeleniumHatch.get_remote_browser_capabilities(browser = "chrome", download_path=None, marionette = False))]
        print(self.drivers)
        #self._Actions = ModuleUtils.get_imported_module("webuidriver.actions")
#         self.drivers = [1,2,3,4]
        
class RemoteDriver(Driver):
    
    def __init__(self):
        super(Driver, self).__init__()
        executors = SeleniumHatch.get_remote_executors("localhost", 4444)
        self._device_id = FileSystemUtils.get_legal_filename(executors[0])
        chrome_capabilities = SeleniumHatch.get_remote_browser_capabilities(browser = "chrome", download_path = None, marionette = False)
        self.drivers = [SeleniumHatch.gen_remote_driver(executor, chrome_capabilities) for executor in executors]
    
            