import Datareader as dr
import numpy as np
import numpy.random as rand
import h5py
import matplotlib.pyplot as plt

#**************************************************************************************

DataLeft = True # DataLeft checks if there is data still left to analyse
counter = 0     # keeps track of which data set we're on

# load in the x-data once

readFile = h5py.File('data.h5', 'r')
xdata = readFile.get('xdata')
xdata = np.array(xdata)
readFile.close

# load in y-data sets sequentially 

while DataLeft:

    readFile = h5py.File('data.h5', 'r')
    data = readFile.get("SpadPulse%d" % counter)

# if there is no data stored under that name, we are out of data. stop the loop
    if data == None:
        DataLeft = False
        break

# there is data here... analysis time
    else:
        data = np.array(data)
        readFile.close()

        # analyseData(data)

        print(data)

        # profit()

        counter += 1
