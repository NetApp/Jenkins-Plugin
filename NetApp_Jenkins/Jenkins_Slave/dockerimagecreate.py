################################################################################
# NetApp-Jenkins Integration Scripts
#          This script was developed by NetApp to help demonstrate NetApp
#          technologies.  This script is not officially supported as a
#          standard NetApp product.
#
# Purpose: Script to create a new docker image out of a running docker-container.
#
#
# Usage:   %> dockerimagecreate.py <args>
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
import argparse
import sys
import time
import subprocess
from subprocess import call

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-dcontname','--dcontname', help='Enter The container name to create image',dest='dcontname',required=True)
    parser.add_argument('-dimgname','--dimgname', help='Enter the Name of image to create',dest='dimgname',required=True)
    parser.add_argument('-duser','--duser', help='Enter the docker repo username',dest='duser',required=True)
    parser.add_argument('-dpass','--dpass', help='Password for the docker repo',dest='dpass',required=True)
    parser.add_argument('-art_url','--art_url', help='Enter Artifactory URL',dest='art_url',required=True)
    globals().update(vars(parser.parse_args()))
    #slave_name = proj_name


    dock_login = "docker login {} -u={} -p={}".format(art_url,duser,dpass)
    return_code = subprocess.call(dock_login,shell=True,stderr=subprocess.STDOUT)
    time.sleep(5)

    #print "Docker Login Successful"

    service_id = "hostname"
#Commit Changes
    #service_cont_name = subprocess.call(service_id,shell=True,stderr=subprocess.STDOUT)
    #output = subprocess.check_output("hostname", shell=True)
    #print service_cont_name

    output = subprocess.Popen(['hostname'], stdout=subprocess.PIPE).communicate()[0]
    print output
    output = output[:-1]
    dock_commit = "docker commit {} {}".format(output,dimgname)
    return_code = subprocess.call(dock_commit,shell=True,stderr=subprocess.STDOUT)
    time.sleep(10)
    print "Image Committed"
#Push Changes
    dock_push = "docker push {}".format(dimgname)
    return_code = subprocess.call(dock_push,shell=True,stderr=subprocess.STDOUT)
    time.sleep(10)
    print "Image Pushed to Artifactory"

#Push to Docker image
    #dock_cmd = "docker run -i -t -d -e labelname={} -e masterip={} -e slavename={} --name {} --volume-driver netapp --volume {}:/workspace/{} {}".format(label_name,masterip,slave_name,cont_name,vo$
    #return_code = subprocess.call(dock_cmd,shell=True,stderr=subprocess.STDOUT)

