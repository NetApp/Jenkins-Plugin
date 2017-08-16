################################################################################
# NetApp-Jenkins Integration Scripts
#          This script was developed by NetApp to help demonstrate NetApp 
#          technologies.  This script is not officially supported as a 
#          standard NetApp product.
#         
# Purpose: Script to delete obsolete clones.
#          
#
# Usage:   %> clone_purge.py <args> 
#
# Author:  Akshay Patil (akshayp@netapp.com)
#           
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
import re
import sys
import requests
import ssl
import subprocess
import time
import os
from subprocess import call

requests.packages.urllib3.disable_warnings()

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
    #print r.headers
    #print "get_volumes works"
    return r.json()

def check_vol_jpath(clone_name):
    clonejpath = '/'+clone_name
    tmp = dict(get_volumes())
    vols = tmp['result']['records']
    jpaths = [i['junction_path'] for i in vols]
    #print "Volume Names: ", names
    return clonejpath in jpaths

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

def clone_delete(clone_name):
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')
    url5= "https://{}/api/2.0/ontap/volumes/{}".format(api,get_key(clone_name))
    url6= "https://{}/api/2.0/ontap/volumes/{}/jobs/unmount".format(api,get_key(clone_name))
    #print url5
    headers = {
        "Authorization": "Basic %s" % base64string,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    #print get_key(vol_name)
    data= {
      "state":"offline"
    }
    r = requests.post(url6, headers=headers,verify=False)
    time.sleep(5)
    jpath_check = check_vol_jpath(clone_name)
    # Wait for job completion
    while (jpath_check!= False):
        #print jpath_check
        jpath_check = check_vol_jpath(clone_name)
        
    r = requests.put(url5, headers=headers,json = data,verify=False)
    print "Successfully taken clone {} offline".format(clone_name)
    time.sleep(3)
    r = requests.delete(url5, headers=headers,verify=False)
    print "Temporary Clone deleted successfully"

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-a','--api', help='API server IP:port details',dest='api',required=True)
    #parser.add_argument('-c','--clone_name', help='Name of the clone to create',dest='clone_name',required=True)
    #parser.add_argument('-cnt','--cont', help='Name of the Container on which workspace is mounted',dest='cont',required=False)
    parser.add_argument('-apiuser','--apiuser', help='Add APIServer Username',dest='apiuser',required=True)
    parser.add_argument('-apipass','--apipass', help='Add APIServer Password',dest='apipass',required=True)
    out1 = subprocess.Popen(["df","|","grep","/tmp/vol2"],stdout=subprocess.PIPE).communicate()[0]
    #print (out1)
    out_clone=re.match(r'\AFilesystem.*[\r\n]+[^/]+/(\S+)', out1)
    clone_name=str(out_clone.group(1))
    print(clone_name)

    globals().update(vars(parser.parse_args()))
    clone_delete(clone_name)

    
