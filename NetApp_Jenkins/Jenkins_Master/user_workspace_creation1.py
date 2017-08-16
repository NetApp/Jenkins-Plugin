################################################################################
# NetApp-Jenkins Integration Scripts
#          This script was developed by NetApp to help demonstrate NetApp 
#          technologies.  This script is not officially supported as a 
#          standard NetApp product.
#         
# Purpose: Script to create a new local workspace from an existing partition.
#          
#
# Usage:   %> user_workspace_creation.py <args> 
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

requests.packages.urllib3.disable_warnings()

def get_jpath(vol_name):
    tmp = dict(get_volumes())
    vols = tmp['result']['records']
    for i in vols:
        if i['name'] == vol_name:
            # print i
            return i['junction_path']

def get_key(vol_name):
    tmp = dict(get_volumes())
    vols = tmp['result']['records']
    for i in vols:
        if i['name'] == vol_name:
            # print i
            return i['key']

def get_sskey(vol_name,snap_name):
    tmp = dict(get_snaps(vol_name))
    snaps = tmp['result']['records']
    for i in snaps:
        if i['name'] == snap_name:
            # print i
            return i['key']

def get_snaps(vol_name):
    key=get_key(vol_name)
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')
    #print key
    url4= "https://{}/api/2.0/ontap/snapshots?volume_key={}".format(api,key)
    headers = {
        "Authorization": "Basic %s" % base64string,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    #print url4
    r = requests.get(url4,headers=headers,verify=False)
    #print r.json()
    return r.json()

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

def make_clone(vol_name,snapshot_name,clone_name):
    #print snapshot_name
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')
    key=get_key(vol_name)
    #print key
    url2= "https://{}/api/2.0/ontap/volumes/{}/jobs/clone".format(api,key)
    #print url2
    headers = {
        "Authorization": "Basic %s" % base64string,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    ss_key= get_sskey(vol_name,snapshot_name)
    #print ss_key
    data= {
        "security_user_id":uid,
        "security_group_id":gid,
        "volume_clone_name":"{}".format(clone_name),
        "snapshot_key":get_sskey(vol_name,snapshot_name)
        }
    #print data
    r = requests.post(url2, headers=headers,json=data,verify=False)
    #print "Clone Created"

def make_clonejpath(clone_name):
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')
    clone = check_vol(clone_name)
    #print clone
    url6= "https://{}/api/2.0/ontap/volumes/{}/jobs/mount".format(api,get_key(clone_name))
    #print url6
    headers = {
        "Authorization": "Basic %s" % base64string,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data= {
            "junction_path":'/'+clone_name
          }
    #print data
    r = requests.post(url6, headers=headers,json=data,verify=False)
    return clone

def check_vol(vol_name):
    tmp = dict(get_volumes())
    vols = tmp['result']['records']
    names = [i['name'] for i in vols]
    #print "Volume Names: ", names
    return vol_name in names

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-v','--vol_name', help='Volume to create or clone from',dest='vol_name',required=True)
    parser.add_argument('-a','--api', help='IP:port of API server',dest='api',required=True)
    parser.add_argument('-s','--snapshot_name', help='Snapshot to create or clone from',dest='snapshot_name')
    parser.add_argument('-c','--clone_name', help='Name of the clone to create',dest='clone_name')
    parser.add_argument('-apiuser','--apiuser', help='Add APIServer Username',dest='apiuser',required=True)
    parser.add_argument('-apipass','--apipass', help='Add APIServer Password',dest='apipass',required=True)
    parser.add_argument('-uid','--uid', help='Add User ID',dest='uid')
    parser.add_argument('-gid','--gid', help='Add Group ID',dest='gid')
    globals().update(vars(parser.parse_args()))

    clone = False
    count = 0
    make_clone(vol_name,snapshot_name,clone_name)
    while (clone == False):
        clone = make_clonejpath(clone_name)
        time.sleep(1)
        count=count+1
    
    print "Clone created successfully in {} seconds.".format(count)

