################################################################################
# NetApp-Jenkins Integration Scripts
#          This script was developed by NetApp to help demonstrate NetApp
#          technologies.  This script is not officially supported as a
#          standard NetApp product.
#
# Purpose: Script to create data structure to hold the snapshot names, Extended Choice Parameter Plugin accepts input in the same format.
#
#
# Usage:   %> Create_snap_structure.py <args>
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

import subprocess
from subprocess import call
import base64
import argparse
import sys
import requests
import ssl
import time
import os

requests.packages.urllib3.disable_warnings()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    f = open("snaps2.properties",'w+')            ## THis will write in the Current workspace of the container
    f.write("buildsnaps=Select CheckPoint")  ##KeyValue pair for the extended choice plugin 
    f.close() 



