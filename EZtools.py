#!/usr/bin/env python
# coding=utf-8
import sys
import argparse
from core import *


child_parser=argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description= 'Easy zabbix tools!',
    epilog="""
Notice:
1.If you do not pass any option except -H or -f,
this EZtools.py script will execute the unlinking and
clearing template(s) of the host(s) then deleting the host(s)!

2.The options of -H and -f only allow one!!!

3.If you just only want to cancel the monitoring of host(s) and
unlink template(s),you just need to pass the corresponding
option like -u|--unlink or -C|--Cancel without any values!

4.Due to the thought of business scenarios,
the option of -u and -C only allow one too!
%s""" % parent_parser.parser.epilog,
    parents=[parent_parser.parser])

group = child_parser.add_mutually_exclusive_group(
    required=True
)
group.add_argument(
    '-H','--hostname',
    help='One or more hostname you want to unlink',
    nargs='+')
group.add_argument(
    '-f','--file',
    help='The file which contains plenty of hostname you want to unlink',
    type=file
)

group2=child_parser.add_mutually_exclusive_group()
group2.add_argument(
    '-u','--unlink',
    help="Just unlink and clear the templates but don't do anything else!",
    action='store_true'
)
group2.add_argument(
    '-C','--Cancel',
    help="Just cancel the monitoring of the host(s) but don't do anything else!",
    action='store_true'
)

# 子解析器调用parse_args()方法解析参数,
# 然后调用login登录模块中的trylogin()方法尝试登录
# 最后返回ZabbixApi类的一个实例zapi和解析后的参数列表,为元祖类型
def argsparse_logintry():
    try:
        args=child_parser.parse_args()
    except IOError,e:
        # -c,-f选项指定了参数类型为file,任何IO错误都会引发异常
        #紧接着打印父,子解析器的帮助文档
        child_parser.print_help()
        child_parser.exit(
            status=1,
            message='\n'+str(e)
        )
    # config选项的类型定义为file类型,所以要想返回
    # config文件的路径需要访问其name属性
    zapi=login.trylogin(args.config.name)
    return args,zapi

def gethost():
    # -H和-f选项互斥,而且必须存在一个参数
    args=argsparse_logintry()[0]
    if args.hostname == None:
        #args.file为file类型,name是其属性,返回文件路径
        hostlist=common.fileparser(args.file.name)
        # 判断文件是否为空
        if hostlist==['']:
            sys.exit('The file you passed do not have hostname in it!')
    else:
        hostlist=args.hostname
    return hostlist

class EZtools():
    zapi=argsparse_logintry()[1]
    host_update_dict={}
    # 思路:
    # 根据hostname拿到hostid,然后根据hostid拿到其所属的所有模板
    # 最后根据模板的名字拿到其所属的id,最后把hostid和模板id均组装为列表
    def __init__(self,hostid):
        self.hostid=hostid

    def temp_unlink(self):
        # 如果主机链接了多个模板,将返回一个包含多个大字典的列表
        temp_name_collection = \
            self.zapi.template.get(output="extend", hostids=self.hostid)
        # 判断是否存在模板
        if temp_name_collection:
            # 遍历列表,根据模板名字拿到id,然后组装为列表
            temp_id=[]
            temp_name_list=[]
            for temp_name in temp_name_collection:
                # 遍历之后,temp_name为一个只含有一个字典元素的列表
                temp_id.append(
                    self.zapi.template.get(
                        filter=({'host':temp_name['name']}))[0]['templateid'])
                temp_name_list.append(temp_name['name'])
            # 开始执行模板unlink and clear动作
            #zapi.host.massremove(hostids=hostid_list,
            #                     templateids_clear=temp_id)
            for temp_name_real in temp_name_list:
                print "%s ==> The template of '%s' had unlinked and cleared!" \
                      % (self.host, temp_name_real)
        else:
            print 'The host of %s do not have any templates!' % self.host

    def cancel_monitor(self):
        pass

def real_action():

    if args.unlink:

        temp_unlink()

def args_assert(command=None):
    hostlist=gethost()
    zapi=argsparse_logintry()[1]
    args=argsparse_logintry()[0]
    for host in hostlist:
        # 从文件中解析出来的主机名列表有可能存在空字符串元素
        if host !='':
            # host.get()方法获取主机id时返回一个只有一个字典元素的列表
            hostid_collection=zapi.host.get(output="extend",
                                            filter={"host": host})
            # 判断主机是否存在
            if hostid_collection:
                # unlink主机模板时需要传入列表数据类型的hostid,
                # 而更新主机信息时,又需要传入字符串类型的hostid,shit!
                hostid_list=[]
                hostid_string=hostid_collection[0]['hostid']
                hostid_list.append(hostid_string)
                command
            else:
                with open('hosterror.log','a+') as hosterror:
                    hosterror.write('%s =>> The hostname can not find!\n' % host)
                sys.exit('%s =>> The hostname can not find!' % host)


