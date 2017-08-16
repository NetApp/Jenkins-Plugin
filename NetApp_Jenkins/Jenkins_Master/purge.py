################################################################################
# NetApp-Jenkins Integration Scripts
#          This script was developed by NetApp to help demonstrate NetApp 
#          technologies.  This script is not officially supported as a 
#          standard NetApp product.
#         
# Purpose: Script for purge unused snapshots if they exceed the 255 limit.
#          
#
# Usage:   %> purge.py <args> 
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
from operator import itemgetter



requests.packages.urllib3.disable_warnings()

def count_snap(vol_name):
    tmp = dict(list_snaps(vol_name))
    count = tmp['result']['total_records']
    return count

def get_sskey(vol_name,snapshot_name):
    tmp = dict(list_snaps(vol_name))
    snaps = tmp['result']['records']
    for i in snaps:
        if i['name'] == snapshot_name:
            # print i
            return i['key']


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
    header = ['Checkpoint name','Dependency','Access Timestamps']
    tab.header(header)
    tab.set_cols_align(['c','c','c'])

    for i in snaps:
        ss = i['name']
	dp = i['dependency'] 
    	at = i['access_timestamp']
	at = long(at)
        row = [ss,dp,at]
        tab.add_row(row)
	tab.set_cols_align(['c','c','c'])	
    s = tab.draw()
    print s


def snapshot_delete(vol_name,snapshot_name):
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')
    url5= "https://{}/api/2.0/ontap/snapshots/{}".format(api,get_sskey(vol_name,snapshot_name))
    #print url5
    headers = {
        "Authorization": "Basic %s" % base64string,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    #print get_key(vol_name)
    #data= {
      #"volume_key":get_key(vol_name),
      #"name":snapshot_name
    #}
    r = requests.delete(url5, headers=headers,verify=False)


def purge_policy(maxsnaps,vol_name,maxworkspaces):
    i = count_snap(vol_name)
    tmp = dict(list_snaps(vol_name))
    snaps = tmp['result']['records']
    #print snaps
    
    maxsnaps = int(maxsnaps)
    non_busy_snapshot_list = []
    busy_snapshot_list = []
    for j in snaps:
	ss = j['name']
        dp = j['dependency']
        at = j['access_timestamp']
	#print dp
	if dp != 'busy,vclone':
		#print " in the none loop : test"
		non_busy_snapshot_list.append([ss,dp,at])
		#print non_busy_snapshot_list
	elif dp == 'busy,vclone':
		busy_snapshot_list.append([ss,dp,at])

			
    extra_deletable_snapshots = len(non_busy_snapshot_list) - maxsnaps
    #print "Extra deletable non-busy snapshots = {}".format(extra_deletable_snapshots)

    #print "Non Busy snapshots are {}".format(len(non_busy_snapshot_list))
    #print "Extra deletable non-busy snapshots = {}".format(extra_deletable_snapshots)
    #print row
    j = 0
    while j < extra_deletable_snapshots:
	#print j
	#print non_busy_snapshot_list[j][0]
	snapshot_delete(vol_name,non_busy_snapshot_list[j][0])
        j = j+1	



    #print "Snapshots with active clones are = {}".format(len(busy_snapshot_list))
    maxworkspaces =int(maxworkspaces)
    if len(busy_snapshot_list) >= maxworkspaces:
        #print busy_snapshot_list
        print "Please delete unused workspaces"	
   
    print "Purge Policy Run Complete and it has deleted {} of the oldest unused snapshots".format(extra_deletable_snapshots)
    	
    tab = tt.Texttable()
    header = ['Total Snapshots','Non-Busy Snapshots','Busy Snapshots','Purged Snapshots in this Run']
    tab.header(header)
    tab.set_cols_align(['c','c','c','c'])
    row = [i, len(non_busy_snapshot_list),len(busy_snapshot_list),extra_deletable_snapshots]
    tab.add_row(row)
    tab.set_cols_align(['c','c','c','c'])
    s = tab.draw()
    print s

  



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-v','--vol_name', help='Volume to list snapshots of',dest='vol_name',required=True)
    parser.add_argument('-a','--api', help='API server IP:port details',dest='api')
    parser.add_argument('-apiuser','--apiuser', help='Add APIServer Username',dest='apiuser',required=True)
    parser.add_argument('-apipass','--apipass', help='Add APIServer Password',dest='apipass',required=True)
    parser.add_argument('-maxsnaps','--maxsnaps', help='Max number of snapshots for purge policy',dest='maxsnaps',required=True)
    parser.add_argument('-maxworkspaces','--maxworkspaces', help='Max number of allowed workspaces per before warning',dest='maxworkspaces',required=True)
    globals().update(vars(parser.parse_args()))
    #print "Total number of snapshots for partition {}:{}".format(vol_name,count_snap(vol_name))
    print "-----------------------------------------------Purge_Policy_Output-----------------------------------------------"
    purge_policy(maxsnaps,vol_name,maxworkspaces)
    #disp_snaps(vol_name)
    


