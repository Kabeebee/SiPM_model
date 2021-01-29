import Datareader as dr
import numpy as np
import numpy.random as rand
import h5py
import matplotlib.pyplot as plt

NUM_SIMS = 1

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
    if rand.rand() > 0.4:
        print("pulse")
        position = rand.normal(100, 50, 1)
        pos = int(position[0])
        print(pos)
        for i in range(pos, len(ydata)):
            ypulse[i] = ypulse[i] + ydata[(i - pos)]

afterpulsing(ydata, ypulse)
ypulse += randNoise(len(ydata), 2)
#**************************************************************************************
# make the data file and fill it with data : )

dataFile = h5py.File('data.h5', 'w')
dataFile.create_dataset('xdata', data = xdata)
dataFile.create_dataset('ypulse', data = ypulse)
dataFile.close()

print(len(xdata))
plt.plot(xdata, ypulse)
plt.show()



#**************************************************************************************
# function for adding random noise to indicidula data points


