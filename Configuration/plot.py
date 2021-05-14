#!/usr/bin/python

# Evan Keane
# 
# A simple script to plot the SKA elements on a Google Map image

import numpy as np
import gmplot as gm

# LOW
# Read in coords
low = file("coords_LOW.txt", "r")
coords = np.transpose(np.genfromtxt(low))
# Grab a google map
gmap = gm.GoogleMapPlotter(-26.82000, 116.76000, 16)
gmap.plot(coords[3][~np.isnan(coords[3])], coords[2][~np.isnan(coords[2])])
# Overplot points
gmap.scatter(coords[3][~np.isnan(coords[3])], coords[2][~np.isnan(coords[2])], 'k', marker=False)
# Output a html file
gmap.draw("low.html")

# MID
# Read in coords
mid = file("coords_MID.txt", "r")
coords = np.transpose(np.genfromtxt(low))
# Grab a google map
gmap = gm.GoogleMapPlotter(-26.82000, 116.76000, 16)
gmap.plot(coords[3][~np.isnan(coords[3])], coords[2][~np.isnan(coords[2])])
# Overplot points
gmap.scatter(coords[3][~np.isnan(coords[3])], coords[2][~np.isnan(coords[2])], 'k', marker=False)
# Output a html file
gmap.draw("mid.html")
