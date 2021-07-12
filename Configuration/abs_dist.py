# to calculate the absolute distance of a dish from the centre of the array
# calculated from x-y offset from centre

import numpy as np

# input file
file1 = open('ngvla_dist_metres.txt','r')
filedata = file1.readlines()
lines = []
for line in filedata:
    lines.append(line.split())

# output file
file2 = open('ngvla_abs_dist.txt','w')

for i in lines:
    x = abs(float(i[2]))
    y = abs(float(i[3]))
    z = np.sqrt(x**2+y**2)

    newline = i[0]+'\t'+i[1]+'\t'+str(z)+'\n'
    file2.write(newline)

    

    