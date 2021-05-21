# Load some useful packages
#import argparse
#import sys
import math as m
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

h_over_k = 4.8e-11 # Planck's constant divided by Boltzmann's constant in s*K
nfreqs = 2000      # number of points at which to sample frequency for output plots etc.

def get_aeff(telescope,plot):

#    if telescope == "LOW":
#    ## Tatm
#        freq_array = np.genfromtxt("SKA_LOW.txt", usecols=0)
#        Aeff_array = np.genfromtxt("SKA_LOW.txt", usecols=1)
#        Aeff = interp1d(freq_array, Aeff_array, kind='cubic')
#        Aeff = lambda freqGHz: Aeff(freqGHz)

    if telescope == "SKA":
        D = 15.0 # dish diameter in metres
        etaF  = lambda freqGHz: 0.92 - 0.04*np.abs(np.log10(freqGHz)) # feed illumination
        epsp  = 280.0e-6 # rms surface error in metres for the primary reflector surface
        epss  = 154.0e-6 # rms surface error in metres for the secondary reflector surface
        Ap    = 0.89     # unitless constant
        As    = 0.98     # unitless constant

    elif telescope == "MeerKAT":
        D     = 13.5 # dish diameter in metres
        etaF  = lambda freqGHz: 0.80 - 0.04*np.abs(np.log10(freqGHz)) # feed illumination
        epsp = 480.0e-6 # rms surface error in metres for the primary reflector surface
        epss = 265.0e-6 # rms surface error in metres for the primary reflector surface
        Ap   = 0.89     #?? # unitless constant
        As   = 0.98     #?? # unitless constant

    elif telescope == "Effelsberg":
        D    = 100.0 # dish diameter in metres
        
    else:
        print("No idea what type of telescope I'm supposed to be calculating for. FAIL.")
        sys.exit(-1)

    # Some basic stuff - could do this better with astropy!
    speedoflight = 3.0e+8 # m/s 
    wavelength = lambda freqGHz: 1.0e-9*speedoflight/freqGHz

    # Aperture efficiency
    delta   = 2*(Ap*epsp*epsp + As*epss*epss)**0.5
    DeltaPh = lambda freqGHz: 2*m.pi*delta/wavelength(freqGHz)
    etaPh = lambda freqGHz: np.exp(-(DeltaPh(freqGHz))**2.0) 
    etaD  = lambda freqGHz: 1.0 - 20.0*(wavelength(freqGHz)/D)**(1.5)
    etaA  = lambda freqGHz: etaF(freqGHz)*etaPh(freqGHz)*etaD(freqGHz)   # Overall aperture efficiency
#    elif telescope == "Effelsberg":
#        etaA  = lambda freqGHz: 0.525 + freqGHz*0.0

    freq = np.logspace(np.log10(0.350), np.log10(50.0), 200)
    if plot == True:
        plt.figure()
        plt.grid(True)
        plt.title("Aperture efficiency - %s dish"%(telescope))
        plt.ylabel("Aperture efficiency")
        plt.xlabel("Frequency (GHz)")
        plt.semilogx(freq, etaA(freq), 'o')
        plt.show()

    # Collecting Area
    Aphys = m.pi*D*D/4.0                               # Physical collecting area

    if telescope == "SKA":
        Aeff  = lambda freqGHz: Aphys*etaA(freqGHz)        # Effective collecting area
    elif telescope == "MeerKAT":
        Aeff  = lambda freqGHz: Aphys*etaA(freqGHz)*(np.heaviside((freqGHz-0.58), 1.0)-np.heaviside((freqGHz-3.05),1.0))        # Effective collecting area
#    elif telescope == "Low":
#        Aeff  = lambda freqGHz: Aphys*etaA(freqGHz)*(np.heaviside((freqGHz-0.050), 1.0)-np.heaviside((freqGHz-0.350),1.0))        # Effective collecting area
    elif telescope == "Effelsberg":
        Aeff  = lambda freqGHz: Aphys*etaA(freqGHz)*(np.heaviside((freqGHz-1.0), 1.0)-np.heaviside((freqGHz-2.0),1.0))        # Effective collecting area

    return Aeff

