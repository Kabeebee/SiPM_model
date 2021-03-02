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
    template_pulse = np.resize(template_pulse, 6)

    fig, (ax_orig) = plt.subplots(1, 1, sharex= True)

    # load in the x-data once

    readFile = h5py.File('data.h5', 'r')
    xdata = readFile.get('xdata')
    xdata = np.array(xdata)
    readFile.close


    trueAP = 0
    trueCT = 0
    trueCTD = 0
    countAP = 0
    countCT = 0
    countCTD = 0

    allTimes = np.array([])

    # load in y-data sets sequentially 
    while DataLeft:
        
        pulseData = Pulse()

        readFile = h5py.File('data.h5', 'r')
        data = readFile.get("SPADPulse%d" % counter)

    # Loading in all data
        # if there is no data stored under that name, we are out of data. stop the loop
        if data == None:
            DataLeft = False
            break
        # if data is [0] means that data is simply reference data + noise (which we will add here)
        elif np.size(data) == 1:
            refdat = readFile.get("referenceData")
            data = np.array(refdat)
            data += rand.normal(0, 1, len(data))
            doTrue = False
            readFile.close()

        # there is data here... analysis time
        else:
            TruthAP = readFile.get("APData%d" % counter)
            TruthCT = readFile.get("CTData%d" % counter)
            TruthAP = np.array(TruthAP)
            TruthCT = np.array(TruthCT)
            data = np.array(data)
            doTrue = True
            readFile.close()

    # try and collect initial guess values to make curve fit easier by searching for peaks

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

        
        # Collect data on total number of afterpulses and cross talks found vs how many there actually are.
        if doTrue == True:
            trueAP += TruthAP[0]
            trueCT += TruthCT[0]
            trueCTD += TruthCT[1]
        if pulseData.numAfterPulses > 0:
            for i in pulseData.afterPulseTimes:
                if i < 1000:
                    countCTD += 1
                    
                else:
                    countAP += 1
                    allTimes = np.append(allTimes, i)
        
        countCT += pulseData.numPromptCT
                          
        # curve fit time (cross fingers)
        initguess = []
        initguess.append(pulseData.numPromptCT * 167) #amplitude
        initguess.append(0)                     #onset time
        initguess.append(2.0)                   #rise time
        initguess.append(5.0)                   #rise time long
        initguess.append(4.0)                   #sharp decay time
        initguess.append(10.0)                  #long decay time                                    
        for i in range(pulseData.numAfterPulses):
            initguess.append(pulseData.afterPulseAmplitudes[i])
            initguess.append(pulseData.afterPulseTimes[i]- 4)     
            initguess.append(2.0)  
            initguess.append(5.0)                          
            initguess.append(4.0)                           
            initguess.append(10.0)  
        for i in range(pulseData.numDelayedCT):
            initguess.append(pulseData.DelayedCTAmplitudes[i])
            initguess.append(pulseData.DelayedCTTimes[i] - 4)     
            initguess.append(2.0)  
            initguess.append(5.0)                          
            initguess.append(4.0)                          
            initguess.append(10.0) 


        try:
            fitParams, fitCovariances = curve_fit(pulse_superpositions, xdata, data, p0 = initguess)
        except (RuntimeError, ValueError):
            fitParams = None


        counter += 1
        
        print(f"{counter}: {fitParams}")
    

    
    print(f"Found AP: {countAP}/{trueAP}")
    print(f"Found CTP: {countCT}/{trueCT}")
    print(f"Found CTD: {countCTD}/{trueCTD}")
    print(allTimes)


def calculate_num_peaks(data, template):
    # step 1, apply a matched filter with the archetype pulse to clean up signal.
    filtered_data = signal.correlate(data, template, mode= 'same')
    filtered_data /= np.max(filtered_data) # normalise for ease

    # find the number of peaks in the matched filter data which is the same as for
    # the raw data. This should account for pulses overlapping
    peaks = signal.find_peaks(filtered_data, height=0.1)
    num_peaks = len(peaks[1]['peak_heights'])
    peak_positions = peaks[0]
    return num_peaks, peak_positions

def calculate_promptCT(amplitude, template):
    PE = np.amax(template) # one photon energy is the max value in the archetype pulse
    
    ampInPE = (amplitude/PE)
    ampInPE = np.round(ampInPE)
    ampInPE -= 1
    return ampInPE

def pulse_superpositions(t, *pos):
    ''' add pulses together to make a compund pulse '''
    pulseSuperPos = 0
    for i in range(0, len(pos), 6):
        pulseSuperPos += pulseFitFunc(t, pos[0 + i], 
                                         pos[1 + i], 
                                         pos[2 + i], 
                                         pos[3 + i],
                                         pos[4 + i],
                                         pos[5 + i])
    return pulseSuperPos

def pulseFitFunc(t, scale, onset, taurise, tauriselong, taushort, taulong):
    ''' overdamped harmonic oscillator analytical solution.'''
    temp1  = np.exp(-(t - onset) / taushort)
    temp2  = np.exp(-(t - onset) / taulong)
    decay = temp1 + temp2
    pulse = - scale * (np.exp(-(t - onset) / taurise) + np.exp(-(t - onset) / tauriselong) - decay)
    pulse[np.where(t < onset)] = 0.0 # not defined before onset time, set 0
    return pulse

if __name__ == '__main__':
    main()