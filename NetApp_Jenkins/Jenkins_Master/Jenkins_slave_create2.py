################################################################################
# NetApp-Jenkins Integration Scripts
#          This script was developed by NetApp to help demonstrate NetApp
#          technologies.  This script is not officially supported as a
#          standard NetApp product.
#
# Purpose: Script to create a new Jenkins slave container with a NetApp volume/clone mounted.
#
#
# Usage:   %> Jenkins_slave_create2.py <args>
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
import argparse
import time
import sys
import subprocess
from subprocess import call

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-i','--image_name', help='Image to run the container from',dest='image_name',required=True)
    parser.add_argument('-m','--masterip', help='IP address of the Jenkins Master Container',dest='masterip',required=True)
    parser.add_argument('-c','--cont_name', help='Name of the container',dest='cont_name',required=True)
    parser.add_argument('-l','--label_name', help='Name of the label of the slave',dest='label_name',required=True)
    parser.add_argument('-p','--proj_name', help='Name of the project tied to this workspace',dest='proj_name',required=True)
    parser.add_argument('-v','--vol_name', help='Name of the volume tied to this workspace',dest='vol_name',required=True)
    globals().update(vars(parser.parse_args()))
    slave_name = proj_name
    #test_cmd = "docker volume create -d netapp --name={}".format(vol_name)
    #return_code1 = subprocess.call(test_cmd,shell=True,stderr=subprocess.STDOUT)
    time.sleep(10)
    #dock_cmd = "docker run -i -t -d -e labelname={} -e masterip={} -e slavename={} --name {} --restart always --volume-driver netapp --volume {}:/workspace/{} {}".format(label_name,masterip,slave_name,cont_name,vol_name,proj_name,image_name)

    dock_service_cmd = 'docker service create --replicas 1 --restart-condition on-failure  --mount "type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock" --mount "type=volume,source={},volume-driver=netapp,target=/workspace/{}" --name {} -e masterip={} -e labelname={} -e slavename={} {}'.format(vol_name,proj_name,vol_name,masterip,proj_name,slave_name,image_name)
    time.sleep(5) 
    return_code = subprocess.call(dock_service_cmd,shell=True,stderr=subprocess.STDOUT)
    



    #return_code = subprocess.call(dock_cmd,shell=True,stderr=subprocess.STDOUT)


