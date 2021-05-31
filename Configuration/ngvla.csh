#!/bin/csh

set phase_centre_x = -1603200.000 # arbitray choice, near m01
set phase_centre_y = -5040600.000 # arbitray choice, near m01

awk -v phase_centre_x=$phase_centre_x -v phase_centre_y=$phase_centre_y 'NR>2{print $5,$1-phase_centre_x,$2-phase_centre_y}' ngvla-revC.cfg > ngvla_dist_metres.txt

