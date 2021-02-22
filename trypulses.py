'''
Detector pulses script
'''
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def plotpulse(xval,yval):
    ''' plot with insert '''
    fig = plt.figure()
    axis1 = fig.add_axes([0.12, 0.1, 0.85, 0.85]) # main axes
    axis2 = fig.add_axes([0.54, 0.25, 0.35, 0.3]) # inset axes
    axis1.plot(xval, yval, 'r-')
    axis1.set_title('Dark Matter detector pulse', size=12)
    axis1.set_xlabel('Time [ns]', size=12)
    axis1.set_ylabel('Bias [mV]', size=12)
    
    axis2.plot(xval[:80], yval[:80], 'b-') # zoom in to 40 ns maximum
    axis2.set_title('Fast pulse component', size=12)
    axis2.set_xlabel('Time [ns]', size=12)
    axis2.set_ylabel('Bias [mV]', size=12)
    plt.show()
    return


def pulse(t, scale, onset, baseline, ratio, taurise, taushort, taulong):
    ''' pulse model function to work with numpy.'''
    denominator = ratio + 1
    temp1  = ratio / (denominator) * np.exp(-(t - onset) / taushort)
    temp2  = 1.0 / (denominator) * np.exp(-(t - onset) / taulong)
    decay = temp1 + temp2
    pulse = scale * (np.exp(-(t - onset) / taurise) - decay) + baseline
    pulse[np.where(t < onset)] = 0.0 # not defined before onset time, set 0
    return pulse

# make a pulse, consider times in nano seconds [ns]
timevalues = np.linspace(0, 1000, 2001) # 0.5 unit step size
taurise = 1.0     # fast sensor rise time
taushort = 6.0    # realistic short decay time for Xenon
taulong = 1500.0  # realistic decay time for Xenon 1500 ns
scale = 210.0  # some scale factor giving reasonable values
onset = 4.0    # start on step 4, here 2 ns in the sample
baseline = 0.0 # no baseline offset
ratio = 2.2    # more in short intensity than long
pp = pulse(timevalues, scale, onset, baseline, ratio, taurise, taushort, taulong)

plotpulse(timevalues, pp)

# fit the pulse, try similar values to construction
initguess = (20.0, 4.0, 0.0, 2.0, 1.0, 5.0, 1000.0)
fitParams, fitCovariances = curve_fit(pulse, timevalues, pp, p0 = initguess)
print (fitParams)
print (fitCovariances)
