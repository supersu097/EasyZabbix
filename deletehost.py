#!/usr/bin/env python
# coding=utf-8

import argparse
from core import common
from core import parent_parser

child_parser = argparse.ArgumentParser(
    parents=[parent_parser.parser],
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Description:delete host...',
    epilog="""%s %s """ % parent_parser.parent_usage())

zapi = common.zapiget(child_parser)


def hostdel_record(host):
    print '[%s]INFO: [%s]:Host deleted!' \
          % (common.nowdate(), host)
    with open('hostdel.log', 'a+') as hostdel:
        hostdel.write('[%s]INFO: [%s]:Host deleted!\n'
                      % (common.nowdate(), host))


def host_delete(hostid):
    zapi.host.delete(hostid)


def host_check():
    hostlist = common.hostget(child_parser)
    for host in hostlist:
        # 从文件中解析出来的主机名列表有可能存在空字符串元素
        if host != '':
            # host.get()方法获取主机id时返回一个只有一个字典元素的列表
            hostid_collection = zapi.host.get(output="extend",
                                              filter={"host": host})
            # 判断主机是否存在
            if hostid_collection:
                hostid = hostid_collection[0]['hostid']
                host_delete(hostid)
                hostdel_record(host)
            else:
                common.hostnotfind(host)


if __name__ == '__main__':
    host_check()