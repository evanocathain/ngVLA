## Caoimhe Mannion Aug 2021 ##

# Generates Figure of Merit Plot of Survey Speed (in arbitrary units) vs Distance from Array Centre
# in 6 plots corresponding to ngVLA bands 1-6
# comparing ngVLA performance to other telescopes in relevant frequencies

## DATA SOURCES:
# ngVLA data sourced from:  ngVLA_RX_cascade_analysis_Ver12_2021-07-15, B Butler (for Aeff/Tsys data; see ngVLA_data_1.py for processing)
#                           ngVLA Rev_D_Configuration, C Carlilli https://ngvla.nrao.edu/page/tools 
# ALMA data sourced from:   ALMA Cycle 7 Technical Handbook (for System Temperatiure; estimated from fig 4.7, assuming PWV = 6mm to match ngVLA data) https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi-pbqRoNvyAhXOiVwKHddJBQYQFnoECAUQAQ&url=https%3A%2F%2Farc.iram.fr%2Fdocuments%2Fcycle7%2FALMA_Cycle7_Technical_Handbook.pdf&usg=AOvVaw0U9fSWq7s2MggeIYcbzb68
#                           ALMA Memo 602, J Magnum (for Aperture Efficiency; from Table 4) https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwia8Ma4ldnyAhXdQEEAHRK8DKIQFnoECAQQAQ&url=https%3A%2F%2Flibrary.nrao.edu%2Fpublic%2Fmemos%2Falma%2Fmemo602.pdf&usg=AOvVaw1WO_BGF7iaXY3kllOw47Va
#                           ALMA Cycle 7 Configuration (used cycle 7 as identical to cycle 8 but includes long baseline config) https://almascience.nrao.edu/tools/casa-simulator
#                           Specifications for 2nd Gen Correlator V2 (for Number of Beams estimated as: max 6 sub arrays * max 4 beams per sub array = 24 beams) https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiOyuG_m9nyAhW-QEEAHYhJDfcQFnoECAQQAQ&url=https%3A%2F%2Fscience.nrao.edu%2Ffacilities%2Falma%2Fscience_sustainability%2FSpecifications2ndGenCorrelatorV2.pdf&usg=AOvVaw3I-nVAwHk_ddlGKRzuzAp7
# SKA/MeerKAT/Effelsburg/FAST/Arecibo/Parkes data sourced from: Evan Keane (see functions.py, fom_plot.gp)

## Dependencies on other scripts: 
# get_gain.py (CM)
# ngvla_data_1.py (CM)
# functions.py (EK)
# Adapted for python from fom_plot.gp (EK)

## TO USE:
# call main(<band no's>,config=[<ALMA config no's>],subplot=<subplot option>) at bottom of script.
# 
# ngVLA band numbers 1-6, can call any or all of these
# ALMA config numbers is an optional argument, and only relevant for band 6. Options 1-10, can call any or all of these. Use list format eg [8],[2,8,10], etc.
# Subplot optional argument, for all 6 bands; takes bool: True gives outputs as subplots on one figure, False gives each plot separately
# 
# Current Defaults: All bands, ALMA configs 8,10, subplot=True
#
# Note: there are two hyothetical ngVLA curves for 100 and 500 beams, for comparison with the other arrays
#       These can be removed/edited in the arrays() function


import numpy as np
import matplotlib.pyplot as plt
import get_gain as g
import random as r


def readfile(file):
    """Reads a file, adds content to a list, line by line. W/ character strip"""
    
    filedata = open(file,'r')

    data = filedata.readlines()
    lines = []
    for line in data:
        if line.find('#') == -1: #exclude lines with comments, only take data
            line = line.strip() #remove newline characters
            line = line.split() #split into list of values, space-delimited
            lines.append(line)

    return lines


