import numpy as np
import numpy.random as rand

def thermal(bins, stdev):
    noise = np.random.normal(0, stdev, bins)
    return noise

def afterpulse(xdata, pulseProb):
    probArray = rand.random(len(xdata))
    result = np.zeros(len(xdata))
    for i in range(0, len(probArray)):
        if probArray[i] < pulseProb:
            result[i] = 1
    return result
