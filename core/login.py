#!/usr/bin/env python
# coding=utf-8

import sys
import ConfigParser
import distutils.util
from pyzabbix import ZabbixAPI

# load config module
Config = ConfigParser.ConfigParser()
Config


def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
             print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1



def trylogin(configpath):
    # test the config file
    Config.read(configpath)
    # try to load available settings from config file
    try:
        username = ConfigSectionMap("Zabbix API")['username']
        password = ConfigSectionMap("Zabbix API")['password']
        api = ConfigSectionMap("Zabbix API")['api']
        noverify = bool(distutils.util.strtobool(ConfigSectionMap("Zabbix API")["no_verify"]))
    except:
        pass

    for item in username,password,api:
        for item_string in ['username','password','api']:
            if not item:
                sys.exit('Error:API %s is not set' % item_string)


    # Setup Zabbix API connection
    zapi = ZabbixAPI(api)
    if noverify is True:
        zapi.session.verify = False
    # Login to the Zabbix API
    print("Logging in on '" + api + "' with user '" + username + "'...")
    # Login to the Zabbix API
    zapi.login(username, password)
    return zapi