def sort_alma(list):
    """For ALMA data. Return list of absolute distance, sorted"""
    #ALMA data is in xyz offset realtive to array centre at origin 
    
    X = []
    Y = []
    Z = []

    for i in list:

        X.append(float(i[0]))
        Y.append(float(i[1]))
        Z.append(float(i[2]))

    dist = []
    for i in range(len(X)):
        d = np.sqrt(X[i]**2 + Y[i]**2 + Z[i]**2)
        dist.append(d)
    
    dist.sort()

    return dist


def sort_ska(list):
    """For SKA. Return list of absolute distance, sorted"""
    #SKA data is in xy offset realtive to array centre at origin
    #Separate the MK and SKA dishes, for gain calc

    X = []
    Y = []
    N = []

    for i in list:        
        X.append(float(i[2]))
        Y.append(float(i[3]))
        N.append(i[1])

    dist = []
    for i in range(len(X)):
        d = np.sqrt(X[i]**2 + Y[i]**2)
        dist.append([d,N[i]])
    
    dist.sort(key=lambda dish: dish[0])
    
    return dist


def sort_mk(list):
    """For MeerKAT. Return list of absolute distance, sorted"""
    #MK data is the telescopes in SKA labelled "M"

    X = []
    Y = []

    for i in list:
        if i[1][0] == 'M':        
            X.append(float(i[2]))
            Y.append(float(i[3]))

    dist = []
    for i in range(len(X)):
        d = np.sqrt(X[i]**2 + Y[i]**2)
        dist.append(d)
    
    dist.sort()

    return dist


def sort_ngvla(list):
    """For ngVLA data. Return list of absolute distance, sorted"""
    #ngVLA data is in xyz ITRF coords relative to centre of the earth

    #set reference point at array centre
    xref = -1603108.43734 
    yref = -5041123.90605 
    zref = 3555256.93667

    X = []
    Y = []
    Z = []

    for i in list:
                
        X.append(float(i[0]))
        Y.append(float(i[1]))
        Z.append(float(i[2]))

    dist = []
    for i in range(len(X)):
        d = np.sqrt((X[i]-xref)**2 + (Y[i]-yref)**2 + (Z[i]-zref)**2)
        dist.append(d)
    
    dist.sort()

    return dist


def y_data(xdata,gn,Nbeams,R,f,ska=False):
    """Calculate Survey Speed"""
    # gain = A_eff/T_sys
    # field of view = min((1/(dish radius)^2),(Nbeams/(dist from array centre)^2))
    # survey speed  = fov*g^2
    # survey speed calculated for 1.4 GHz: scale for different frequencies
    # sort SKA separately as it includes MK dishes with different gain

    g = 0
    fov = 1/(R**2)

    ydata = []

    if ska == True:
        for i in xdata:
            
            if i[1][0] == 'M':
                g += gain(f,'M')
            elif i[1][0] == 'S':
                g += gain(f,'S')

            if Nbeams/(i[0]**2) < fov:
                fov = Nbeams/(i[0]**2)
            
            ydata.append(fov*(g*(1.4/f))**2)

    else:
        for i in xdata:
            
            g += gn

            if Nbeams/(i**2) < fov:
                fov = Nbeams/(i**2)
            
            ydata.append(fov*(g*(1.4/f))**2)

    return ydata


def gain(f,telescope):
    """Get gain values from get_gain.py"""

    N, S, M = g.main(f)

    if telescope == 'N':
        return N
    elif telescope == 'S':
        return S
    elif telescope == 'M':
        return M


def alma_gain(Ndishes):
    """Calculate A_eff/Tsys for ALMA at 90GHz"""

    Tsys = 80

    Aphys = Ndishes*np.pi*(12**2)/4 #physcial area = pi*(D/2)^2 *number of dishes
    Aeff = Aphys*0.75 #effective area = physical area * efficiency

    return Aeff/Tsys


def alma_configs(C):
    """To choose which ALMA configuration to plot"""

    inputs = ['alma.cycle7.1.cfg','alma.cycle7.2.cfg','alma.cycle7.3.cfg','alma.cycle7.4.cfg','alma.cycle7.5.cfg','alma.cycle7.6.cfg','alma.cycle7.7.cfg','alma.cycle7.8.cfg','alma.cycle7.9.cfg','alma.cycle7.10.cfg']

    return inputs[C-1]