def get_tsys(telescope, gal, pwv, zenith, plot):
    
    # Receiver & Spillover Temperature
    if telescope == "SKA":
        Trcv = lambda freqGHz: (15.0 + 30*(freqGHz - 0.75)**2)*(np.heaviside((freqGHz-0.35),1.0)-np.heaviside((freqGHz-0.95),0.0)) + (7.5)*(np.heaviside((freqGHz-0.95),0.0)-np.heaviside((freqGHz-4.6),0.0)) + (4.4 + 0.69*freqGHz)*(np.heaviside((freqGHz-4.6),0.0)-np.heaviside((freqGHz-50.0),0.0))
        Tspill = lambda freqGHz: 3.0 + freqGHz*0.0 # assumed to be this for all Bands but (a) is frequency dependent; (b) is zenith angle dependent - 3 K is thought to be appropriate for zenith < 45 deg; (c) the frequency dependence would actually be such that this should actually be a bit worse for Band 1 as it is not an octave feed.

    elif telescope == "MeerKAT":
        Trcv = lambda freqGHz: (11.0-4.5*(freqGHz-0.58))*(np.heaviside((freqGHz-0.58),1.0)-np.heaviside((freqGHz-1.02),0.0)) + (7.5+6.8*(np.abs(freqGHz-1.65))**1.5)*(np.heaviside((freqGHz-1.02),0.0)-np.heaviside((freqGHz-1.65),0.0)) + (7.5)*(np.heaviside((freqGHz-1.65),0.0)-np.heaviside((freqGHz-3.05),0.0))
        Tspill = lambda freqGHz: 4.0 + freqGHz*0.0

    elif telescope == "Effelsberg":
        Trcv = lambda freqGHz: 21.0 + freqGHz*0.0
        Tspill = lambda freqGHz: 0.0 + freqGHz*0.0 # don't know

    # Sky Temperature
    ## Tgal
    ## At the minute can only do 10th, 50th and 90the percentile values for Tgal 
    ## Need to add any line of sight
    ## For now this is fine as it allows a direct comparison with Robert's calculations
    if (gal == "low"):
        tgal_pc = 10
        T408 = 17.1
    elif (gal == "medium"):
        tgal_pc = 50
        T408 = 25.2
    elif (gal == "high"):
        tgal_pc = 90
        T408 = 54.8
    Tgal = lambda freqGHz: T408*(0.408/(freqGHz))**(2.75) # an off-plane approximation, need to do this more generally
    ## Tcmb
    Tcmb = 2.73
    ## Tatm
    freq_array = np.genfromtxt("SKA_Tatm.txt", usecols=0)
    if (pwv == "low"):
        pwv_mm = 5.0
        Tatm_array = np.genfromtxt("SKA_Tatm.txt", usecols=1)
    elif (pwv == "medium"):
        pwv_mm = 10.0
        Tatm_array = np.genfromtxt("SKA_Tatm.txt", usecols=2)
    elif (pwv == "high"):
        pwv_mm = 20.0
        Tatm_array = np.genfromtxt("SKA_Tatm.txt", usecols=2)
    Tatm = interp1d(freq_array, Tatm_array, kind='cubic')
    Tsky = lambda freqGHz: Tgal(freqGHz) + Tcmb + Tatm(freqGHz)
    ### Opacity
    if (pwv == "low"):
        tau_array = np.genfromtxt("SKA_tau.txt", usecols=1)
    elif (pwv == "medium"):
        tau_array = np.genfromtxt("SKA_tau.txt", usecols=2)
    elif (pwv == "high"):
        tau_array = np.genfromtxt("SKA_tau.txt", usecols=2)
    tau = interp1d(freq_array, tau_array, kind='cubic')

    #tau      = 0.01    # just eye-balled a reasonable value until I have the full function
    Tx = lambda freqGHz, temp: (((h_over_k*freqGHz*1.0e9)/(temp))/(np.exp((h_over_k*freqGHz*1.0e9)/(temp)) - 1.0 ))*temp*np.exp(tau(freqGHz)/np.cos(zenith*m.pi/180.0))

    Tsys = lambda f: Tx(f,(Trcv(f)+Tspill(f)+Tsky(f)))

    f = np.logspace(np.log10(0.35),np.log10(50),nfreqs)
    if (plot == True):
        plt.grid(True)
        plt.semilogx(f,Trcv(f),label='Receiver Temp.')
        plt.semilogx(f,Tspill(f),label='Spillover Temp.')
        plt.semilogx(f,Tsky(f),label='Sky Temp. (Gal+CMB+Atm)')
        plt.semilogx(f,Tsys(f),label='Tsys')
        plt.title("Temperature contributions, %2dth percentile $T_{\mathrm{Gal}}$, PWV %.1f mm"%(tgal_pc,pwv_mm))
        plt.ylabel("Temperature (K)")
        plt.xlabel("Frequency (GHz)")
        plt.legend()
        plt.show()

    return Tsys, f
