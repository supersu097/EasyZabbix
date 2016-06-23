#!/usr/bin/env python
# coding=utf-8

import argparse
from core import *

child_parser = argparse.ArgumentParser(
    parents=[parent_parser.parser],
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Description:disable one trigger for many hosts...',
    epilog="""%s %s """ % parent_parser.parent_usage())

child_parser.add_argument(
    '-e', '--enable',
    help='Enable trigger...',
    action='store_true'
)

child_parser.add_argument(
    '-t','--triggerid',
    help='The triggerid you wanna disable',
    type=int
)
zapi = common.getzapi(child_parser)
args = common.args_parser(child_parser)