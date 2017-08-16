################################################################################
# NetApp-Jenkins Integration Scripts
#          This script was developed by NetApp to help demonstrate NetApp
#          technologies.  This script is not officially supported as a
#          standard NetApp product.
#
# Purpose: Script to delete obsolete containers.
#
#
# Usage:   %> build_artifact_container_purge.py <args>
#
# Author:  Akshay Patil (Akshay.Patil@netapp.com)
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
import requests
import subprocess
from subprocess import call

requests.packages.urllib3.disable_warnings()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-cnt','--cont', help='Name of the Container on which workspace is mounted',dest='cont',required=False)
    globals().update(vars(parser.parse_args()))
    dock_cmd = "docker rm -f {}".format(cont)
    return_code = subprocess.call(dock_cmd,shell=True)
    print "Temporary container deleted successfully"

