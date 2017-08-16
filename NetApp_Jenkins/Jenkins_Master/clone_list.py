################################################################################
# NetApp-Jenkins Integration Scripts
#          This script was developed by NetApp to help demonstrate NetApp 
#          technologies.  This script is not officially supported as a 
#          standard NetApp product.
#         
# Purpose: Script to list all the local workspaces for a base partition.
#          
#
# Usage:   %> clone_list.py <args> 
#
# Author:  Akshay Patil (akshay.patil@netapp.com)
#
# NETAPP CONFIDENTIAL
# -------------------
# Copyright 2016 NetApp, Inc. All Rights Reserved.
#
# NOTICE: All information contained herein is, and remains the property
# of NetApp, Inc.  The intellectual and technical concepts contained
# herein are proprietary to NetApp, Inc. and its suppliers, if applicable,
# and may be covered by U.S. and Foreign Patents, patents in process, and are
# protected by trade secret or copyright law. Dissemination of this
# information or reproduction of this material is strictly forbidden unless
# permission is obtained from NetApp, Inc.
#
################################################################################
import base64
import argparse
import sys
import requests
import ssl
import subprocess
import time
import os
from subprocess import call
import texttable as tt

requests.packages.urllib3.disable_warnings()

def get_volumes():
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')

    url = "https://{}/api/2.0/ontap/volumes/".format(api)
    headers = {
        "Authorization": "Basic %s" % base64string,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    r = requests.get(url, headers=headers,verify=False)
    #print r.json()
    #print "get_volumes works"
    return r.json()

def get_key(vol_name):
    tmp = dict(get_volumes())
    vols = tmp['result']['records']
    for i in vols:
        if i['name'] == vol_name:
            # print i
            return i['key']

def disp_clones(vol_name):
    ctr = 0
    tmp = dict(get_volumes())
    vols = tmp['result']['records']
    tab = tt.Texttable()
    header = ['Workspace name']
    tab.header(header)
    tab.set_cols_align(['c'])
    key = get_key(vol_name)
    for i in vols:
	if i['clone_parent_key'] == key:
            ctr = ctr + 1 
            cl = i['name']
            row = [cl]
            tab.add_row(row)
            tab.set_cols_align(['c'])
    
    print "Number of active workspaces for Partition {} :{}".format(vol_name,ctr)
    s = tab.draw()
    print s

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-v','--vol_name', help='Volume to create or clone from',dest='vol_name',required=True)
    parser.add_argument('-a','--api', help='API server IP:port details',dest='api')
    parser.add_argument('-apiuser','--apiuser', help='Add APIServer Username',dest='apiuser',required=True)
    parser.add_argument('-apipass','--apipass', help='Add APIServer Password',dest='apipass',required=True)
    globals().update(vars(parser.parse_args()))
    disp_clones(vol_name)

