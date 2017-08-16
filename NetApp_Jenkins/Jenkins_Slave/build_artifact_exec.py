################################################################################
# NetApp-Jenkins Integration Scripts
#          This script was developed by NetApp to help demonstrate NetApp
#          technologies.  This script is not officially supported as a
#          standard NetApp product.
#
# Purpose: Script to execute archiving of build artifacts.
#
#
# Usage:   %> build_actifact_exec.py <args>
#
# Author:  Vishal Kumar S A (vishal.kumarsa@netapp.com)
#          Akshay Patil (akshay.patil@netapp.com)
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
import subprocess
import os
import errno
import re
import time
from datetime import datetime
from subprocess import call


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-art_url','--art_url', help='Artifactory server URL',dest='art_url',required=True)
    parser.add_argument('-art_repo','--art_repo', help='Name of repo in Artifactory to push the zip files ',dest='art_repo',required=True)
    parser.add_argument('-duser','--duser', help='Username for the Repo',dest='duser',required=True)
    parser.add_argument('-dpass','--dpass', help='Password for the Repo',dest='dpass',required=True)
    mntvol = "/tmp/vol1"
    mntclone= "/tmp/vol2"
    parser.add_argument('-z','--zfile', help='Name of the zipfile',dest='zfile',required=True)
    globals().update(vars(parser.parse_args()))
    i = datetime.now()
    foldertime=i.strftime('%Y_%m_%d_%H_%M')
    zfile=foldertime+zfile
    directory=mntvol+'/'+foldertime
    directoryclone=mntclone+'/'+foldertime
    if not os.path.exists(directoryclone):
                os.makedirs(directoryclone)
    if not os.path.exists(directory):
                os.makedirs(directory)
    fullpath = directory+'/'+zfile
    fullpath1= directory+zfile+'/'
    zip_cmd = "zip -r {}/{}/{} {}".format(mntclone,foldertime,zfile,mntclone)
    return_code = subprocess.call(zip_cmd,shell=True)
    own_cmd = "chmod +x {}/{}/{}".format(mntclone,foldertime,zfile)
    return_code = subprocess.call(own_cmd,shell=True)
    mv_cmd = "mv {}/{}/{} {}/{}/".format(mntclone,foldertime,zfile,mntvol,foldertime)
    return_code = subprocess.call(mv_cmd,shell=True)
    art_url1  = re.search('(.+?):',art_url).group(1)  
    pushcmd='curl -u{}:{} -T {} "http://{}/artifactory/{}/{}"'.format(duser,dpass,fullpath,art_url1,art_repo,fullpath)
    return_code = subprocess.call(pushcmd,shell=True)
    #output_clone = subprocess.run("df -HP -t nfs | grep /tmp/vol2", shell=True, stdout=subprocess.PIPE,universal_newlines=True)
    #bashCommand = "df -HP -t nfs | grep /tmp/vol2"
    #out1=subprocess.check_output(['bash','-c', bashCommand])
    #print(out1)
    #out1 = subprocess.Popen(["df","|","grep","/tmp/vol2"],stdout=subprocess.PIPE).communicate()[0]
    #df_cmd= "df | grep /tmp/vol2"
    #out1 = subprocess.Popen(["df","|","grep","/tmp/vol2"],stdout=subprocess.PIPE).communicate()[0]
    #print (out1)
    #out_clonename=re.match(r'\AFilesystem.*[\r\n]+[^/]+/(\S+)', out1)
    #print (out_clonename.group(1))

    print "Contents of baseline zipped and archived successfully"

