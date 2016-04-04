#!/usr/bin/env python
# coding=utf-8
import sys
import argparse
from core import *


child_parser=argparse.ArgumentParser(
    description='Unlink all templates of the specified hosts'
                '(Default to clear all its entities)!',
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
    type=file,
    nargs=1
)

try:
    args=child_parser.parse_args()
except IOError,e:
    parent_parser.parser.print_help()
    child_parser.error(str(e))

#login.trylogin(args.config.name)


if args.hostname:
    print args.hostname








