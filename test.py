import h5py
import numpy as np
import matplotlib.pyplot as plt 
import math
import numpy as np
from scipy.optimize import curve_fit

def getAP():
    readFile = h5py.File('data.h5', 'r')
    for i in range(0,100):
        spad = readFile.get(f"SPADPulse{i}")
        if np.size(spad) != 1:
            ap = readFile.get(f"APData{i}")
            ap = np.array(ap)
            if np.size(ap) != 1:
                print(ap)


def plotAP(): 
    readFile = h5py.File('data.h5', 'r')
    xdata = readFile.get("xdata")
    for i in range(0,100):
        try:
            spad = readFile.get(f"SPADPulse{i}")
            spad = np.array(spad)
            if np.size(spad) != 1:
                AP = readFile.get(f"APData{i}")
                AP = np.array(AP)
                if AP[0] > 0:
                    xdata = np.array(xdata)
                    plt.plot(xdata, spad)
                    print(f"Pulse {i} at Position: {AP[1]}")
        except:
            print(i)
        
    readFile.close()
    plt.show()
       

        
    
            
'''
Detector pulses script
'''

def plotpulse(xval,yval,pulse1,pulse2):
    ''' plot with insert '''
    fig = plt.figure()
    axis1 = fig.add_axes([0.12, 0.1, 0.85, 0.85]) # main axes
    axis1.plot(xval, yval, 'r-')
    axis1.plot(xval, pulse1, 'b-')
    #axis1.plot(xval, pulse2, 'g-')
    axis1.set_title('Dark Matter detector pulse', size=12)
    axis1.set_xlabel('Time [ns]', size=12)
    axis1.set_ylabel('Bias [mV]', size=12)
    axis1.set_xlim(-10, 500)
    
    plt.show()
    return

readFile = h5py.File('data.h5', 'r')
t = readFile.get("xdata")
pulseData22 = readFile.get("referenceData")
pulseData22 = np.array(pulseData22)
t = np.array(t)


scale = 123.47
onset = 1.218
taurise = 1.506
taushort = 10.577
taulong = 10.590
b = 6.08
c = 15.42


scale2 = 224
onset2 = 95.1
taurise2 = 4.11
taushort2 = 5.233
taulong2 = 11.175
b2 = -4.105
c2 =1.016

temp1  = np.exp(-(t - (onset)) / taushort)
temp2  = np.exp(-(t - (onset)) / taulong)
decay = temp1 + temp2
pulse = -scale * (np.exp(-(t - (onset)) / taurise) - decay)
#pulse[np.where(t<=onset+taurise)] = -(c * t[np.where(t<=onset+taurise)]-onset)*(t[np.where(t<=onset+taurise)] - onset -b)
pulse[np.where(t < onset + taurise)] = 0.0

temp3  = np.exp(-(t - (onset2 + taurise2)) / taushort2)
temp4  = np.exp(-(t - (onset2 + taurise2)) / taulong2)
decay2 = temp3 + temp4
pulse2 = -scale2 * (np.exp(-(t - (onset2 + taurise2)) / taurise2) - decay2)
#pulse2[np.where(t<=onset2+taurise2)] = -(c2 * t[np.where(t<=onset2+taurise2)]-onset)*(t[np.where(t<=onset2+taurise2)] - onset -b2)
pulse2[np.where(t < onset2 + taurise)] = 0.0



plotpulse(t, pulseData22, pulse, pulse2)

