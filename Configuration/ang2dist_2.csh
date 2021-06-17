#!/bin/csh

# pi*radius of earth = 20 037.3921 kilometers
set degtokm = `echo 20037.3921 180.0 | awk '{print $1/$2}'`
#echo $degtokm

# Output the configuration with x-y offsets from 
# array centres in metres
# nglva - ascii
awk -v fac=$degtokm 'NR==2{clong=$3;clat=$4}''NR>2{print $1,$2,cos(clat*3.14159/180.0)*($3-clong)*1000*fac,($4-clat)*1000*fac}' coords_ngvla.txt > ngvla_dist_metres.txt
# ngvla - csv
awk -v fac=$degtokm 'NR==2{clong=$3;clat=$4;print "Number,Name,x,y"}''NR>2{print $1","$2","cos(clat*3.14159/180.0)*($3-clong)*1000*fac","($4-clat)*1000*fac}' coords_ngvla.txt > ngvla_dist_metres.csv
