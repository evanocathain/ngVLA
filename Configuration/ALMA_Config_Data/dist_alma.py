## get distance from centre of array data for alma
## for input to fom_plot.gp, same format as MID_dist_metres, etc

import numpy as np
import matplotlib.pyplot as plt
import sys

def readfile(file):
    """Reads a file, adds content to a list, line by line. W/ character strip"""
    
    filedata = open(file,'r')

    data = filedata.readlines()
    lines = []
    for line in data:
        if line.find('#') == -1: #exclude lines with comments, only take data
            line = line.strip() #remove newlne characters
            line = line.split() #split into list of values, space-delimited
            lines.append(line)

    return lines


def process(list):
    """Sort x,y,z and name of dish into individual lists""" 
    
    X = []
    Y = []
    Z = []
    N = []

    for i in list:
                
        X.append(abs(float(i[0])))
        Y.append(abs(float(i[1])))
        Z.append(abs(float(i[2])))
        N.append(i[4])

    return X,Y,Z


def dist(X,Y,Z,filename):
    """Returns file of absolute distance from origin"""
    
    file = open(filename,'w')
    file.write("##Number abs_dist (m) \n")

    for i in range(len(X)):
        d = np.sqrt(X[i]**2 + Y[i]**2 + Z[i]**2)
        newline = str(i+1)+' '+str(d)+'\n'
        file.write(newline)

    file.close()

def xy(X,Y,Z,filename):
    """Returns file of xy offset from centre"""

    file = open(filename,'w')
    file.write("##Number x_offset y_offset (m) \n")

    for i in range(len(X)):
        newline = str(i+1)+' '+str(X[i])+' '+str(Y[i])+'\n'
        file.write(newline)

    file.close()

inputs = ['alma.cycle7.1.cfg','alma.cycle7.2.cfg','alma.cycle7.3.cfg','alma.cycle7.4.cfg','alma.cycle7.5.cfg','alma.cycle7.6.cfg','alma.cycle7.7.cfg','alma.cycle7.8.cfg','alma.cycle7.9.cfg','alma.cycle7.10.cfg']
outputs = ['alma_dist_metres_7.1.txt','alma_dist_metres_7.2.txt','alma_dist_metres_7.3.txt','alma_dist_metres_7.4.txt','alma_dist_metres_7.5.txt','alma_dist_metres_7.6.txt','alma_dist_metres_7.7.txt','alma_dist_metres_7.8.txt','alma_dist_metres_7.9.txt','alma_dist_metres_7.10.txt']

def main(inputs,outputs):
    
    for i in range(len(inputs)):

        X,Y,Z = process(readfile(inputs[i]))

        xy(X,Y,Z,outputs[i])

main(inputs,outputs)