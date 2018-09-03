# rtsf-web
 基于rtsf测试框架，关键字驱动Web UI层面，进行自动化的功能测试


## 编写测试用例，模板基于rtsf

> 变量引用-> $var    关键字(函数)引用-> ${function}

- 常量的定义， glob_var 和  glob_regx
- 模板常用的关键字，参见 [rtsf](https://github.com/RockFeng0/rtsf)介绍

### 基本用例

基本用例，是指没有分层的情况下，简单的测试用例

```
- project:
    name: xxx系统
    module: 登陆模块-功能测试
    
- case:
    # id 必填
    id: ATP-1
    # desc 必填
    desc: 测试用例-模板格式的设计-模板（全字段）
    
    # responsible 选填
    responsible: rockfeng0
    
    # tester 选填
    tester: rockfeng0
    
    # 定义正则表达式, 定义的字符串不会解析
    glob_regx:
        rex_title: '百度一下，你就知道'
    
    # 定义变量， 效果同 SetVar(name, value)
    glob_var:
        url1: https://www.baidu.com
        url2: https://www.sina.com
        
    # pre_command 选填
    pre_command:
        - ${NavigateTo($url1)}
        # - ${DyStrData("title", re.compile(rex_title))}
        # - ${VerifyTitle($title)}
        
    # steps 必填
    steps:        
        # webdriver 测试web ui 时使用
        
        - webdriver:
            action: ${NavigateTo($url2)}
            
        - webdriver:
            action: ${ScrollTo(0, 1000)}
        
        - webdriver:
            action: ${TimeSleep(1)}
        
        - webdriver:
            action: ${Refresh()}
        
        - webdriver:
            action: ${NewTab($url1)}
                
        # 在webdriver中，设置 SetControl参数，定位元素
        - webdriver:
            by: css selector
            value: '#kw'
            index: 0
            timeout: 10
            action: ${SendKeys(123)}
        
        - webdriver:
            action: ${TimeSleep(1)}
            
        # 直接使用 SetControl关键字，定位元素
        - webdriver:
            action: ${SetControl(by=css selector, value=#kw)}
        
        - webdriver:
            action: ${SendKeys(456)}
        
        - webdriver:
            action: ${SetControl(by=id, value=su)}
        
        - webdriver:
            action: ${DyAttrData(id_su_value, value)}
            
        - webdriver:
            action: ${TimeSleep(1)}
        
        - webdriver:
            action: ${WebClose()} 
                   
    # post_command 选填
    post_command:
        - ${WebQuit()}

```

### 分层用例

- 分层用例，是指模块功能测试的时候，对测试用例进行分层，最小的单元为api，其次为suite，最后组成用例
- 其存放路径、编写规则等，详见 [rtsf](https://github.com/RockFeng0/rtsf)相关介绍
- 示例可以，参见[rtsf-http](https://github.com/RockFeng0/rtsf-http)相关介绍


## 执行测试用例

> 执行有两个命令,  hdriver 或者   httpdriver

```
to write
```


## 测试报告及日志

> 执行结束后，测试用例所在路径，就是report生成的路径


## 基于rtsf，封装的关键字(内置函数)

```
to write
```

## 自定义，关键字(函数、变量)
> 在case同级目录中，创建  preference.py, 该文件所定义的 变量、函数，可以被动态加载和引用

执行用例的时候，可以使用 变量引用 或者关键字引用的方法，调用，自定义的函数和变量

```
# preference.py 示例

test_var = "hello rtsf."
def test_func():
    return "nihao rtsf."
 
```








 