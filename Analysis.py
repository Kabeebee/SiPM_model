import Datareader as dr
import numpy as np
import numpy.random as rand
import h5py
import matplotlib.pyplot as plt
from scipy import signal
from datetime import datetime
from scipy.optimize import curve_fit
from tqdm import tqdm

#**************************************************************************************
class Pulse:
    def __init__(self):
        self.numAfterPulses = 0
        self.afterPulseTimes = []
        self.afterPulseAmplitudes = []
        self.numPromptCT = 0
        self.numDelayedCT = 0
        self.DelayedCTTimes = []
        self.DelayedCTAmplitudes = []
        self.PulseAmplitude = 0
        



def main():
    DataLeft = True # DataLeft checks if there is data still left to analyse
    counter = 0     # keeps track of which data set we're on
    numsims = 100
 
    timeData, template_pulse = dr.reader("londat.csv")
    template_pulse = np.resize(template_pulse, 100)

    fig, (ax_orig) = plt.subplots(1, 1, sharex= True)

    # load in the x-data once

    readFile = h5py.File('data.h5', 'r')
    xdata = readFile.get('xdata')
    xdata = np.array(xdata)
    readFile.close

    # load in y-data sets sequentially 
    while DataLeft:
        for i in tqdm(range(numsims)):

            pulseData = Pulse()

            readFile = h5py.File('data.h5', 'r')
            data = readFile.get("SPADPulse%d" % counter)

        # if there is no data stored under that name, we are out of data. stop the loop
            if data == None:
                DataLeft = False
                break
        # if data is [0] means that data is simply reference data + noise (which we will add here)
            elif data == [0]:
                refdat = readFile.get("referenceData")
                data = np.array(refdat)
                data += rand.normal(0, 1, len(data))
                readFile.close()

        # there is data here... analysis time
            else:
                data = np.array(data)
                readFile.close()

            # try and collect initial guess values to make curve fit easier

            numPeaks, peakPositions = calculate_num_peaks(data, template_pulse)

            for i in range(len(peakPositions)):
                if i != 0:
                    pulseData.afterPulseTimes.append(peakPositions[i])
                    amplitude = data[peakPositions[i]]
                    pulseData.afterPulseAmplitudes.append(amplitude)
                elif i == 0:
                    amplitude = data[peakPositions[i]]
                    CT = calculate_promptCT(amplitude, template_pulse)
                    pulseData.numPromptCT = CT
                    
            pulseData.numAfterPulses = numPeaks - 1

            # curve fit time (cross fingers)

            initguess = (pulseData.numPromptCT, #amplitude
                        4.0,                   #onset time
                        1.0,                   #rise time
                        5.0,                   #sharp decay time
                        1000.0)                #long decay time

            fitParams, fitCovariances = curve_fit(pulseFitFunc, xdata, data, p0 = initguess)

            counter += 1



def calculate_num_peaks(data, template):
    # step 1, apply a matched filter with the archetype pulse to clean up signal.
    filtered_data = signal.correlate(data, template, mode= 'same')
    filtered_data /= np.max(filtered_data) # normalise for ease
    lag = 57

    # find the number of peaks in the matched filter data which is the same as for
    # the raw data. This should account for pulses overlapping
    peaks = signal.find_peaks(filtered_data, height= 0.4)
    num_peaks = len(peaks[1]['peak_heights'])
    peak_positions = peaks[0] - lag
    return num_peaks, peak_positions

def calculate_promptCT(amplitude, template):
    PE = np.amax(template) # one photon energy is the max value in the archetype pulse
    ampInPE = (amplitude/PE)
    return ampInPE

def pulseFitFunc(t, scale, onset, taurise, taushort, taulong):
    ''' pulse model function to work with numpy.'''
    temp1  = np.exp(-(t - onset) / taushort)
    temp2  = np.exp(-(t - onset) / taulong)
    decay = temp1 + temp2
    pulse = -scale * (np.exp(-(t - onset) / taurise) - decay)
    pulse[np.where(t < onset)] = 0.0 # not defined before onset time, set 0
    return pulse

if __name__ == '__main__':
    main()