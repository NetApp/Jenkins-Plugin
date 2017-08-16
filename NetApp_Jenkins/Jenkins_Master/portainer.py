################################################################################
# NetApp-Jenkins Integration Scripts
#          This script was developed by NetApp to help demonstrate NetApp
#          technologies.  This script is not officially supported as a
#          standard NetApp product.
#
# Purpose: Script to start portainer to monitor the Jenkins Docker Swarm Cluster.
#
#
# Usage:   %> portainer.py
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

    portainer = "docker service create --name portainer --publish 9000:9000 --mount type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock portainer/portainer -H unix:///var/run/docker.sock"

    return_code = subprocess.call(portainer,shell=True,stderr=subprocess.STDOUT)

