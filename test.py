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


scale = 1.69766873e+02
onset = -1.44362685e-02
taurise = 1.23049988e+00
tauriselong = 2.86445752e+00
taushort = 7.08704322e+00
taulong = 1.18153265e+01


scale2 = 173.88
onset2 = 99
taurise2 = 1.187
tauriselong2 = 2.9944
taushort2 = 6.875
taulong2 = 11.86

temp1  = np.exp(-(t - (onset)) / taushort)
temp2  = np.exp(-(t - (onset)) / taulong)
decay = temp1 + temp2
pulse = -scale * (np.exp(-(t - (onset)) / taurise) + np.exp(-(t - (onset)) / tauriselong) - decay)
pulse[np.where(t < onset)] = 0.0

temp3  = np.exp(-(t - onset2) / taushort2)
temp4  = np.exp(-(t - onset2 ) / taulong2)
decay2 = temp3 + temp4
pulse2 = -scale2 * (np.exp(-(t - onset2) / taurise2) + np.exp(-(t - onset2) / tauriselong2)- decay2)
pulse2[np.where(t < onset2)] = 0.0



plotpulse(t, pulseData22, pulse, pulse2)

