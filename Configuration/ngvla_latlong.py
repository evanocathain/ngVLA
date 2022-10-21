#Converts xyz coords to longitude-latitude
#for input into google maps 

## *NB* This code uses Geocentric Latitude instead of Geodetic Latitude, so the latitudes given are off by a bit from actual values

#import module
import numpy as np
import csv
import sys

## Old files: Rev C
#.txt file of xyz data as input
file1_1 = 'ngvla-xyz.txt' #full array
file2_1 = 'ngVLA-config-revC_forweb/ngvla-core-revC.cfg' #core
file3_1 = 'ngVLA-config-revC_forweb/ngvla-plains-revC.cfg' #plains
file4_1 = 'ngVLA-config-revC_forweb/ngvla-mid-subarray-revC.cfg' #mid
file5_1 = 'ngVLA-config-revC_forweb/ngvla-sba-revC.cfg' #sba
file6_1 = 'ngVLA-config-revC_forweb/ngvla-lba-revC.cfg' #lba
#.txt file of lat-long data as output
file1_2 = 'ngvla_latlong.csv'
file2_2 = 'google_maps_files/core.csv'
file3_2 = 'google_maps_files/plains.csv'
file4_2 = 'google_maps_files/mid.csv'
file5_2 = 'google_maps_files/sba.csv'
file6_2 = 'google_maps_files/lba.csv'

## New files: Rev D
#.txt file of xyz data as input
file1_1 = 'Rev_D_Config_Data/ngvla-revD.core.cfg' #core
file2_1 = 'Rev_D_Config_Data/ngvla-revD.lba.cfg' #lba
file3_1 = 'Rev_D_Config_Data/ngvla-revD.spiral.cfg' #spiral
file4_1 = 'Rev_D_Config_Data/ngvla-revD.mid.cfg' #mid
file5_1 = 'Rev_D_Config_Data/ngvla-revD.sba.cfg' #sba
#.txt file of lat-long data as output
file1_2 = 'google_maps_files/Core.csv'
file2_2 = 'google_maps_files/Lba.csv'
file3_2 = 'google_maps_files/Spiral.csv'
file4_2 = 'google_maps_files/Mid.csv'
file5_2 = 'google_maps_files/Sba.csv'

#sba = small baseline array of 6m antennas
#core = 18m antennas within ~ 2.2 km of the array center
#spiral = 18m antennas from 2.2km to 20 km
#mid = 18m antennas from 30km to 700km
#lba = 18m antennas on continental scales

#to convert to longitude (degrees E)
def long(x,y):
    l_0 =  np.degrees(np.arctan(y/x))
    l_1 = -1*(180 - l_0)
    if abs(l_1) > 180:
        return l_0
    else: 
        return l_1

#to convert to latitude (degrees N)
def lat(x,y,z):
    h = np.sqrt(x**2 + y**2)
    return np.degrees(np.arctan(z/h)))

#to convert .txt file of xyz data to lat-long
def xyz_latlong(file1,file2):

    #read file of xyz coords
    filedata = open(file1,'r')

    data = filedata.readlines()
    lines = []
    for line in data:
        if line.find('#') == -1:
            lines.append(line.split())

    #open csv file for longlat coords
    f = open(file2,'w',encoding='UTF8',newline='')
    fieldnames = ['name','lat','long']
    writer = csv.DictWriter(f,fieldnames=fieldnames)
    writer.writeheader()    

    #read data, get lat & long, write to new file
    for i in lines:
        x = float(i[0])
        y = float(i[1])
        z = float(i[2])
        n = i[4]

        row = {'name':n,'lat':lat(z,R),'long':long(x,y)}
        
        writer.writerow(row)

#xyz_latlong(file2_1,file2_2)
#xyz_latlong(file3_1,file3_2)
#xyz_latlong(file4_1,file4_2)
#xyz_latlong(file5_1,file5_2)
#xyz_latlong(file1_1,file1_2)
