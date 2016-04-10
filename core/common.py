#!/usr/bin/env python
# coding=utf-8
import sys
import login


class Help:
    def file_parser(self, file):
        with open(self.file, 'rU') as lines:
            data = lines.read().split('\n')
        return data


class Args:
    def __init__(self, which_parser):
        self.which_parser = which_parser

    def args_parser(self):
        # 子解析器调用Args本类的parse_args()进行参数解析时需要传递其实例化对象
        try:
            args = self.which_parser.parse_args()
        except IOError, e:
            # -c,-f选项指定了参数类型为file,任何IO错误都会引发异常
            # 紧接着打印脚本的帮助文档
            self.which_parser.print_help()
            self.which_parser.exit(
                status=1,
                message='\n' + str(e))
        return args

    def getzapi(self):
        # config选项的类型定义为file类型,所以要想返回
        # config文件的路径需要访问其name属性
        args = self.args_parser()
        # 实例化login模块中的ConfigLoad类
        configload = login.ConfigLoad()
        # 调用trylogin()方法尝试登录,登录完毕后返回zabbix API的实例对象
        zapi = configload.trylogin(args.config.name)
        return zapi

    def gethost(self):
        args = self.args_parser()
        # -H和-f选项互斥,而且必须存在一个参数
        if args.hostname == None:
            help = Help()
            # 给Help的实例化对象help绑定属性file
            help.file = args.file.name
            # args.file为file类型,name是其属性,返回文件路径
            hostlist = help.file_parser(help.file)
            # 判断文件是否为空
            if hostlist == ['']:
                sys.exit('The file of [%s] you passed do not'
                         ' have hostname in it!\n' % args.file.name)
        else:
            hostlist = args.hostname
        return hostlist
