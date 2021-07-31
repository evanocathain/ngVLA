set term x11 font 'Times, 10'

#telescope              #max frequency (GHz)       #Corresponding to ngVLA band
# SKA1-Mid                      50                              5
# SKA1-Mid SKA dishes only      50                              5
# MeerKAT                       50                              5
# FAST                          3                               1   **
# Arecibo                       10                              2   **
# Effelsberg                    86                              6   **
# GBT (GBNCC)                   *                               *
# uGMRT                         *                               *
# Parkes                        26                              4   **
# LOFAR                         *                               *
# ALMA                          950 ***                         6 only ***

# * : currently not defined here
# ** : currently only defined here for Band 1. 
# *** : currently not defined here: to be added

# Get gain for ngVLA, SKA, MeerKAT from Sensitivity/get_gain.py: input the desired frequency and it outputs A_eff/T_sys for that freq
# For each band, change frequency, gain, title & labels of plot and name of output file (fomplot_2.ps for Band 2, etc)
# Label positions on graph need to be changed manually each time. 
# Also: add in equation for survey speed calculation

# constants, functions etc.
pi      = 3.14159
Tsky(x) = 25.2*(0.408/x)**2.75   # x = freq in GHz

fullska(x) = 1.0e+6/(30.0+Tsky(x))

## The telescopes ##
# First the non-SKA single dish components. 
# Let's go for decreasing dish diameter


# FAST
fast_func(x)  = 40000.0/(20.0+Tsky(x))
fast(x) = x>=1.530 ? 1/0 : x<=1.230 ? 1/0 : fast_func(x)

# Arecibo
ao_func(x)  = 28704.0/(24.0+Tsky(x)) 
ao_centre(x) = x>=1.57 ? 1/0 : x<=1.27 ? 1/0 : ao_func(x) # 10.4 K/Jy
ao_ring(x) = x>=1.57 ? 1/0 : x<=1.27 ? 1/0 : ao_func(x)*(8.2/10.4) # 8.2 K/Jy

# Effelsberg MB-7 HTRU-N
eff_func(x)  = 0.525*pi*100**2*0.25/(21.0+Tsky(x))
eff_centre(x) = x>=1.4875 ? 1/0 : x<=1.2325 ? 1/0 : eff_func(x)
eff_ring(x) = x>=1.4875 ? 1/0 : x<=1.2325 ? 1/0 : eff_func(x)*(0.455/0.525)

# GBT - GBNCC
gbt_func(x)  = 5520/(23.0+Tsky(x)) # 2 K/Jy
gbt(x) = x>=0.400 ? 1/0 : x<=0.300 ? 1/0 : gbt_func(x)

# Parkes MB-13 HTRU/SUPERB
pks_func(x)  = 0.86*0.86*pi*64**2*0.25/(23.0+Tsky(x))
pks_centre(x) = x>=1.582 ? 1/0 : x<=1.182 ? 1/0 : pks_func(x)            # 0.735 K/Jy
pks_inner(x) = x>=1.582 ? 1/0 : x<=1.182 ? 1/0 : pks_func(x)*0.690/0.735 # 0.690 K/Jy
pks_outer(x) = x>=1.582 ? 1/0 : x<=1.182 ? 1/0 : pks_func(x)*0.581/0.735 # 0.581 K/Jy

# Next add in aperture arrays
#

# uGMRT

# UTMOST
utmost_func(x)  = 0.5*18200.0/(200.0+Tsky(x))
utmost(x) = x>=0.86 ? 1/0 : x<=0.830 ? 1/0 : utmost_func(x) # NB the BW is so narrow it doesn't display

# CHIME
# https://arxiv.org/pdf/1609.00929.pdf
chime_func(x)  = 5520.0/(50.0+Tsky(x))
chime(x) = x>=0.8 ? 1/0 : x<=0.4 ? 1/0 : chime_func(x)

# LOFAR LOTAS
# lt 8

# MWA

# Plot properties
set key bottom right box
unset key
set ylabel "1.4-GHz PSR Survey Speed FoM (arb. units)" font 'Times, 15'
set xlabel "Distance from array centre (m)" font 'Times, 15'
set logscale xy
set xrange [20:4000]
set yrange [0:2.0e4]
set grid mxtics mytics #lt -1 lc rgb 'gray90'
set grid xtics ytics #lt -1 lc rgb 'gray70'
set xtics font "Times, 15"
set ytics font "Times, 15"
#set arrow from 500,1.0e4 to 500,10 nohead lc rgb 'red' lt -1
#set label at 510,5000 textcolor rgb 'red' "SKA1-Mid PSR Search Radius" font "Times, 15"

