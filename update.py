#!/usr/bin/python

import os
import subprocess

dirs = [ 'Projects/kensho' ]

home = os.getenv("HOME")
curdir = os.getcwd()

for dir in dirs:
    d = "%s/%s" % (home, dir) 
    for files in os.listdir(d):
        if os.path.isdir(d + '/' + files + '/.git'):
            print "Updating.  chdir to %s/%s" % (d, files)
            os.chdir(d + '/' + files)
            subprocess.call('git pull -u', shell=True) 
    os.chdir("../..")

os.chdir(curdir)
