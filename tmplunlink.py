#!/usr/bin/env python
# coding=utf-8
import argparse
from core import parent_parser
from core import common

child_parser = argparse.ArgumentParser(
    parents=[parent_parser.parser],
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Description: Unlink and clear templates...',
    epilog="""%s %s""" % parent_parser.parent_usage())

# 单独unlink模板的功能还未实现
child_parser.add_argument(
    '-t', '--tmpl',
    help='The single template you wanna unlink '
         'for one or more hosts!'
)
args = common.args_parser(child_parser)
zapi = common.zapiget(child_parser)


def temp_unlink(host, hostid):
    # 思路:
    # 根据hostname拿到hostid,然后根据hostid拿到其所属的所有模板
    # 最后根据模板的名字拿到其所属的id,然后把hostid和模板id均组装为列表
    # 如果主机链接了多个模板,将返回一个包含多个大字典的列表

    temp_name_collection = \
        zapi.template.get(output="extend", hostids=hostid)
    # 判断是否存在模板
    if temp_name_collection:
        # 遍历列表,根据模板名字拿到id,然后组装为列表
        temp_id_list = []
        temp_name_list = []
        # temp_name_collection为上面所说的返回一个包含多个大字典的列表
        for temp_name in temp_name_collection:
            # 遍历之后,temp_name为一个只含有一个字典元素的列表
            temp_id_list.append(
                zapi.template.get(
                    filter=({'host': temp_name['name']}))[0]['templateid'])
            temp_name_list.append(temp_name['name'])
        # 开始执行模板unlink and clear动作
        # unlink主机模板时需要传入列表数据类型的hostid,
        # 这里有个技巧,貌似不需要初始化列表,直接在变量的外侧添加[]就行了,如下:
        # hostid_list = []
        # hostid_list.append(hostid)
        zapi.host.massremove(hostids=[hostid],
                             templateids_clear=temp_id_list,
                             templateids=temp_id_list)
        for temp_name_real in temp_name_list:
            print "[%s]INFO: [%s]: [%s]: Template unlinked!" \
                  % (common.nowdate(),
                     host,
                     temp_name_real)
            with open('tmpllink.log', 'a+') as tmplunlink:
                tmplunlink.write(
                    "[%s]INFO: [%s]: [%s]: Unlinked!\n"
                    % (common.nowdate(),
                       host,
                       temp_name_real))
    else:
        print '[%s]: No template exists!' % host


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
                temp_unlink(host, hostid)
            else:
                # 思路:与common模块中的gethost()方法一样
                common.hostnotfind(host)


if __name__ == '__main__':
    host_check()
