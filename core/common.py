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
        hosterror.write('[%s]ERROR: [%s]: The hostname can not find!\n'
                        % (nowdate(), host))
    print '[%s]ERROR: [%s]: The hostname can not find!\n' \
          % (nowdate(), host)


def trrigerdis_record():
    pass


def args_parser(which_parser):
    # 子解析器调用Args本类的parse_args()进行参数解析时需要传递其实例化对象
    try:
        args = which_parser.parse_args()
    except IOError, e:
        # -c,-f选项指定了参数类型为file,任何IO错误都会引发异常
        # 紧接着打印脚本的帮助文档
        which_parser.print_help()
        which_parser.exit(
            status=1,
            message='\n' + str(e))
    return args


def getzapi(which_parser):
    # 实例化login模块中的ConfigLoad类
    configload = login.ConfigLoad()
    # 调用trylogin()方法尝试登录,登录完毕后返回zabbix API的实例对象
    zapi = configload.trylogin(args_parser(which_parser).config.name)
    return zapi


def gethost(which_parser):
    args = args_parser(which_parser)
    # -H和-f选项互斥,而且必须存在一个参数
    if args.hostname is None:
        # args.file为file类型,name是其属性,返回文件路径
        hostlist = file_parser(file)
        # 判断文件是否为空
        if hostlist == ['']:
            sys.exit('The file of [%s] you passed do not'
                     ' have hostname in it!\n' % args.file.name)
    else:
        hostlist = args.hostname
    return hostlist