def arrays(F,B,configs):
    """Outputs data for plotting the arrays. Takes Frequency, Band number, ALMA configuration"""

    args = []
    
    #ngVLA
    x1 = sort_ngvla(readfile('../Configuration/Rev_D_Config_Data/rev_d_xyz.txt'))
    y1 = y_data(x1,gain(F,'N'),50,9,F)
    args.append([x1,y1,'magenta','ngVLA 50 beams',0.03])
    #hypothetical ngVLA curves for 100 and 500 beams:
    y11 = y_data(x1,gain(F,'N'),100,9,F)
    y12 = y_data(x1,gain(F,'N'),500,9,F)
    args.append([x1,y11,'orchid','ngVLA 100 beams',0.031])
    args.append([x1,y12,'orchid','ngVLA 500 beams',0.032])

    if B == 6:
        #ALMA
        for i in range(len(configs)):
            x4 = sort_alma(readfile('../Configuration/ALMA_Config_Data/'+alma_configs(configs[i])))
            y4 = y_data(x4,alma_gain(len(x4)),24,6,F) 
            args.append([x4,y4,'b','ALMA (config cycle 7.'+str(configs[i])+')',(r.randint(1,9))*0.01])
    else:
        #SKA
        x2 = sort_ska(readfile('../Configuration/MID_dist_metres.txt'))
        y2 = y_data(x2,0,750,7.5,F,ska=True)
        y21 = y_data(x2,0,1500,7.5,F,ska=True)
        y22 = y_data(x2,0,10000,7.5,F,ska=True)
        
        x21 = []
        for i in x2:
            x21.append(i[0])
        
        args.append([x21,y2,'k','SKA Mid 750 beams',0.4])
        args.append([x21,y21,'k','SKA Mid 1500 beams',0.5])
        args.append([x21,y22,'k','SKA Mid 10000 beams',0.55])

        #MeerKAT
        x3 = sort_mk(readfile('../Configuration/MID_dist_metres.txt'))
        y3 = y_data(x3,gain(F,'M'),400,6.75,F)
        y31 = y_data(x3,gain(F,'M'),10000,6.75,F)
        args.append([x3,y3,'g','MeerKAT 400 beams',0.7])
        args.append([x3,y31,'g','MeerKAT 10000 beams',0.7])

    return args


def single_dishes(f):
    """Outputs data for plotting the single dishes."""
    
    args = []

    Tsky = 25.2*(0.408/f)**2.75

    # FAST
    fast_x = 250 #dish radius for x
    fast_full  = 40000.0/(20.0+Tsky)
    fast_y = (19.0*fast_full**2)/(125.50**2)
    args.append([fast_x,fast_y,'mediumslateblue','FAST MB-19'])
    
    # Arecibo
    ao_x = 150
    ao_centre  = 28704.0/(24.0+Tsky) # 10.4 K/Jy
    ao_ring = ao_centre*(8.2/10.4) # 8.2 K/Jy
    ao_y = ((ao_centre**2)/(95.6**2))+((6.0*ao_ring**2)/((95.6*8.2/10.4)**2))
    args.append([ao_x,ao_y,'dodgerblue','Arecibo MB-7'])

    # Effelsberg MB-7 HTRU-N
    eff_x = 60
    eff_centre = 0.525*np.pi*100**2*0.25/(21.0+Tsky) 
    eff_ring = eff_centre*(0.455/0.525)
    eff_y = ((eff_centre**2)/(0.525*eff_x**2))+((6.0*eff_ring**2)/(0.455*eff_x**2))
    args.append([eff_x,eff_y,'orange','Effelsberg MB-7'])

    # Parkes MB-13 HTRU/SUPERB
    pks_x = 32
    pks_centre  = 0.86*0.86*np.pi*64**2*0.25/(23.0+Tsky) #  0.735 K/Jy
    pks_inner =  pks_centre*0.690/0.735 # 0.690 K/Jy
    pks_outer =  pks_centre*0.581/0.735 # 0.581 K/Jy
    pks_y = ((pks_centre**2)/(0.86*0.86*pks_x**2))+((6.0*pks_inner**2)/((0.86*0.86*(0.690/0.735)*pks_x**2)))+((6.0*pks_outer**2)/((0.86*0.86*(0.581/0.735)*pks_x**2)))
    args.append([pks_x,pks_y,'wheat','Parkes MB-13'])

    return args


