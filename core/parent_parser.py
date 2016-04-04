#!/usr/bin/env python
# coding=utf-8
import argparse
import os

defconf = os.getenv("HOME") + "/.zbx.conf"
parser=argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Easy zabbix tools!',
    epilog="""
 This program can use .ini style configuration files to retrieve the needed
 API connection information.To use this type of storage, create a conf file
 (the default is $HOME/.zbx.conf) that contains at least the [Zabbix API]
 section and any of the other parameters:

 [Zabbix API]
 username=yourusername
 password=yourpassword
 api=https://your-zabbix-frontend-url/api_jsonrpc.php
 no_verify=flase""",
    add_help=False
)

parser.add_argument(
    '-c','--config',
    help='Config file location (defaults to $HOME/.zbx.conf)',
    default=defconf
)
