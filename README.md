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
- 公共参数
这些参数为EasyZabbix这个项目下所有python脚本共享的(除了configtest.py校验脚本)

>`-h / --help`
显示帮助文档

>`-c / --config`
配置文件路径和文件名（配置文件与脚本在同级目录的话用相对路径，否则用绝对路径, 另外，如果不想每次执行脚本时都添加这个参数，你可以把配置文件放在当前用户家目录下命名为.zabbix.conf)  

>`-H / --hostname`
需要操作的主机名（支持多个主机名，但至少提供一个，主机名中间有空格的需要加上引号，如果主机不存在则会在脚本当前目录生成hosterror.log文件)  

>`-f / --file`
存储大量的主机名的文件（以行为单位，每行一个主机名。注意：-f和-H参数二者必须存在一个，但二者不能同时使用)

>`--version`
显示当前脚本的版本号

以上就是所有的脚本共有的参数了，个别脚本会有其他参数，见下面每个脚本的功能说明


