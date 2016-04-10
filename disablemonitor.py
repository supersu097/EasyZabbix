#!/usr/bin/env python
# coding=utf-8
import argparse
from core import *

child_parser=argparse.ArgumentParser(
    parents=[parent_parser.parser],
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Description:disable host monitoring...',
    epilog="""%s %s """ % parent_parser.parent_usage())

parser=common.Args(child_parser)
zapi=parser.getzapi()

