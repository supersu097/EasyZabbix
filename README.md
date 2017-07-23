###EasyZabbix

This project learns from [zabbix-gnomes](https://github.com/q1x/zabbix-gnomes).Thanks!!!  
I rewrite the argument parsing and implement some bugs(bug as feature:-D) base on the project requirements of our team.   
欢迎有需要的小伙伴们fxxk and star →_→

----------
#### 1. 解决第三方依赖
```
sudo pip install requests
sudo pip install pyzabbix
```
#### 2. 编写登录验证配置文件
- 创建登录验证要用的配置文件,配置文件采用ini格式,  
必须包含一个名为[Zabbix API]的section,创建一个名为
`.zabbix.conf`配置文件示例如下:  
```
[Zabbix API]
username=Admin  
password=zabbix  
api=https://yourcompany.com/api_jsonrpc.php
no_verify=false
PS:用户名、密码以及zabbix前端网址要修改为自己公司的
```

- 验证是否配置成功
在EasyZabbix这个项目的目录下执行如下命令(配置文件路径换成自己的):  
`./configtest.py -c ~/.zabbix.conf`  
说明：-c参数后面跟的是我当前的配置文件,如果最后返回`Check success`，说明登录验证的配置成功了，没有看到这个消息的，要根据脚本打印的异常信息自己判断是什么情况了，一般来说有网络问题(在家使用的话要登录公司VPN)，账号密码问题，然后再核对一下配置文件基本就可以解决了。
    
#### 3. 参数及功能说明
- **公共参数**  
这些参数为EasyZabbix这个项目下所有python脚本共享的(除了configtest.py校验脚本)

>`-h / --help`
显示帮助文档

>`-c / --config`
配置文件路径和文件名（配置文件与脚本在同级目录的话用相对路径，否则用绝对路径, 另外，如果不想每次执行脚本时都添加这个参数，你可以把配置文件放在当前用户家目录下命名为.zabbix.conf)  

>`-H / --hostname`
需要操作的主机名（支持多个主机名，但至少提供一个，主机名中间有空格的需要加上引号，如果主机不存在则会在脚本当前目录生成hostnotfind.log文件)  

>`-f / --file`
存储大量的主机名的文件（以行为单位，每行一个主机名。注意：-f和-H参数二者必须存在一个，但二者不能同时使用)

>`--version`
显示当前脚本的版本号

以上就是所有的脚本共有的参数了，个别脚本会有其他参数，见下面每个脚本的功能说明

- **功能说明**

>`configtest.py`  
用来测试登录验证配置文件是否正确配置

>`deletehost.py`  
用来批量删除不需要监控的主机（当然也可以只删除一个）

>`disablemonitor.py`  
用来批量关闭不需要监控的主机（当然也可以关闭一个，如果向该脚本传递-e或者--enable参数，将会批量开启主机的监控）

>`tmplunlink.py`  
用来批量unlink掉该主机下的所有模板同时清除其所属的所有实例(补充：比如item，trigger)，详见此处[zabbix官方文档](https://www.zabbix.com/documentation/2.2/manual/config/templates/linking)最后一行。ps：这里单独unlink一个模板的参数已经添加在了代码里面，但是功能还没有实现，以后有时间了可以实现下，或者大家谁看到后实现一下这个功能然后提个PR是很欢迎的。。这个功能最好也支持unlink个多个主机的同一个模板（这个功能的实现可以参考下面的<其他功能扩展>这个section），用来应对大面积出现的因为模板设置的问题而引起的报警报警洪流。

>`disablemonitor.py`  
这个脚本打算用来批量关闭多个主机的同一个触发器的报警，平常在工作中经常遇到salt-minion相关的报警洪流，感觉暂时屏蔽了报警用处不大，最后最好还是要去用salt刷配置来解除报警比较好。不过也有多个主机上的某个service提示down了，直接unlink模板因为还有其他item要监控，不能这样做，产研一时半会搞不定，zabbix一直报警，leader会看报警量，这时候后还是有必要暂时屏蔽下的，公司有实现snooze功能也有web管理界面，但是没有看到可以批量操作的功能，像service down掉的情况最好还是用snooze比较好，disable的话万一后面忘记enable了就不好了。对了，这个脚本也只是把参数解析写好了，具体是disable掉还是snooze掉报警的功能还没有写。

#### **其他功能扩展**
这里以还没有实现功能的`disablemonitor.py`为例，脚本部分内容如下：
```python
import argparse #导入python官方自带命令行参数解析标准库
from core import parent_parser 
"""导入父解析器模块，可以使脚本共享
很多步骤3中的公共参数，可以减少每个
功能脚本的代码冗余"""
from core import common #封装的一些工具函数
child_parser = argparse.ArgumentParser(
    parents=[parent_parser.parser],#继承父解析器的paser对象
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Description:disable one trigger for many hosts...',
	#我们主要更改这个参数，用来告知用户这个脚本的功能 
    epilog="""%s %s """ % parent_parser.parent_usage())

child_parser.add_argument(
    '-t','--triggerid',
    help='The triggerid you wanna disable',
    type=int
)#调用子解析器的add_argument方法添加参数
zapi = common.getzapi(child_parser)#进行登录验证，获取zabbix api 对象
args = common.args_parser(child_parser)#进行参数解析
```

下面我们来看一下，仅仅是添加了上面这几行代码，我们可以达到的运行效果：
```
$ ./disabletrigger.py
usage: disabletrigger.py [-h] [-c CONFIG] [--version]
                         (-H HOSTNAME [HOSTNAME ...] | -f FILE) [-e]
                         [-t TRIGGERID]

Description:disable one trigger for many hosts...

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file location (defaults to $HOME/.zbx.conf)
  --version             show program's version number and exit
  -H HOSTNAME [HOSTNAME ...], --hostname HOSTNAME [HOSTNAME ...]
                        One or more hostname you wanna do sth,if hostname has
                        whitespace,pls use quotes to it!
  -f FILE, --file FILE  Many hostname in file,notice that one line one
                        hostname
  -e, --enable          Enable trigger...
  -t TRIGGERID, --triggerid TRIGGERID
                        The triggerid you wanna disable

Easy zabbix tools!!!

This program can use .ini style configuration files to retrieve the needed
API connection information.To use this type of storage, create a conf file
(the default is $HOME/.zbx.conf) that contains at least the [Zabbix API]
section and any of the other parameters:
[Zabbix API]
username=yourusername
password=yourpassword
api=https://your-zabbix-frontend-url/api_jsonrpc.php
no_verify=flase

Any question can contact with me at lin.gan@ele.me!
GayHub repository(:-D at https://github.com/supersu097/EasyZabbix
welcome to fxxk and star!
Finally,thank the open project at https://github.com/q1x/zabbix-gnomes!!!

Notice:
The options of -H and -f only allow one!!!
[Errno 2] No such file or directory: '/Users/Terminator./zabbix.conf'%
```

最后说一下，上面这些代码只是导入了core目录下的两个模块，一个是父解析器模块parent_parser.py，
一个是common.py模块封装了很多工具函数，然后添加了这个功能脚本特有的一些参数，之后进行登录验证获取zabbix api   对象和参数解析拿到所有命令行中用户传进来的参数列表对象，有了这两个对象大家就可以按照自己的需求来编写一些函数去实现了，
具体的过程大家可以参考下这个项目的其他功能脚本。
