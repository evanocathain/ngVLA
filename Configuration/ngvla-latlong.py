#Converts xyz coords to longitude-latitude
#for input into google maps 

#import module
import numpy as np
import csv

#.txt file of xyz data as input
file1 = 'ngvla-xyz.txt'
#.txt file of lat-long data as output
file2 = 'ngvla_latlong.csv'

#taking radius of earth=6378km
R = 6.378e6 #in metres

#to convert to longitude (degrees E)
def long(x,y):
    l_0 =  np.degrees(np.arctan(y/x))
    l_1 = -1*(180 - l_0)
    if abs(l_1) > 180:
        return l_0
    else: 
        return l_1

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

    #open csv file for longlat coords
    f = open(file2,'w',encoding='UTF8',newline='')
    fieldnames = ['name','part','lat','long']
    writer = csv.DictWriter(f,fieldnames=fieldnames)
    writer.writeheader()    

    #read data, get lat & long, write to new file
    for i in lines:
        x = float(i[0])
        y = float(i[1])
        z = float(i[2])
        n = i[4]

        if n[0] == 'm' and n[1] != 'a':
            p = 'Main Array'
        elif n[0] == 's' and n[1] == '0':
            p = 'SBA'
        else:
            p = 'LBA'

        row = {'name':n,'part':p,'lat':lat(z,R),'long':long(x,y)}
        
        writer.writerow(row)

xyz_latlong(file1,file2)