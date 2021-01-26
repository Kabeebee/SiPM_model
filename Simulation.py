import Datareader as dr
import numpy as np
import numpy.random as rand
import h5py

#**************************************************************************************
# read in and store the data from csv called 'londat.csf'

xvals, voltage = dr.reader("londat.csv")

#**************************************************************************************
# h5py takes numpy arrays as input so first create an array from the data lists

data = []
for i in range(0, len(xvals) - 1):
    data.append([xvals[i], voltage[i]])
dataArray = np.array(data)

#**************************************************************************************
# make the data file and fill it with data : )

dataFile = h5py.File('data.h5', 'w')                     # create a new h5py file called 'data.h5'
dataFile.create_dataset('dataset', data = dataArray)     # make the data array into h5py data and write to file
dataFile.close()                                         # close the file

