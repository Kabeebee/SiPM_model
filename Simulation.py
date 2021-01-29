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
# h5py takes numpy arrays as input so first create arrays from the data lists
print(xdata)

#**************************************************************************************
# make the data file and fill it with data : )

dataFile = h5py.File('data.h5', 'w')
dataFile.create_dataset('xdata', data = xdata)
dataFile.create_dataset('ydata', data = ydata)
dataFile.close()

#**************************************************************************************
# open the file and read the data back out

readFile = h5py.File('outputdata\data.h5', 'r')
readX = readFile.get('xdata')
readY = readFile.get('ydata')
readX = np.array(readX)
readY = np.array(readY)
readFile.close()

print(readX)

#**************************************************************************************

