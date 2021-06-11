#Converts xyz coords to longitude-latitude

#import module
import numpy as np

#.txt file of xyz data as input
file1 = '/home/caoimhe/ngVLA-fork/ngVLA/Configuration/ngvla-xyz.txt'
#.txt file of lat-long data as output
file2 = '/home/caoimhe/ngVLA-fork/ngVLA/Configuration/ngvla-latlong.txt'

#taking radius of earth=6378km
R = 6.378e6 #in metres

#to convert to longitude (degrees E)
def long(x,y):
    l =  -1*(180 - np.degrees(np.arctan(y/x)))
    if l == -180:
        return 0
    else:
        return l

#to convert to latitude (degrees N)
def lat(z,R):
    return 90 - np.degrees(np.arccos(z/R))

#to convert .txt file of xyz data to lat-long
def xyz_latlong(file1,file2):

    #read file of xyz coords
    filedata = open(file1,'r')

    data = filedata.readlines()
    lines = []
    for line in data:
        lines.append(line.split())

    #open file for longlat coords
    result = open(file2,'w')

    #read data, get lat & long, write to new file
    for i in lines:
        x = float(i[0])
        y = float(i[1])
        z = float(i[2])
        name = i[4]

        newline = str(lat(z,R)) + ',' + str(long(x,y)) + '\n'

        result.write(newline)

xyz_latlong(file1,file2)