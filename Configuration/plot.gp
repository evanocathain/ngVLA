# Evan Keane
# 08/05/2017
#
# A very simple gnuplot script to plot the cumulative number 
# of dishes/stations, collecting area etc. for SKA1 Mid and Low.
# 
# Update 31/05/2021
# Adding in ngVLA
#

# Plot formatting
set key top left box
set logscale x
set mxtics 10
set mytics 2
set grid
set grid mxtics
set grid mytics

# MID
set ylabel "Number of dishes"
set xlabel "Distance from array centre (km)"
plot "< awk '{print 0.001*sqrt($3*$3+$4*$4)|\"sort -g -k1\"}' MID_dist_metres.txt | cat -n" u 2:1 wi li title "SKA1-Mid Total"
replot "< awk '{if (substr($2,0,1)==\"M\") print 0.001*sqrt($3*$3+$4*$4)|\"sort -g -k1\"}' MID_dist_metres.txt | cat -n" u 2:1 wi li title "MeerKAT Dishes"
replot "< awk '{if (substr($2,0,1)==\"S\") print 0.001*sqrt($3*$3+$4*$4)|\"sort -g -k1\"}' MID_dist_metres.txt | cat -n" u 2:1 wi li title "SKA1 Dishes"

pause mouse

# LOW
set ylabel "Number of stations"
set xlabel "Distance from array centre (km)"
plot "< awk '{print 0.001*sqrt($3*$3+$4*$4)|\"sort -g -k1\"}' LOW_dist_metres.txt | cat -n" u 2:1 wi li title "SKA1-Low Total"

pause mouse

# ngVLA
set ylabel "Number of dishes"
set xlabel "Distance from array centre (km)"
plot "< awk '{print 0.001*sqrt($3*$3+$4*$4)|\"sort -g -k1\"}' ngvla_dist_metres.txt | cat -n" u 2:1 wi li title "ngVLA Main Array Total", "< awk 'NR<=214{print 0.001*sqrt($3*$3+$4*$4)|\"sort -g -k1\"}' ngvla_dist_metres.txt | cat -n" u 2:1 wi li title "ngVLA Long Baseline Array Total"

pause mouse
