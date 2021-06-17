set term x11 font 'Times, 10'

# SKA1-Mid
# SKA1-Mid SKA dishes only
# MeerKAT
# FAST
# Arecibo
# Effelsberg
# GBT (GBNCC)
# uGMRT
# Parkes
# LOFAR

# constants, functions etc.
pi      = 3.14159
Tsky(x) = 25.2*(0.408/x)**2.75   # x = freq in GHz

fullska(x) = 1.0e+6/(30.0+Tsky(x))

## The telescopes ##
# First the non-SKA single dish components. 
# Let's go for decreasing dish diameter
#

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
set ylabel "A_{eff}/T_{sys} (m^2/K)" font 'Times, 15'
set xlabel "Frequency (GHz)" font 'Times, 15'
set logscale xy
set xrange [0.050:50.0]
set yrange [5:3000]
set grid mxtics mytics #lt -1 lc rgb 'gray90'
set grid xtics ytics #lt -1 lc rgb 'gray70'
set xtics font "Times, 15"
set ytics font "Times, 15"

# Plot the non-SKA components
plot fast(x) wi li lt 1 title "FAST MB-19", ao_centre(x) wi li lt 6 title "Arecibo MB-7", ao_ring(x) wi li lt 6 notitle, eff_centre(x) wi li lt 4 title "Effelsberg MB-7", eff_ring(x) wi li lt 4 notitle, gbt(x) wi li lt 7 title "GBT", pks_centre(x) wi li lt 5 title "Parkes MB-13", pks_inner(x) wi li lt 5 notitle, pks_outer(x) wi li lt 5 notitle, chime(x) wi li lt 9 title "CHIME", "lofar" u 1:(12.0*$2/(140.0+Tsky($1))) wi li lt 3 title "LOFAR Superterp", "lofar" u 1:((66.0*$2)/(140.0+Tsky($1))) wi li lt 3 title "LOFAR Core", "lofar" u 1:((66.0*$2+14.0*2.0*$2)/(140.0+Tsky($1))) wi li lt 3 title "LOFAR NL"

# Not sure what/how to add uGMRT yet, for pulsar applications
# Coherent GMRT
#, "ugmrt" u ($1*0.001):(30*2760*$4)/($2+$3+Tsky($1*0.001))) wi li title "uGMRT"
# Incoherent GMRT a la GHRSS
#, "ugmrt" u ($1*0.001):((sqrt(30)*2760*$4)/($2+$3+Tsky($1*0.001))) wi li title "uGMRT"
# According to this http://www.gmrt.ncra.tifr.res.in/gmrt_hpage/Users/doc/GMRT-specs.pdf can do 4 beams for incoherent or coherent. It seems the GHRSS did 1 x 32-MHz beam. Coherent gain is v impressive but SS is 30*(25m/25km)^2 is 3*10^-5 worse than for incoherent mode. If it could do lots of beams it would be awesome, especially in the SKA Band 1 region.

# UTMOST - special case as BW is so narrow
#set style line 1 lc -1 lw 1 dashtype 2
#set style line 2 lc -1 lw 1
#set style line 3 lc rgb "#66CDAA" dashtype 2 lw 1
#set style line 4 lc rgb "#66CDAA" lw 1
#set style line 5 lc rgb "#FA8072" dashtype 2 lw 1
#set style line 6 lc rgb "#FA8072" lw 1
set arrow from 0.830,91 to 0.860,91 nohead lt 8 front

# Label the non-SKA single dish components
set label "FAST MB-19" front at 1.15,2100
set label "Arecibo MB-7" front at 1.6,1000
set label "Effelsberg MB-7" front at 1.5,175
set label "GBT" front at 0.32, 70
set label "Parkes MB-13" front at 1.7,100
set label "UTMOST" front at 0.7,80
set label "CHIME" front at 0.42,100
set label "LOFAR HBA (Superterp, core, NL)" front at 0.25,20

# Overplot the SKA-Mid components
replot "skamid_500m_50pct" u 1:2 wi li lt -1 title "SKA1-Mid inner 1 km", "skamid_20km_50pct" u 1:2 wi li lt -1 title "SKA1-Mid inner 20 km", "skamid_full_50pct" u 1:2 wi li lt -1 title "SKA1-Mid (full)"
# MeerKAT alone
replot "mk_500m_50pct" u 1:($2*64.0/38.0) wi li lt 2 title "MeerKAT (full)", "mk_500m_50pct" u 1:2 wi li lt 2 title "MeerKAT inner 1 km"
#replot "skamid_500m_50pct" u 1:2 wi li lt -1 title "SKA1-Mid (SKA1+MeerKAT) inner 1 km", "mk_500m_50pct" u 1:($2*64.0/38.0) wi li lt 2 title "MeerKAT (full)", "mk_500m_50pct" u 1:2 wi li lt 2 title "MeerKAT inner 1 km", "mid_500m_50pct" u 1:2 wi li title "SKA1 dishes only inner 1 km"

# Label the SKA-Mid components
set label "SKA1-Mid (incl. MeerKAT, 1 km, 20 km, full)" front at 4,1600
set label "MeerKAT (1 km, full)" front at 3.3,350

# Overplot the SKA-Low components
replot "ska1-low_full" u ($1):($2/(40.0+Tsky($1))) wi li lt 8, "ska1-low_full" u ($1):((404.0/512.0)*$2/(40.0+Tsky($1))) wi li lt 8, "ska1-low_full" u ($1):((224.0/512.0)*$2/(40.0+Tsky($1))) wi li lt 8

# Label the SKA-Low components
set label "SKA1-Low (1km, 20km, full)" front at 0.092,210 textcolor lt 8


# Full SKA comparison curves
replot fullska(x) lt 0, 0.5*fullska(x) lt 0, 0.1*fullska(x) lt 0, 0.01*fullska(x) lt 0
# Full SKA comparison labels
set label "100% SKA/(30 K + Tsky)" front at 0.11, 750 rotate by 65 textcolor lt 0
set label "50% SKA/(30 K + Tsky)" front at 0.14, 750 rotate by 65 textcolor lt 0
set label "10% SKA/(30 K + Tsky)" front at 0.08, 30 rotate by 65 textcolor lt 0
set label "1% SKA/(30 K + Tsky)" front at 0.15, 15 rotate by 65 textcolor lt 0
replot

set term postscript enhanced color solid font 'Times, 10'
set output "bigplot.ps
replot