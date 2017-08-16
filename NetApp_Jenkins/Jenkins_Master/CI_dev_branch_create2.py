################################################################################
# NetApp-Jenkins Integration Scripts
#          This script was developed by NetApp to help demonstrate NetApp
#          technologies.  This script is not officially supported as a
#          standard NetApp product.
#
# Purpose: Script to create a new base partition container with a netapp volume mounted to it and pu# ll code from the SCM onto this
#
#
# Usage:   %> CI_dev_branch_create2.py <args>
#
# Author:  Akshay Patil (akshay.patil@netapp.com)
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


import time
import base64
import argparse
import json
import requests 
requests.packages.urllib3.disable_warnings()

def get_svms():
    #base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')
    
    url = "https://{}/api/1.0/slo/storage-vms/".format(api)
    headers = {
    'authorization': "Basic %s" % base64string,
    'content-type': "application/json",
    'accept': "application/json"
    }

    r = requests.get(url, headers=headers,verify=False)
    #print r.json()
    return r.json()


def get_key_svms(svm_name):
    tmp = dict(get_svms())
    svms = tmp['result']['records']
    for i in svms:
        if i['name'] == svm_name:
            # print i
            return i['key']


#def get_storage_platform_resource_key(vol_name):
    #tmp = dict(get_vols())
    #platform_keys =tmp['result']['records']
    

def get_vols():
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')

    #url = "https://{}/api/1.0/ontap/volumes/".format(api)
    url = "https://{}/api/1.0/slo/file-shares/".format(api)

    headers = {
    'authorization': "Basic %s" % base64string,
    'content-type': "application/json",
    'accept': "application/json"
    }

    r = requests.get(url, headers=headers,verify=False)
    
    #print r.json()
    #with open('/tmp/ps/data.txt', 'w') as outfile:
        #json.dump(r, outfile)
    return r.json()

def check_vol(vol_name):
    tmp = dict(get_vols())
    vols = tmp['result']['records']
    names = [i['name'] for i in vols]
    #print "Volume Names: ", names
    return vol_name in names


def get_storage_platform_resource_key(vol_name):
    tmp = dict(get_vols())
    vols = tmp['result']['records']
    for i in vols:
        if i['name'] == vol_name:
            #print i['storage_platform_resource_key']
            return i['storage_platform_resource_key']


def make_snapdir_false(vol_name):
    storage_platform_resource_key=get_storage_platform_resource_key(vol_name)

    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')
    #v_size=get_size(vol_size)
    url = "https://{}/api/2.0/ontap/volumes/{}".format(api,storage_platform_resource_key)
    payload = {
    #"storage_service_level_key": "44b90387-a490-4267-8229-9c0b422e961c",
    #"storage_vm_key": svm_key,
    #"name": vol_name,
    #"size": v_size
    "is_snap_dir_access_enabled":"False"
    }
    headers = {
    'authorization': "Basic %s" % base64string,
    'content-type': "application/json",
    'accept': "application/json"
    }
    response = requests.put(url,headers=headers,json=payload,verify=False)
      

def get_size(vol_size):
    tmp = int(vol_size) * 1024 * 1024
    return tmp


def make_volume(vol_name,svm_name,vol_size):
    svm_key=get_key_svms(svm_name)

    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')
    v_size=get_size(vol_size)
    url = "https://{}/api/1.0/slo/file-shares".format(api) 
    payload = {
    "storage_service_level_key": "44b90387-a490-4267-8229-9c0b422e961c",
    "storage_vm_key": svm_key,
    "name": vol_name,
    "size": v_size
    #"is_snap_dir_access_enabled":"False"
    } 
    headers = {
    'authorization': "Basic %s" % base64string,
    'content-type': "application/json",
    'accept': "application/json"
    }
    response = requests.post(url,headers=headers,json=payload,verify=False)
    #print (response.text)
    #print(response.text)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-v','--vol_name', help='Volume to create or clone from',dest='vol_name',required=True)
    parser.add_argument('-vs','--vs name', help='Select SVM',dest='svm_name',required=True)
    parser.add_argument('-s','--vol_size', help='Size of Volume',dest='vol_size',required=True)
    parser.add_argument('-a','--api', help='API server IP:port',dest='api',required=True)
    parser.add_argument('-apiuser','--apiuser', help='Add APIServer Username',dest='apiuser',required=True)
    parser.add_argument('-apipass','--apipass', help='Add APIServer Password',dest='apipass',required=True)

    globals().update(vars(parser.parse_args()))
    count = 0
    make_volume(vol_name,svm_name,vol_size)
    while check_vol(vol_name) == False:
        time.sleep(1)
        count=count+1
    time.sleep(5)
    make_snapdir_false(vol_name)
    #get_storage_platform_resource_key(vol_name)
    print "New Development Branch baseline created successfully in {} seconds".format(count)
    make_snapdir_false(vol_name)

