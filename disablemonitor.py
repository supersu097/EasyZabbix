#!/usr/bin/env python
# coding=utf-8
import argparse
from core import *

child_parser=argparse.ArgumentParser(
    parents=[parent_parser.parser],
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Description:disable host monitoring...',
    epilog="""%s %s """ % parent_parser.parent_usage())

child_parser.add_argument(
    '-e','--enable',
    help='Enable host monitoring...',
    action='store_true'
)
parser=common.Args(child_parser)
zapi=parser.getzapi()
args=parser.args_parser()

def cancelmonitor(host,host_dict):
    # 构造一个key为hostid和主机监控status的字典传进来
    zapi.host.update(**host_dict)
    if args.enable:
        print 'The host of %s has monitored again!' % host
    else:
        print 'The host of %s has disabled monitoring!' % host
def host_check():
    hostlist = parser.gethost()
    for host in hostlist:
        host_dict={}
        # 从文件中解析出来的主机名列表有可能存在空字符串元素
        if host != '':
            # host.get()方法获取主机id时返回一个只有一个字典元素的列表
            hostid_collection = zapi.host.get(output="extend",
                                              filter={"host": host})
            # 判断主机是否存在
            if hostid_collection:
                hostid_int = hostid_collection[0]['hostid']
                host_dict['hostid']=hostid_int
                if args.enable:
                    host_dict['status']=0
                else:
                    host_dict['status']=1
                # 开始执行真正的操作
                cancelmonitor(host, host_dict)
            else:
                with open('hosterror.log', 'a+') as hosterror:
                    hosterror.write('%s =>> The hostname can not find!\n' % host)
                print '[ %s ] =>> The hostname can not find!' % host

if __name__ == '__main__':
    host_check()