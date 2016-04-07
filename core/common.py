#!/usr/bin/env python
# coding=utf-8
import os
import sys

def fileparser(file):
    with open(file,'rU') as lines:
        data=lines.read().split('\n')
    return data