def plot(data):
    """Plots Survey Speed vs Distance from array centre."""
    
    # input format: dictionary {"f","b","array data"}
    # array data format: list of [xdata,ydata,'colour','name','label location']

    #plot arrays
    f = data["f"]
    b = data["b"]
    arraydata = data["array data"]    
    for i in arraydata:
        plt.loglog(i[0],i[1],color=i[2],linewidth=.5)
        l = int(i[4]*len(i[0])) #label position
        plt.text(i[0][l],i[1][l],i[3],color=i[2],fontsize='medium')

    #plot single dishes
    if b == 1:
        single = single_dishes(f)
        for i in single:
            plt.plot(i[0],i[1],color=i[2],marker='s',markersize=10)
            plt.text(i[0],i[1],i[3],color='k',fontsize='medium')

    plt.title("Survey Speed at "+str(f)+"GHz (ngVLA Band "+str(b)+")")
    plt.xlabel("Distance from Array Centre (m)")
    plt.ylabel("PSR Survey Speed FoM (arbitrary units)")
    plt.grid(True,which='both',ls='--')
    plt.xlim(20,6000)
    
    plt.savefig('SS_band'+str(b)+'.png',dpi=400,facecolor='w',edgecolor='w',transparent=False,bbox_inches='tight',pad_inches=0.2)
    plt.show()


