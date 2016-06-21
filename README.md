###EasyZabbix
This project learns from [zabbix-gnomes](https://github.com/q1x/zabbix-gnomes).Thanks!!!
I rewrite the argument parsing and implement some bugs(bug as feature:-D) base on the project requirements of our team.  
欢迎有需要的小伙伴们fxxk and star →_→

####解决第三方依赖
```
sudo pip install requests
sudo pip install pyzabbix
```
####登录验证配置说明
1. 创建登录验证要用的配置文件,配置文件采用ini格式,  
必须包含一个名为[Zabbix API]的section,示例如下:  
```
[Zabbix API]
username=Admin  
password=zabbix  
api=https://yourcompany.com/api_jsonrpc.php
no_verify=false
```
