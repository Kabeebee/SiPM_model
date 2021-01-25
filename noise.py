import numpy as np

def thermal(bins, stdev):
    noise = np.random.normal(0, stdev, bins)
    return noise

def afterpulse(xdata, pulseProb):
    probArray = np.random.random(len(xdata))
    result = np.zeros(len(xdata))
    for i in range(0, len(probArray)):
        if probArray[i] < pulseProb:
            result[i] = 1
    return result
