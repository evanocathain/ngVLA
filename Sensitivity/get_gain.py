## get the gain from Butler Data and sens.py
# gain  = A_eff/T_sys

import numpy as np
import matplotlib.pyplot as plt
import ngvla_data_1 as d
import functions as s

# A program for linear plots to compute the y value for a given x value
def get_y(x,y,xvalue):

    if len(x) != len(y):
        print("Input Error: x,y values of different lengths")

    else:
        for i in range(len(x)):
            if x[i] == xvalue:
                yvalue = y[i]
            elif x[i] < xvalue and x[i+1] > xvalue:
                x1, x2 = x[i], x[i+1]
                y1, y2 = y[i], y[i+1]

                frac = (abs(xvalue-x1))/(abs(x2-x1))
                yvalue = y1 + frac*(y2-y1)
        
        return yvalue

# ngVLA
xval = eval(input("Choose Frequency (GHz): "))
if xval > 50 and xval < 70:
    print("Undefined for 50-70 GHz")

f, gain = d.process("sensitivity")
print("ngVLA: ", get_y(f,gain,xval))

#get values from sens.py
def func(telescope):
    Tsys, f = s.get_tsys(telescope,"low","low",0.0,False)
    Aeff = s.get_aeff(telescope,False)
    g = []
    for i in range(len(f)):
        a = Aeff(f[i])
        t = Tsys(f[i])
        g.append(a/t)
    return f, g

# SKA
f, gain = func("SKA")
print("SKA: ", get_y(f,gain,xval))

# MeerKAT
f, gain = func("MeerKAT")
print("MeerKAT: ", get_y(f,gain,xval))