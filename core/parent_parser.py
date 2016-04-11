#!/usr/bin/env python
# coding=utf-8
import argparse
import os
parser=argparse.ArgumentParser(
    add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""
Easy zabbix tools!!!
""",
    epilog="""
This program can use .ini style configuration files to retrieve the needed
API connection information.To use this type of storage, create a conf file
(the default is $HOME/.zbx.conf) that contains at least the [Zabbix API]
section and any of the other parameters:
[Zabbix API]
username=yourusername
password=yourpassword
api=https://your-zabbix-frontend-url/api_jsonrpc.php
no_verify=flase

Any question can contact with me at lin.gan@ele.me!
GayHub repository(:-D at https://github.com/supersu097/EasyZabbix
welcome to fxxk and star!
Finally,thank the open project at https://github.com/q1x/zabbix-gnomes!!!

Notice:
The options of -H and -f only allow one!!!
 """
)

defconf = os.getenv("HOME") + "/.zbx.conf-test"

parser.add_argument(
    '-c','--config',
    help='Config file location (defaults to $HOME/.zbx.conf)',
    default=defconf,
    type=file
)

group = parser.add_mutually_exclusive_group(
    required=True
)
group.add_argument(
    '-H','--hostname',
    help='One or more hostname you wanna do sth,if hostname has whitespace,pls use quotes to it!',
    nargs='+')
group.add_argument(
    '-f','--file',
    help='Many hostname in file,notice that one line one hostname',
    type=file
)

def parent_usage():

    return parser.description,parser.epilog

