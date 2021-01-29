import Datareader as dr
import numpy as np
import numpy.random as rand
import h5py
import matplotlib.pyplot as plt

deadTime = 20

#**************************************************************************************
# read in and store the data from csv called 'londat.csf'
xdata = np.array([])
ydata = np.array([])
xdata, ydata = dr.reader("londat.csv")

ypulse = np.array([])
ypulse = np.append(ypulse, ydata)

#**************************************************************************************
# add random fluctuations to data

def randNoise(bins, stdev):
    noise = rand.normal(0, stdev, bins)
    return noise

#**************************************************************************************
# Afterpulsing
def afterpulsing(ydata, ypulse):
    A = 1
    LAMBDA = 2
    for j in range(1, len(xdata) - 1):
        pulseProb = (A * ((xdata[j] + 1) ** (-LAMBDA)))
        if rand.rand() > 1 - pulseProb:
            print("pulse")
            print (pulseProb)
            position = xdata[j]
            pos = j
            print(pos, position)
            if position > deadTime:
                for i in range(pos, len(ydata)):
                    ypulse[i] = ypulse[i] + ydata[(i - pos)]

afterpulsing(ydata, ypulse)
ypulse += randNoise(len(ydata), 2)

#**************************************************************************************
# make the data file and fill it with data : )
def saveData():
    dataFile = h5py.File('data.h5', 'w')
    dataFile.create_dataset('xdata', data = xdata)
    dataFile.create_dataset('ypulse', data = ypulse)
    dataFile.close()

print(len(xdata))
plt.plot(xdata, ypulse)
plt.show()

#**************************************************************************************
# function for adding random noise to indicidula data points



