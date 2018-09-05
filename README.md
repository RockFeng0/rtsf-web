# rtsf-web
 基于rtsf测试框架和selenium程序框架，关键字驱动Web UI层面，进行自动化的功能测试

## 编写测试用例，模板基于rtsf

> 变量引用-> $var    关键字(函数)引用-> ${function}

- 常量的定义， glob_var 和  glob_regx
- 模板常用的关键字，参见 [rtsf](https://github.com/RockFeng0/rtsf)介绍

### 基本用例

基本用例，是指没有分层的情况下，简单的测试用例

```
# test_case.yaml
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

1. 执行前，注意下selenium的执行环境， rtsf-web限定了两中浏览器(chrome和firefox)
2. 谷歌浏览器，按照selenium的文档介绍，自行下载chromedriver.exe并配置
3. 火狐浏览器，按照selenium的文档介绍，版本高的，自行下载geckodriver.exe并配置

> 执行测试用例，有个命令：  wldriver 和 wrdriver

### wldriver(web local driver)本地执行
本地执行测试用例，是指直接使用webdriver中各个浏览器的驱动，比如webdriver.Chrome等

查看帮助: wldriver -h
选填：
- 设置浏览器(chrome、firefox),默认是谷歌浏览器:      --browser chrome
- 设置浏览器下载文件的路径，默认值是浏览器的设置:    --download-path c:\downloads
- 设置火狐是否使用geckodriver.exe,默认值是False:     --marionette False

```
# run web local case
wldriver --browser chrome C:\f_disk\BaiduNetdiskDownload\rtsf-web\tests\data\test_case.yaml
```

### wrdriver(web remote driver)远程执行，即selnium grid分布式模式
该模式，遵循selnium grid要求，需要开启hub和node, rtsf-web提供两个命令: wrhub和wrnode

#### 开启hub
简单理解下hub, 玩局域网游戏，我们先要建立主机，那么hub可以理解为主机的概念

查看帮助: wrhub -h
选填：
- 设置HUB监听端口,默认是4444:       --port 4444
- 指定java.exe路径,默认(已配置java环境变量):    --java-path java

```
# start hub A: 192.168.0.1
wrhub c:\selenium-server-standalone-3.14.0.jar --port 4444 --java-path C:\tmp\Java\jdk1.8.0_161\bin\java.exe
```

#### 开启node
简单理解下node, 游戏主机创建好，玩家需要加入，那么node可以理解为加入主机的玩家

查看帮助: wrnode -h
选填：
- 设置NODE监听端口,默认是5555:       --port 5555
- 执行连接hub的ip,默认是localhost:   --hub-ip 127.0.0.1
- 执行连接hub的,默认是4444:          --hub-port 4444
- 指定java.exe路径,默认(已配置java环境变量):    --java-path java
  
```
# start node B: 192.168.0.1     这个node机器的ip跟hub A一样，主机也可以是玩家
wrnode c:\selenium-server-standalone-3.14.0.jar --port 5555 --hub-ip 192.168.0.1 --hub-port 4444 --java-path C:\tmp\Java\jdk1.8.0_161\bin\java.exe

# start node C: 192.168.0.2
wrnode c:\selenium-server-standalone-3.14.0.jar --port 5555 --hub-ip 192.168.0.1 --hub-port 4444 --java-path C:\tmp\Java\jdk1.8.0_161\bin\java.exe
```

#### 执行分布式测试
远程执行测试用例，也就是selnium grid分布式执行测试用例，是指使用webdriver.Remote驱动各个浏览器进行测试
简单理解下，创建了主机，玩家也上线了，wrdriver将指定的游戏异步发送给这些玩家

查看帮助: wrdriver -h
选填：
- 设置浏览器(chrome、firefox),默认是谷歌浏览器:      --browser chrome
- 设置浏览器下载文件的路径，默认值是浏览器的设置:    --download-path c:\downloads
- 设置火狐是否使用geckodriver.exe,默认值是False:     --marionette False
- 设置HUB IP,默认是localhost:    --ip 127.0.0.1
- 设置HUB PORT,默认是4444:       --port 4444

```
# run web remote case.  简单理解， 已连接上主机的玩家，会接收到test_case游戏
wrdriver C:\f_disk\BaiduNetdiskDownload\rtsf-web\tests\data\test_case.yaml --browser chrome --ip 192.168.0.1 --port 4444
```

## 测试报告及日志

> 执行结束后，测试用例所在路径，就是report生成的路径


## 封装的关键字(内置函数)

### 浏览器相关操作

Web functions | 参数介绍 | 描述
--------------|----------|----
AlertAccept()        | |点击alert弹窗的Accept(确定)
AlertDismiss()       | |点击alert弹窗的Dismiss(取消)
AlertSendKeys(value) | |向alert弹窗中输入信息
Back()               | |浏览器后退
Forward()            | |浏览器前进
IESkipCertError()    | |IE Skip SSL Cert Error
Js(script)           | |浏览器执行js脚本
Maximize()           | |浏览器最大化
NavigateTo(url)      | |浏览器打开url
NewTab()             | |浏览器新开标签页，并将所有焦点指向该标签页
PageSource()         | |当前页面源码
Refresh()            | |浏览器刷新当前页面
ScreenShoot(pic_path)| |截图当前页面，并为pic_path
ScrollTo(x,y)        | |移动滚动条至(x,y),如下，X-Y-top :  ScrollTo("0","0"); X-bottom:  ScrollTo("10000","0");Y-bottom:  ScrollTo("0","10000")
SetWindowSize(width, height)| |设置浏览器窗口大小
SwitchToAlert()             | |切换浏览器焦点至alert弹窗
SwitchToDefaultFrame()      | |切换浏览器焦点至默认frame框, 比如打开的页面有多个iframe的情况
SwitchToDefaultWindow()     | |切换浏览器焦点至默认window窗,比如多个标签页窗的情况
SwitchToNewFrame(frame_name)| |切换浏览器焦点至frame_name框
SwitchToNewWindow()         | |切换浏览器焦点至新window窗
WebClose()                  | |关闭浏览器当前窗口
WebQuit()                   | |Quits the driver and closes every associated window.


## 自定义，关键字(函数、变量)
> 在case同级目录中，创建  preference.py, 该文件所定义的 变量、函数，可以被动态加载和引用

执行用例的时候，可以使用 变量引用 或者关键字引用的方法，调用，自定义的函数和变量

```
# preference.py 示例

test_var = "hello rtsf."
def test_func():
    return "nihao rtsf."
 
```








 