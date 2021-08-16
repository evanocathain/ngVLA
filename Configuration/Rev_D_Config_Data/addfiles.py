# add the config files into one

import sys


# define functions
def readfile(file):
    """Reads a file, adds content to a list, line by line. No character strip"""
    
    filedata = open(file,'r')

    data = filedata.readlines()
    lines = []
    for line in data:
        if line.find('#') == -1: #exclude lines with comments, only take data
            lines.append(line)

    return lines


def addlist(*args):
    """Pass lists as arguments, outputs concatenated list"""

    biglist = []

    for i in args:
        for j in i:
            biglist.append(j)

    return biglist


def writefile(list):
    """Writes lines to a file from a list"""
    
    output = open('rev_d_xyz.txt','w')

    for i in list:
        output.write(i)


# run functions
file1 = readfile('ngvla-revD.core.cfg')
file2 = readfile('ngvla-revD.sba.cfg')
file3 = readfile('ngvla-revD.spiral.cfg')
file4 = readfile('ngvla-revD.mid.cfg')
file5 = readfile('ngvla-revD.lba.cfg')

file0 = addlist(file1,file2,file3,file4,file5)

writefile(file0)