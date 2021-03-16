import h5py
import numpy as np
import matplotlib.pyplot as plt 
import math
import numpy as np
from scipy.optimize import curve_fit

def getAP():
    readFile = h5py.File('mergedData.h5', 'r')
    amps = []
    mid = 0
    ml = 0
    mr = 0
    l = 0
    r = 0
    for i in range(0, 100000):
        spad = readFile.get(f"Parameters{i}")
        spad = np.array(spad)
        if np.size(spad) > 1:
            if spad[0] > 165 and spad[0] < 175:
                amps.append(spad[0])
                mid += 1
            if spad[0] > 155 and spad[0] < 165:
                amps.append(spad[0])
                ml += 1
            if spad[0] > 175 and spad[0] < 185:
                amps.append(spad[0])
                mr += 1
            if spad[0] > 145 and spad[0] < 155:
                amps.append(spad[0])
                l += 1
            if spad[0] > 185 and spad[0] < 195:
                amps.append(spad[0])
                r += 1


    plt.scatter(range(5), [l, ml, mid, mr, r])
    plt.show()

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

def calcchi():
    readFile = h5py.File(r'F:\data.h5', 'r')
    t = readFile.get("xdata")
    pulseData22 = readFile.get("SPADPulse342")
    pulseData22 = np.array(pulseData22)
    t = np.array(t)


def getParams(Num):

    file = h5py.File("mergedData.h5")
    params = file.get(f"Parameters{Num}")
    params = np.array(params) 
    file.close()
    print(params)

def plotpulse(xval,yval,pulse1):
    ''' plot with insert '''
    fig = plt.figure()
    axis1 = fig.add_axes([0.12, 0.1, 0.85, 0.85]) # main axes
    axis1.plot(xval, yval, 'r-')
    axis1.plot(xval, pulse1, 'g-')
    axis1.set_xlabel('Time (ns)')
    axis1.set_ylabel('Voltage (mV)')
    axis1.set_xlim(-10, 200)
    axis1.set_ylim(-3, 175)
    
    plt.show()
    return

readFile = h5py.File(r'F:\data.h5', 'r')
t = readFile.get("xdata")
pulseData22 = readFile.get("SPADPulse29068")
pulseData22 = np.array(pulseData22)
t = np.array(t)

params = [ 1.62438867e+02, -1.27802305e-02,  1.19408058e+00,  2.77489857e+00,
  7.68660089e+00,  1.17870762e+01,  2.88421903e+02,  9.21718780e+01,
  1.79194954e+00,  7.88923565e-01,  1.00025321e+00,  1.02269090e+01]

superpos = [0] * 150000

for i in range(0, int(len(params)/6)):
    temp1  = np.exp(-(t - (params[6 * i + 1])) / params[6 *i + 4])
    temp2  = np.exp(-(t - (params[6 *i + 1])) / params[6 *i + 5])
    decay = temp1 + temp2
    pulse = -params[6 *i] * (np.exp(-(t - (params[6 *i + 1])) / params[6 *i + 2]) + np.exp(-(t - (params[6 *i + 1])) / params[6 *i + 3]) - decay)
    pulse[np.where(t < params[6 *i + 1])] = 0.0

    superpos = superpos + pulse




residual = []
residual = (superpos - pulseData22) ** 2
chi = sum(residual) / 4
rchi = chi / (150000 - 6)
print(rchi)

getParams(29068)

plotpulse(t, pulseData22, superpos)

