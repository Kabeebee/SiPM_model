import Datareader as dr
import numpy as np
import numpy.random as rand
import h5py
import matplotlib.pyplot as plt
from scipy import signal
from datetime import datetime

#**************************************************************************************
class Pulse:
    def __init__(self):
        self.numAfterPulses = 0
        self.afterPulseTimes = []
        self.afterPulseAmplitudes = []
        self.numPromptCT = 0

def main():
    start_time = datetime.now()
    DataLeft = True # DataLeft checks if there is data still left to analyse
    counter = 0     # keeps track of which data set we're on

    timeData, template_pulse = dr.reader("londat.csv")

    fig, (ax_orig) = plt.subplots(1, 1, sharex= True)

    # load in the x-data once

    readFile = h5py.File('data.h5', 'r')
    xdata = readFile.get('xdata')
    xdata = np.array(xdata)
    readFile.close

    # load in y-data sets sequentially 

    while DataLeft:

        pulseData = Pulse()

        readFile = h5py.File('data.h5', 'r')
        data = readFile.get("SPADPulse%d" % counter)

    # if there is no data stored under that name, we are out of data. stop the loop
        if data == None:
            DataLeft = False
            break

    # there is data here... analysis time
        else:
            data = np.array(data)
            readFile.close()

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

            counter += 1
            print("-------- pulse No:%d --------" % (counter))
            print("Number of afterpulses: %d" % pulseData.numAfterPulses)
            if pulseData.numAfterPulses != 0:
                print("Afterpulse Time(s): %s" % str(pulseData.afterPulseTimes))
                print("Afterpulse amplitude(s): %s" % str(pulseData.afterPulseAmplitudes))
            print("Number of Prompt CTs: %d" % pulseData.numPromptCT)

    stop_time = datetime.now()
    run_time = stop_time - start_time
    print("Total run time (h:m:s):   %s" % str(run_time))


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

if __name__ == '__main__':
    main()