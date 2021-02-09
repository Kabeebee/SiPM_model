import Datareader as dr
import numpy as np
import numpy.random as rand
import h5py
import matplotlib.pyplot as plt

#**************************************************************************************
# open the file and read the data back out

readFile = h5py.File('data.h5', 'r')
readFile.keys()
readFile.close()
