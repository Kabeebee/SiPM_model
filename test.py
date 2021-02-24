import h5py
import numpy as np
import matplotlib.pyplot as plt 

def plot(): 
    readFile = h5py.File('data.h5', 'r')
    print(readFile.keys())
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
       

        
    
            
plotAP()