# Plot the non-SKA components
plot "<echo '250.0'" u 1:((19.0*fast(1.4)**2)/(125.50**2)) w p lt 1 pt 5 ps 2, \
"<echo '150'" u 1:(((ao_centre(1.4)**2)/(95.6**2))+((6.0*ao_ring(1.4)**2)/((95.6*8.2/10.4)**2))) w p lt 6 pt 5 ps 2, \
"<echo '50'"  u 1:(((eff_centre(1.4)**2)/(0.525*$1**2))+((6.0*eff_ring(1.4)**2)/(0.455*$1**2))) w p lt 4 pt 5 ps 2, \
"<echo '32'"  u 1:(((pks_centre(1.4)**2)/(0.86*0.86*$1**2))+((6.0*pks_inner(1.4)**2)/((0.86*0.86*(0.690/0.735)*$1**2)))++((6.0*pks_outer(1.4)**2)/((0.86*0.86*(0.581/0.735)*$1**2)))) w p lt 5 pt 5 ps 2, \
"<awk '{print $0,sqrt($3*$3+$4*$4)}' ../Configuration/MID_dist_metres.txt | sort -g -k5 | awk -v g=0.0 -v mkgain=6.34 -v skagain=10.16 '{if (substr($2,1,1)==\"M\") g+=mkgain; if (substr($2,1,1)==\"S\") g+=skagain; fov=1.0/(7.5*7.5); if (10000/($5*$5) < fov) fov=10000/($5*$5); print $5,g*g*fov}'" w li lt -1, \
"<awk '{print $0,sqrt($3*$3+$4*$4)}' ../Configuration/MID_dist_metres.txt | sort -g -k5 | awk -v g=0.0 -v mkgain=6.34 -v skagain=10.16 '{if (substr($2,1,1)==\"M\") g+=mkgain; if (substr($2,1,1)==\"S\") g+=skagain; fov=1.0/(7.5*7.5); if (1500/($5*$5) < fov) fov=1500/($5*$5); print $5,g*g*fov}'" w li lt -1, \
"<awk '{print $0,sqrt($3*$3+$4*$4)}' ../Configuration/MID_dist_metres.txt | sort -g -k5 | awk -v g=0.0 -v mkgain=6.34 -v skagain=10.16 '{if (substr($2,1,1)==\"M\") g+=mkgain; if (substr($2,1,1)==\"S\") g+=skagain; fov=1.0/(7.5*7.5); if (750/($5*$5) < fov) fov=750/($5*$5); print $5,g*g*fov}'" w li lt -1, \
"<awk '{print $0,sqrt($3*$3+$4*$4)}' ../Configuration/MID_dist_metres.txt | sort -g -k5 | awk -v g=0.0 -v mkgain=6.34 '{if (substr($2,1,1)==\"M\") {g+=mkgain; fov=1.0/(6.75*6.75); if (10000/($5*$5) < fov) fov=10000/($5*$5); print $5,g*g*fov}}'" w li lt 2, \
"<awk '{print $0,sqrt($3*$3+$4*$4)}' ../Configuration/MID_dist_metres.txt | sort -g -k5 | awk -v g=0.0 -v mkgain=6.34 '{if (substr($2,1,1)==\"M\") {g+=mkgain; fov=1.0/(6.75*6.75); if (400/($5*$5) < fov) fov=400/($5*$5); print $5,g*g*fov}}'" w li lt 2, \
"<awk '{print $0,sqrt($3*$3+$4*$4)}' ../Configuration/ngvla_dist_metres.txt | sort -g -k5 | awk -v g=0.0 -v nggain=8.78 '{g+=nggain; fov=1.0/(9*9); if ((50/($5*$5)) < fov) fov=50/($5*$5); print $5,g*g*fov}'" w li lt 7


#plot "<echo '250.0'" u 1:((19.0*fast(1.4)**2)/(150.0**2)) w p lt 1 pt 5 ps 2, \
#"<echo '150'" u 1:(((ao_centre(1.4)**2)+(6.0*ao_ring(1.4)**2))/(100.0**2)) w p lt 6 pt 5 ps 2, \
#"<echo '50'"  u 1:(((eff_centre(1.4)**2)+(6.0*eff_ring(1.4)**2))/($1**2)) w p lt 4 pt 5 ps 2, \
#"<echo '32'"  u 1:(((pks_centre(1.4)**2)+(6.0*pks_inner(1.4)**2)+(6.0*pks_outer(1.4)**2))/($1**2)) w p lt 5 pt 5 ps 2, \
#"<awk '{print $0,sqrt($3*$3+$4*$4)}' ../Configuration/MID_dist_metres.txt | sort -g -k5 | awk -v g=0.0 -v mkgain=6.34 -v skagain=10.16 '{if (substr($2,1,1)==\"M\") g+=mkgain; if (substr($2,1,1)==\"S\") g+=skagain; print $5,g*g*1500.0/($5*$5)}'" w li lt -1, \
#"<awk '{print $0,sqrt($3*$3+$4*$4)}' ../Configuration/MID_dist_metres.txt | sort -g -k5 | awk -v g=0.0 -v mkgain=6.34 '{if (substr($2,1,1)==\"M\") {g+=mkgain; print $5,g*g*400.0/($5*$5)}}'" w li lt 2

# for Aeff(r) use this
#"<awk '{print $0,sqrt($3*$3+$4*$4)}' ../Configuration/MID_dist_metres.txt | sort -g -k5 | awk -v g=0.0 -v mkgain=6.34 -v skagain=10.16 '{if (substr($2,1,1)==\"M\") g+=mkgain; if (substr($2,1,1)==\"S\") g+=skagain; print $5,g}'" w p


