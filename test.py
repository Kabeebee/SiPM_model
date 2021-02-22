import h5py
import numpy as np
import matplotlib.pyplot as plt 

def plot(): 
    readFile = h5py.File('data.h5', 'r')

    spad = readFile.get("referenceData")
    xdata = readFile.get("xdata")
    spad = np.array(spad)
    xdata = np.array(xdata)
    readFile.close()
        
    plt.plot(xdata[:6], spad[:6])
    plt.show()

def getAP():
    readFile = h5py.File('data.h5', 'r')
    for i in range(0,100):
        spad = readFile.get(f"SPADPulse{i}")
        if np.size(spad) != 1:
            ap = readFile.get(f"APData{i}")
            ap = np.array(ap)
            if np.size(ap) != 1:
                print(ap)
            
getAP()