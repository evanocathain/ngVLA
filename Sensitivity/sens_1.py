#!/usr/local/bin/python2.7

#
## Update to sens.py to produce data for ngVLA as input for big_plot.gp

# Load some useful packages
import argparse
import sys
import math as m
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from functions import *

h_over_k = 4.8e-11 # Planck's constant divided by Boltzmann's constant in s*K
kB = 1380.0        # Boltzmann's constant in Jy*m^2*K^-1
nfreqs = 2000      # number of points at which to sample frequency for output plots etc.

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-radius', type=float, dest='radius', help='choose distance from the array centre, in km, for chosen sub-array (default: entire array)', default=1.08)
parser.add_argument('-glgb', nargs=2, type=float, dest='coord', help='enter specific Galactic coordinates to use (default: gl=180.0, gb=-90.0) NOT DONE YET', default=[180.0,-90.0])
parser.add_argument('-gallos', dest='gal', help='choose either 10th, 50th or 90th percentile value for the galaxy contribution to the sky temperature (low/medium/high, default: low)', default='low')
parser.add_argument('-pwv', dest='pwv', help='choose either 5mm, 10mm or 20mm for the PWV value for choosing (a) the zenith opacity, and (b) the atmospheric temperature contribution to the sky temperature (low/medium/high, default: low)', default="low")
parser.add_argument('-tel', dest='tel', help='Which telescopes to include - options are low, mk, ska (meaning SKA1-Mid dishes only), mid (meaning mk+ska), ngvla (default: ngvla)', default="ngvla")
parser.add_argument('-nelements', type=int, dest='nelements', help='choose the inner nelements elements (default: entire array)', default=214)
parser.add_argument('-o', dest='output', help='choose the type of output - plot, file or both (default: plot)', default="plot")
parser.add_argument('-zenith', type=float, dest='zenith', help='choose a zenith angle in degrees (default: 0.0)', default=0.0)
parser.add_argument('--version', action='version', version='%(prog)s 0.0.1')
args = parser.parse_args()

# Set values from command line inputs
tel = args.tel
gl = args.coord[0]
gb = args.coord[1]
gal = args.gal
output = args.output
plot = True
if output != "plot":
    plot = False
zenith = args.zenith
pwv = args.pwv
radius = args.radius
nelements = args.nelements


if str.lower(tel) == "ngvla":
    # Data from https://ngvla.nrao.edu/download/MediaFile/199/original Table 2
    # f = frequency (GHz). s = SEFD (Jy), t = T_sys (K), a = effective area (m^2)
    #Band 1
    f1 = [1.2,2.0,3.5]
    s1 = np.array([1.22,1.44,1.39])
    t1 = np.array([28.1,25.9,23.4])
    # Band 2
    f2 = np.array([3.5,6.6,12.3])
    s2 = np.array([1.75,1.59,1.42])
    t2 = np.array([31.8,28.1,24.6])
    # Band 3
    f3 = np.array([12.3,15.9,20.5])
    s3 = np.array([1.27,1.43,1.91])
    t3 = np.array([24.3,28.3,37.3])
    # Band 4
    f4 = np.array([20.5,26.4,34.0])
    s4 = np.array([1.8,1.72,1.95])
    t4 = np.array([34.1,33.4,37.0])
    # Band 5
    f5 = np.array([30.5,39.2,50.5])
    s5 = np.array([1.91,2.27,5.73])
    t5 = np.array([35.0,42.0,102.0])
    # Band 6
    f6 = np.array([70.0,90.0,116.0])
    s6 = np.array([8.02,4.99,17.45])
    t6 = np.array([124.0,69.0,190.0])
    # lists
    freq = [f1,f2,f3,f4,f5,f6]
    SEFD = [s1,s2,s3,s4,s5,s6]
    T_sys = [t1,t2,t3,t4,t5,t6]

    # Distance to centre of array data
    file = open('../Configuration/ngvla_abs_dist.txt','r')
    filedata = file.readlines()
    lines = []
    for line in filedata:
        lines.append(line.split())

else:
    print("No idea what telescope I'm supposed to be calculating for. FAIL.")
    sys.exit(-1)


# Effective Area
A_eff = []
for i in range(6):
    a = 2*kB*T_sys[i]/SEFD[i]
    A_eff.append(a)

# Sensitivity vs Frequency Plot: A_eff/T_sys for full array
plt.grid(True)
plt.title("A_eff/T_sys vs Frequency")
plt.loglog(f1,A_eff[0]/t1,'r-',label="Band 1")
plt.loglog(f2,A_eff[1]/t2,'g-',label="Band 2")
plt.loglog(f3,A_eff[2]/t3,'b-',label="Band 3")
plt.loglog(f4,A_eff[3]/t4,'c-',label="Band 4")
plt.loglog(f5,A_eff[4]/t5,'m-',label="Band 5")
plt.loglog(f6,A_eff[5]/t6,'y-',label="Band 6")
plt.ylabel("A_eff/T_sys (m^2/K))")
plt.xlabel("Frequency (GHz)")
plt.legend()
plt.show()

