#!/usr/bin/env python3
"""
Script to find the project that a file is in.
A project is defined to be a folder containing a .git folder
If we are in /home/user1/project1/submodules/ project2 /file.txt, the project is defined to be project2
"""

import os
from pathlib import Path
import subprocess
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')

def getgitproject_main(filename):
    # use cwd if no filename specified
    if filename is None:
        filename = os.getcwd()

    # convert to str in case inputted as pathlib.Path
    filename = str(filename)

    # get absolute path of filename
    # use PWD to ensure that we don't go over links
    # so if /home/user1/dir1/file1.txt is a symbolic link to /home/user1/dir2/file1.txt
    # we will consider the path /home/user1/dir1/file1.txt
    filename = os.path.abspath(os.path.join(os.getenv('PWD'), filename))

    # first get lowest directory
    if os.path.isfile(filename):
        filename = os.path.dirname(filename)

    # now go through one directory at a time and see if .git exists
    projectdir = None
    # note that Python sets os.path.dirname('/') = '/' so I use that as the terminal condition
    while os.path.dirname(filename) != filename:
        if os.path.exists(os.path.join(filename, '.git')) is True:
            return(filename)
        else:
            filename = os.path.dirname(filename)

    raise ValueError('Filename is not contained within a git project. Filename: ' + filename + '.')


def getgitproject_argparse():
    import argparse
    
    parser=argparse.ArgumentParser()
    parser.add_argument("filename", type = str, nargs = '?', help = 'Function will find project containing filename by looking for a .git folder.')
    parser.add_argument("--usecwd", action = 'store_true', help = 'Use current working directory as the filename.')
    
    
    args=parser.parse_args()

    if args.usecwd is True:
        filename = os.getcwd()
    else:
        if args.filename is None:
            raise ValueError('If you do not specify --usecwd, you must specify a filename.')
        filename = args.filename[0]

    print(getgitproject_main(filename))


# Test:{{{1
def test_getgitproject():
    if getgitproject_main(__projectdir__) != str(__projectdir__):
        raise ValueError('Error in getgitproject_main.')
    if getgitproject_main(__projectdir__ / 'getgitproject_func.py') != str(__projectdir__):
        raise ValueError('Error in getgitproject_main.')

    # next step only works if this project is not saved in a git folder
    try:
        getgitproject_main(__projectdir__ / '../')
        # this should return an error
        worked = True
    except Exception:
        worked = False
    if worked is True:
        raise ValueError('Error in getgitproject_main.')

    # now test the argparse function
    gitproject = subprocess.check_output([__projectdir__ / 'run/getgitproject_argparse.py', 'hello'], encoding = 'UTF-8')
    gitproject = str(gitproject[: -1])
    if not gitproject == str(__projectdir__):
        raise ValueError('Error in getgitproject_argparse.')
