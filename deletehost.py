#!/usr/bin/env python
# coding=utf-8

import argparse
from core import *

child_parser=argparse.ArgumentParser(
    parents=[parent_parser.parser],
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Description:delete host...',
    epilog="""%s %s """ % parent_parser.parent_usage())

parser=common.Args(child_parser)
zapi=parser.getzapi()

def delete_host(hostid):
    #File "/Library/Python/2.7/site-packages/pyzabbix/__init__.py",
    #line 157, in fn args or kwargs
    #吐槽:被坑了一下下,我要不要给https://github.com/CNSRE/Zabbix-PyZabbix/
    # blob/master/zabbix_host_delete.py 提个request:-D
    zapi.host.delete(hostid)


def host_check():
    hostlist = parser.gethost()
    for host in hostlist:
        # 从文件中解析出来的主机名列表有可能存在空字符串元素
        if host != '':
            # host.get()方法获取主机id时返回一个只有一个字典元素的列表
            hostid_collection = zapi.host.get(output="extend",
                                              filter={"host": host})
            # 判断主机是否存在
            if hostid_collection:
                hostid = hostid_collection[0]['hostid']
                print hostid
                delete_host(hostid)
            else:
                # 思路:与common模块中的gethost()方法一样
                errp=common.Tools()
                errp.host=host
                errp.hosterror(host)
if __name__ == '__main__':
    host_check()