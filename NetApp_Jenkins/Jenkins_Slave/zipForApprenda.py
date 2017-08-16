################################################################################
# NetApp-Jenkins Integration Scripts
#          This script was developed by NetApp to help demonstrate NetApp
#          technologies.  This script is not officially supported as a
#          standard NetApp product.
#
# Purpose: Script to create a new Jenkins slave container with a NetApp volume/clone mounted.
#
#
# Usage:   %> zipForApprenda.py <args>
#
# Author:   Shrivatsa Upadhye (shrivatsa.upadhye@netapp.com)
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
from subprocess import call

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-ptz','--pathtozip', help='Path to zip inside the workspace',dest='pathtozip',required=True)
    parser.add_argument('-zip','--zipfile', help='Name of the zipfile',dest='zfile',required=True)

    globals().update(vars(parser.parse_args()))

    print "Unzipping the File..."
    tempDirName = "temp"
    tempdir_cmd = "mkdir {}/{}".format(pathtozip,tempDirName)
    return_code = subprocess.call(tempdir_cmd,shell=True)

    templocation = pathtozip + tempDirName 
    unzip_cmd = "unzip {}{} -d {}/".format(pathtozip,zfile,templocation)
    return_code = subprocess.call(unzip_cmd,shell=True)
    copywar_cmd = "cp /tmp/vol2/war/target/jenkins.war {}/wars/jenkins.war/".format(templocation)
    return_code = subprocess.call(copywar_cmd,shell=True)
   
    zip_cmd = "zip -r {}{} *".format(pathtozip,zfile,tempDirName)
    return_code = subprocess.call(zip_cmd,shell=True,cwd=templocation)
    
    deleteTempDir_cmd = "rm -rf {}".format(templocation)
    return_code = subprocess.call(deleteTempDir_cmd,shell=True)

    gitemail = "test@netapp.com"
    gituser = "Gituser"
    gitconfig_cmd = "git config --global user.email {}".format(gitemail)
    return_code = subprocess.call(gitconfig_cmd,shell=True)
    
    gitconfiguser_cmd = "git config --global user.name {}".format(gituser)
    return_code = subprocess.call(gitconfiguser_cmd,shell=True)

    gitadd_cmd = "git add -A"
    return_code = subprocess.call(gitadd_cmd,shell=True)

    gitcommit_cmd = "git commit -m 'Pushed Updated Deployment Zip'"
    return_code = subprocess.call(gitcommit_cmd,shell=True)

    print "Target War File copied... Uploading the file to Repository !!"

