import Datareader as dr
import numpy as np
import numpy.random as rand
import h5py
import matplotlib.pyplot as plt

deadTime = 20
NUMSPADS = 25

#**************************************************************************************
# read in and store the data from csv called 'londat.csf'
xdata = np.array([])
ydata = np.array([])
xdata, ydata = dr.reader("londat.csv")

SiPMPulse = np.array([])


#**************************************************************************************
# add random fluctuations to data

def randNoise(bins, stdev):
    noise = rand.normal(0, stdev, bins)
    return noise

#**************************************************************************************
# Afterpulsing
def afterpulsing(ydata, spadPulse):
    A = 1
    LAMBDA = 2
    for j in range(1, len(xdata) - 1):
        pulseProb = (A * ((xdata[j] + 1) ** (-LAMBDA)))
        if rand.rand() > 1 - pulseProb:
            position = xdata[j]
            pos = j
            if position > deadTime:
                scale = rand.rand()
                for i in range(pos, len(ydata)):
                    spadPulse[i] = spadPulse[i] + ydata[(i - pos)]


#**************************************************************************************
# make the data file and fill it with data : )
def saveData():
    dataFile = h5py.File('data.h5', 'w')
    dataFile.create_dataset('xdata', data = xdata)
    dataFile.create_dataset('ypulse', data = spadPulse)
    dataFile.close()



#**************************************************************************************
# Add together multiple SPad PUlses to simulate a Sipm
# look at making the spad firing distrobution more sophisticated

for index in range(0, 1): 
    if rand.rand() > 0.5:
        spadPulse = np.array([])
        spadPulse = np.append(spadPulse, ydata)

        afterpulsing(ydata, spadPulse)
        spadPulse += randNoise(len(ydata), 2)

        if len(SiPMPulse) == 0:
            SiPMPulse = np.append(SiPMPulse, spadPulse)
        
        #else:
            #SiPMPulse += spadPulse


plt.plot(xdata, SiPMPulse)
plt.show()