def splot(data):
    """Plots Survey Speed vs Distance from array centre for all 6 bands in a single figure"""

    # input format: list of 6 dictionaries, 1 for each band
    # dictionary format: {"f","b","array data"}
    # array data format: list of [xdata,ydata,'colour','name','label location']

    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(16,9),constrained_layout=True, gridspec_kw={'height_ratios': [1, 1]})    
    
    for i in data[0]["array data"]:
        ax1.loglog(i[0],i[1],color=i[2],linewidth=.5)
        l = int(i[4]*len(i[0])) #label position
        ax1.text(i[0][l],i[1][l],i[3],color=i[2],fontsize='small')
    ax1.set_title("Survey Speed at "+str(data[0]["f"])+"GHz (ngVLA Band "+str(data[0]["b"])+")")
    ax1.set(xlabel="Distance from Array Centre (m)",ylabel="PSR Survey Speed FoM (arbitrary units)")
    ax1.grid(True,which='both',ls='--')
    ax1.set(xlim=(20,6000))
    ax1.set(ylim=(10e-2,10e4))
    
    for i in data[1]["array data"]:
        ax2.loglog(i[0],i[1],color=i[2],linewidth=.5)
        l = int(i[4]*len(i[0])) #label position
        ax2.text(i[0][l],i[1][l],i[3],color=i[2],fontsize='small')
    ax2.set_title("Survey Speed at "+str(data[1]["f"])+"GHz (ngVLA Band "+str(data[1]["b"])+")")
    ax2.set(xlabel="Distance from Array Centre (m)",ylabel="PSR Survey Speed FoM (arbitrary units)")
    ax2.grid(True,which='both',ls='--')
    ax2.set(xlim=(20,6000))
    ax2.set(ylim=(10e-3,10e3))
    
    for i in data[2]["array data"]:
        ax3.loglog(i[0],i[1],color=i[2],linewidth=.5)
        l = int(i[4]*len(i[0])) #label position
        ax3.text(i[0][l],i[1][l],i[3],color=i[2],fontsize='small')
    ax3.set_title("Survey Speed at "+str(data[2]["f"])+"GHz (ngVLA Band "+str(data[2]["b"])+")")
    ax3.set(xlabel="Distance from Array Centre (m)",ylabel="PSR Survey Speed FoM (arbitrary units)")
    ax3.grid(True,which='both',ls='--')
    ax3.set(xlim=(20,6000))
    ax3.set(ylim=(10e-4,10e2))
    
    for i in data[3]["array data"]:
        ax4.loglog(i[0],i[1],color=i[2],linewidth=.5)
        l = int(i[4]*len(i[0])) #label position
        ax4.text(i[0][l],i[1][l],i[3],color=i[2],fontsize='small')
    ax4.set_title("Survey Speed at "+str(data[3]["f"])+"GHz (ngVLA Band "+str(data[3]["b"])+")")
    ax4.set(xlabel="Distance from Array Centre (m)",ylabel="PSR Survey Speed FoM (arbitrary units)")
    ax4.grid(True,which='both',ls='--')
    ax4.set(xlim=(20,6000))
    ax4.set(ylim=(10e-5,10e1))
    
    for i in data[4]["array data"]:
        ax5.loglog(i[0],i[1],color=i[2],linewidth=.5)
        l = int(i[4]*len(i[0])) #label position
        ax5.text(i[0][l],i[1][l],i[3],color=i[2],fontsize='small')
    ax5.set_title("Survey Speed at "+str(data[4]["f"])+"GHz (ngVLA Band "+str(data[4]["b"])+")")
    ax5.set(xlabel="Distance from Array Centre (m)",ylabel="PSR Survey Speed FoM (arbitrary units)")
    ax5.grid(True,which='both',ls='--')
    ax5.set(xlim=(20,6000))
    ax5.set(ylim=(10e-6,10))

    for i in data[5]["array data"]:
        ax6.loglog(i[0],i[1],color=i[2],linewidth=.5)
        l = int(i[4]*len(i[0])) #label position
        ax6.text(i[0][l],i[1][l],i[3],color=i[2],fontsize='small')
    ax6.set_title("Survey Speed at "+str(data[5]["f"])+"GHz (ngVLA Band "+str(data[5]["b"])+")")
    ax6.set(xlabel="Distance from Array Centre (m)",ylabel="PSR Survey Speed FoM (arbitrary units)")
    ax6.grid(True,which='both',ls='--')
    ax6.set(xlim=(20,6000))
    ax6.set(ylim=(10e-8,10e-2))
    
    plt.savefig('SS_plots.png',dpi=400,facecolor='w',edgecolor='w',transparent=False,bbox_inches='tight',pad_inches=0.2)
    plt.show() 


def data_all(configs):
    """Collects data for each band into a dictionary for plotting"""
    
    b_1 = {"f":1.4,"b":1,"array data":arrays(1.4,1,configs)}
    b_2 = {"f":6.6,"b":2,"array data":arrays(6.6,2,configs)}
    b_3 = {"f":15.9,"b":3,"array data":arrays(15.9,3,configs)}
    b_4 = {"f":26.4,"b":4,"array data":arrays(26.4,4,configs)}
    b_5 = {"f":39.2,"b":5,"array data":arrays(39.2,5,configs)}
    b_6 = {"f":90.0,"b":6,"array data":arrays(90.0,6,configs)}

    return [b_1,b_2,b_3,b_4,b_5,b_6]


def main(*B,configs=[8],subplot=True):
    """Take band number(s), and optional ALMA config specification (for band 6: choose any/all of 1-10)"""
    
    # Get relevant array data
    alldata = data_all(configs)
    data = []
    for i in B:
        data.append(alldata[i-1])

    if (len(B) != 6) or (subplot == False):
        for i in range(len(data)):
            plot(data[i])
    else:
        splot(alldata)


main(1,2,3,4,5,6,configs=[8,10],subplot=True)