# SKA1-Mid dish gain (50 pct GALLOS and PWV) at 1.4 GHz -> 10.16 m^2/K
# MeerKAT  dish gain (50 pct GALLOS and PWV) at 1.4 GHz -> 6.34 m^2/K

#plot '-'
#250.0 (fast(1.4)**2)*19.0							# FAST MB-19
#150.0 ((ao_centre(1.4)**2)+(6.0*ao_ring(1.4)**2))				# Arecibo PALFA MB-7
#e
#50 (eff_centre(1.4)**2)+(6.0*eff_centre(1.4)**2)				# Eff MB-7
#e
#32 (pks_centre(1.4)**2)+(6.0*pks_inner(1.4)**2)+(6.0*pks_outer(1.4)**2)	# PKS MB-13
#e


#plot '-' using 1:2 title "FAST TEST1" with points#, \
#     '-' using 1:2 title "FAST TEST2" with points
#     	 0.150 10
#     	 0.150 (fast(1.4)**2)*19.0*225**(-2)
#EOF
#     	 0.20 20
#     	 0.150 fast(1.4)**2*19.0*((4.0/pi)*fast(1.4))**(-2) 
#EOF
#plot fast(1.4)**2*19.0*((4.0/pi)*fast(1.4))**(-2) wi li lt 1 title "FAST MB-19"
#, ao_centre(x) wi li lt 6 title "Arecibo MB-7", ao_ring(x) wi li lt 6 notitle, eff_centre(x) wi li lt 4 title "Effelsberg MB-7", eff_ring(x) wi li lt 4 notitle, gbt(x) wi li lt 7 title "GBT", pks_centre(x) wi li lt 5 title "Parkes MB-13", pks_inner(x) wi li lt 5 notitle, pks_outer(x) wi li lt 5 notitle, chime(x) wi li lt 9 title "CHIME", "lofar" u 1:(12.0*$2/(140.0+Tsky($1))) wi li lt 3 title "LOFAR Superterp", "lofar" u 1:((66.0*$2)/(140.0+Tsky($1))) wi li lt 3 title "LOFAR Core", "lofar" u 1:((66.0*$2+14.0*2.0*$2)/(140.0+Tsky($1))) wi li lt 3 title "LOFAR NL" 

# UTMOST - special case as BW is so narrow
#set style line 1 lc -1 lw 1 dashtype 2
#set style line 2 lc -1 lw 1
#set style line 3 lc rgb "#66CDAA" dashtype 2 lw 1
#set style line 4 lc rgb "#66CDAA" lw 1
#set style line 5 lc rgb "#FA8072" dashtype 2 lw 1
#set style line 6 lc rgb "#FA8072" lw 1
set arrow from 0.830,91 to 0.860,91 nohead lt 8 front

# Label the non-SKA single dish components
#set label "FAST MB-19" front at 200,2500 font "Times, 15"
set label "FAST MB-19" front at 250,3500 #font "Times, 15"
#set label "Arecibo MB-7" front at 120,550 font "Times, 15"
set label "Arecibo MB-7" front at 120,800 #font "Times, 15"
#set label "Effelsberg MB-7" front at 40,60 font "Times, 15"
set label "Effelsberg MB-7" front at 30,210 #font "Times, 15"
#set label "GBT" front at 0.32, 70
#set label "Parkes MB-13" front at 30,100 font "Times, 15"
set label "Parkes MB-13" front at 22,100 #font "Times, 15"
#set label "UTMOST" front at 0.7,80
#set label "CHIME" front at 0.42,100
#set label "LOFAR (Superterp, core, NL)" front at 0.25,20

# Overplot the SKA-Mid components
#replot "skamid_500m_50pct" u 1:2 wi li lt -1 title "SKA1-Mid inner 1 km", "skamid_20km_50pct" u 1:2 wi li lt -1 title "SKA1-Mid inner 20 km", "skamid_full_50pct" u 1:2 wi li lt -1 title "SKA1-Mid (full)"
# MeerKAT alone
#replot "mk_500m_50pct" u 1:($2*64.0/38.0) wi li lt 2 title "MeerKAT (full)", "mk_500m_50pct" u 1:2 wi li lt 2 title "MeerKAT inner 1 km"

# Label the SKA-Mid components
set label "SKA1-Mid 10000 beams" front at 1300,7000 #font "Times, 15"
set label "SKA1-Mid 1500 beams" front at 700,3000 #font "Times, 15"
set label "SKA1-Mid 750 beams" front at 600,600 #font "Times, 15"
set label "MeerKAT 10000 beams" front at 900,300 textcolor lt 2 #font "Times, 15"
set label "MeerKAT 400 beams" front at 800,60 textcolor lt 2 #font "Times, 15"
set label "ngVLA (50 beams)" front at 200,200  textcolor lt 7 font "Times,15"
set title "Survey Speed at 1.4GHz (ngVLA Band 1)" font "Times, 22"
replot

set term postscript enhanced color solid font 'Times, 10'
set output "fomplot.ps
replot