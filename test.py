import h5py
import numpy as np
import matplotlib.pyplot as plt 
import math
import numpy as np
from scipy.optimize import curve_fit

def getAP():
    readFile = h5py.File('output.h5', 'r')
    for i in range(0,100):
        spad = readFile.get(f"Parameters{i}")
        spad = np.array(spad)
        print(spad)


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
    axis1.plot(xval, pulse2, 'g-')
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


scale = 3.21553988e+02
onset = -2.54059274e-06
taurise = 1.65380240e+00
tauriselong = 4.92097753e+00
taushort =  4.21741858e+00
taulong = 1.01444488e+01


scale2 = 1.58923801e+02
onset2 = -6.69606635e-03
taurise2 = 1.19690101e+00
tauriselong2 = 2.54068511e+00
taushort2 =  7.61608389e+00
taulong2 = 1.19584934e+01

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



getAP()

