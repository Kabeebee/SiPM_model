import Datareader as dr
import csv
import matplotlib.pyplot as plt
import numpy as np
import numpy.random as rand

def thermal(bins, stdev):
    noise = np.random.normal(0, stdev, bins)
    return noise

def afterpulseProb():
    print("hello")

xvals, voltage = dr.reader("londat.csv")

voltage = voltage + thermal(len(voltage), 2)
plt.plot(xvals, voltage)
plt.show()