# Effective Area per individual dish (frequency dependent)
factor_list = [] 
for i in range(6):
    factors = []
    for j in A_eff[i]:
        f = j/(244*(18**2)+19*(6**2))
        factors.append(f)
    factor_list.append(factors)
# for 18m dishes:
a_18 = []
for i in range(6):
    a_list = []
    for j in factor_list[i]:
        a = j*(18**2)
        a_list.append(a)
    a_18.append(np.array(a_list))
# for 6m dishes
a_6 = []
for i in range(6):
    a_list = []
    for j in factor_list[i]:
        a = j*(6**2)
        a_list.append(a)
    a_6.append(np.array(a_list))

# Sensitivity vs Frequency: Main Array (214*18m)
plt.grid(True)
plt.title("A_eff/T_sys vs Frequency: Main Array")
plt.loglog(f1,a_18[0]*214/t1,'r-',label="Band 1")
plt.loglog(f2,a_18[1]*214/t2,'g-',label="Band 2")
plt.loglog(f3,a_18[2]*214/t3,'b-',label="Band 3")
plt.loglog(f4,a_18[3]*214/t4,'c-',label="Band 4")
plt.loglog(f5,a_18[4]*214/t5,'m-',label="Band 5")
plt.loglog(f6,a_18[5]*214/t6,'y-',label="Band 6")
plt.ylabel("A_eff/T_sys (m^2/K))")
plt.xlabel("Frequency (GHz)")
plt.legend()
plt.show()

# Plot by distance from centre
## find all dishes within given radius
dishes = []
for i in lines:
    if (float(i[2])*.001) <= radius:
        dishes.append(i[1])
## sort into 18m/6m dishes
count_18 = 0
count_6 = 0
for i in dishes:
    if i[0] == 's' and i[1] == '0':
        count_6 += 1
    else:
        count_18 += 1

print("Distance from centre (km): ",radius)
print("Number of elements: ",len(dishes))

# Plot
plt.grid(True)
plt.title("A_eff/T_sys vs Frequency: by dist from centre")
plt.loglog(f1,(a_18[0]*count_18+a_6[0]*count_6)/t1,'r-',label="Band 1")
plt.loglog(f2,(a_18[1]*count_18+a_6[1]*count_6)/t2,'g-',label="Band 2")
plt.loglog(f3,(a_18[2]*count_18+a_6[2]*count_6)/t3,'b-',label="Band 3")
plt.loglog(f4,(a_18[3]*count_18+a_6[3]*count_6)/t4,'c-',label="Band 4")
plt.loglog(f5,(a_18[4]*count_18+a_6[4]*count_6)/t5,'m-',label="Band 5")
plt.loglog(f6,(a_18[5]*count_18+a_6[5]*count_6)/t6,'y-',label="Band 6")
plt.ylabel("A_eff/T_sys (m^2/K))")
plt.xlabel("Frequency (GHz)")
plt.legend()
plt.show()

# Print to files: first 4 bands
full4 = open('ngvla_full_4.txt','w')
main4 = open('ngvla_main_4.txt','w')
core4 = open('ngvla_core_4.txt','w')

for i in range(4):
    f = freq[i]
    a = A_eff[i]
    t = T_sys[i]
    a18 = a_18[i]
    a6 = a_6[i]

    for j in range(3):
        newline_f = str(f[j])+' '+str(a[j]/t[j])+'\n'
        full4.write(newline_f)

        newline_m = str(f[j])+' '+str(a18[j]*214/t[j])+'\n'
        main4.write(newline_m)

        newline_c = str(f[j])+' '+str((a18[j]*count_18+a6[j]*count_6)/t[j])+'\n'
        core4.write(newline_c)

# Print to files: Band 5
full5 = open('ngvla_full_5.txt','w')
main5 = open('ngvla_main_5.txt','w')
core5 = open('ngvla_core_5.txt','w')

a5 = A_eff[4]
a18_5 = a_18[4]
a6_5 = a_6[4]

for j in range(3):
    newline_f = str(f5[j])+' '+str(a5[j]/t5[j])+'\n'
    full5.write(newline_f)

    newline_m = str(f5[j])+' '+str(a18_5[j]*214/t5[j])+'\n'
    main5.write(newline_m)

    newline_c = str(f5[j])+' '+str((a18_5[j]*count_18+a6_5[j]*count_6)/t5[j])+'\n'
    core5.write(newline_c)

# Print to files: Band 6
full6 = open('ngvla_full_6.txt','w')
main6 = open('ngvla_main_6.txt','w')
core6 = open('ngvla_core_6.txt','w')

a6 = A_eff[5]
a18_6 = a_18[5]
a6_6 = a_6[5]

for j in range(3):
    newline_f = str(f6[j])+' '+str(a6[j]/t6[j])+'\n'
    full6.write(newline_f)

    newline_m = str(f6[j])+' '+str(a18_6[j]*214/t6[j])+'\n'
    main6.write(newline_m)

    newline_c = str(f6[j])+' '+str((a18_6[j]*count_18+a6_6[j]*count_6)/t6[j])+'\n'
    core6.write(newline_c)

sys.exit()





