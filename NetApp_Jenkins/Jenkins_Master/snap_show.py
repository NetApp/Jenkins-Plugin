################################################################################
# NetApp-Jenkins Integration Scripts
#          This script was developed by NetApp to help demonstrate NetApp 
#          technologies.  This script is not officially supported as a 
#          standard NetApp product.
#         
# Purpose: Script to list all the checkpoints for a base partition.
#          
#
# Usage:   %> snap_show.py <args> 
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

def count_snap(vol_name):
    tmp = dict(list_snaps(vol_name))
    count = tmp['result']['total_records']
    return count

def list_snaps(vol_name):
    key=get_key(vol_name)
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')
    #print key
    url4= "https://{}/api/2.0/ontap/volumes/{}/snapshots".format(api,key)
    headers = {
        "Authorization": "Basic %s" % base64string,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    #print url4
    r = requests.get(url4,headers=headers,verify=False)
    #print r.json()
    return r.json()

def get_key(vol_name):
    tmp = dict(get_volumes())
    vols = tmp['result']['records']
    for i in vols:
        if i['name'] == vol_name:
            # print i
            return i['key']

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
    return r.json()

def disp_snaps(vol_name):
    i = count_snap(vol_name)
    tmp = dict(list_snaps(vol_name))
    snaps = tmp['result']['records']
    tab = tt.Texttable()
    header = ['Checkpoint name','Dependency']
    tab.header(header)
    tab.set_cols_align(['c','c'])

    for i in snaps:
        ss = i['name']
	dp = i['dependency'] 
        row = [ss,dp]
        tab.add_row(row)
	tab.set_cols_align(['c','c'])	
    s = tab.draw()
    print s

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-v','--vol_name', help='Volume to list snapshots of',dest='vol_name',required=True)
    parser.add_argument('-a','--api', help='API server IP:port details',dest='api')
    parser.add_argument('-apiuser','--apiuser', help='Add APIServer Username',dest='apiuser',required=True)
    parser.add_argument('-apipass','--apipass', help='Add APIServer Password',dest='apipass',required=True)
    globals().update(vars(parser.parse_args()))
    print "Total number of snapshots for partition {}:{}".format(vol_name,count_snap(vol_name))
    disp_snaps(vol_name)


