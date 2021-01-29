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



#**************************************************************************************
# make the data file and fill it with data : )

dataFile = h5py.File('data.h5', 'w')
dataFile.create_dataset('xdata', data = xdata)
dataFile.create_dataset('ydata', data = ydata)
dataFile.close()

print(len(xdata))
plt.plot(xdata[:1000], ydata[:1000])
plt.show()


