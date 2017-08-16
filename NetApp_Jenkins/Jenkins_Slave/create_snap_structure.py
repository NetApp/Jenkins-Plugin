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
    f.write("buildsnaps=Select Snapshot")  ##KeyValue pair for the extended choice plugin 
    f.close() 



