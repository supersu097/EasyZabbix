#!/usr/bin/env python
# coding=utf-8
import sys
import login
import datetime


def nowdate():
    now = datetime.datetime.now()
    nowdate = now.strftime("%Y-%m-%d %H:%M:%S")
    return nowdate


def file_parser(fileinput):
    with open(fileinput, 'rU') as lines:
        data = lines.read().split('\n')
    return data


def hostnotfind(host):
    with open('hostnotfind.log', 'a+') as hosterror:
        hosterror.write('[%s]ERROR: [%s]:Host not find!\n'
                        % (nowdate(), host))


def args_parser(which_parser):
    try:
        args = which_parser.parse_args()
        return args
    except IOError, e:
        # -c,-f选项指定了参数类型为file,任何IO错误都会引发异常
        # 紧接着打印脚本的帮助文档
        which_parser.print_help()
        which_parser.exit(
            status=1,
            message='\n' + str(e))

def zapiget(which_parser):
    # 实例化login模块中的ConfigLoad类
    configload = login.ConfigLoad()
    # 调用trylogin()方法尝试登录,登录完毕后返回zabbix API的实例对象
    return configload.trylogin(
        args_parser(which_parser).config.name)


def hostget(which_parser):
    args = args_parser(which_parser)
    # -H和-f选项互斥,而且必须存在一个参数
    if args.hostname is None:
        # args.file为file类型,name是其属性,返回文件路径
        hostlist = file_parser(args.file.name)
        # 判断文件是否为空
        if hostlist == ['']:
            sys.exit('[%s]: File empty!\n'
                     % args.file.name)
    else:
        hostlist = args.hostname
    return hostlist
