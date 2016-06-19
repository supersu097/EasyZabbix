#!/usr/bin/env python
# coding=utf-8
import argparse
from core import parent_parser
from core import common

child_parser = argparse.ArgumentParser(
    parents=[parent_parser.parser],
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Description:disable host monitoring...',
    epilog="""%s %s """ % parent_parser.parent_usage())

child_parser.add_argument(
    '-e', '--enable',
    help='Enable host monitoring...',
    action='store_true'
)
zapi = common.zapiget(child_parser)
args = common.args_parser(child_parser)


def cancelmonitor(host, host_dict):
    # 构造一个key为hostid和主机监控status的字典传进来
    zapi.host.update(**host_dict)
    if args.enable:
        print '[%s]INFO: [%s]:Enabled monitoring!\n' \
              % (common.nowdate(), host)
        with open('hostmonitor.log', 'a+') as hostmon:
            hostmon.write('[%s]INFO: [%s]:Enabled monitoring!\n'
                          % (common.nowdate(), host))
    else:
        print '[%s]INFO: [%s]: Disabled monitoring!\n' % \
              (common.nowdate(), host)
        with open('hostmonitor_status.log', 'a+') as hostmon:
            hostmon.write('[%s]INFO: [%s]: Disabled monitoring!\n'
                          % (common.nowdate(), host))


def host_check():
    hostlist = common.hostget(child_parser)
    for host in hostlist:
        host_dict = {}
        # 从文件中解析出来的主机名列表有可能存在空字符串元素
        if host != '':
            # host.get()方法获取主机id时返回一个只有一个字典元素的列表
            hostid_collection = zapi.host.get(output="extend",
                                              filter={"host": host})
            # 判断主机是否存在
            if hostid_collection:
                hostid = hostid_collection[0]['hostid']
                host_dict['hostid'] = hostid
                if args.enable:
                    host_dict['status'] = 0
                else:
                    host_dict['status'] = 1
                # 开始执行真正的操作
                cancelmonitor(host, host_dict)
            else:
                common.hostnotfind(host)


if __name__ == '__main__':
    host_check()
