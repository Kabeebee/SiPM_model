import Datareader as dr
import numpy as np
import numpy.random as rand
import h5py
import matplotlib.pyplot as plt

# Simulation Parameters
NUMSIMS = 20
deadTime = 20
recoveryTime = 200
crossTalkProbTotal = 0.5
neighbours = 4
crossTalkProb = 1 - (1 - crossTalkProbTotal)**(1/neighbours)

def main():
    counter = 0
    fig, ax = plt.subplots()
    xdata = np.array([])
    ydata = np.array([])
    xdata, ydata = dr.reader("londat.csv")

    while counter < NUMSIMS:
       
        xdata = np.arange(200)
        spadPulse = np.zeros(200)
        ydata.resize(spadPulse.shape)
        spadPulse = spadPulse + ydata

        afterPulseProb = rand.normal(0.02, 0.08)
        if rand.rand() > 1 - afterPulseProb:
            afterpulsing(ydata, spadPulse, xdata)

        
        triggered = rand.randint(0, neighbours)
        Pulses = rand.binomial(n = triggered, p=crossTalkProb)
        if Pulses > 0:
            crossTalk(ydata, spadPulse, xdata, Pulses)
       

        randNoise(spadPulse, 1)

        ax.plot(xdata, spadPulse)
        counter += 1

    plt.show()


#**************************************************************************************
# add random fluctuations to data

def randNoise(Pulse, stdev):
    Pulse += rand.normal(0, stdev, len(Pulse))


#**************************************************************************************
# Afterpulsing
def afterpulsing(ydata, spadPulse, xdata):
    LAMBDA = 0.02
    lastPulse = 1
    counter = 0
    NUMCOUNTS = 0
    while counter < 200:
        for j in range(lastPulse, len(xdata) - lastPulse):
            pulseProb = np.exp(-NUMCOUNTS) * (1 - np.exp(- LAMBDA))
            trial = rand.rand()
            if trial > 1 - pulseProb:
                position = xdata[j] + lastPulse
                if position > lastPulse + deadTime:
                    scale = np.log(position/deadTime) / 3.1 # still an arbitrary scale factor
                    for i in range(position, len(ydata)):
                        spadPulse[i] = (spadPulse[i] + (ydata[(i - position)])) * scale
                    lastPulse = position
                    NUMCOUNTS += 1
        counter += 1

#**************************************************************************************
# Add Crosstalk 

def crossTalk(ydata, spadPulse, xdata, Pulses):
    promptProb = 0.5
    for _ in range(0, Pulses):
        if rand.rand() < promptProb:
            spadPulse += ydata
        else:
            afterpulsing(ydata, spadPulse, xdata)


#**************************************************************************************
# make the data file and fill it with data : )
def saveData(iteration, xdata,  spadPulse):
    dataFile = h5py.File('data.h5', 'w')
    dataFile.create_dataset('xdata', data = xdata)
    dataFile.create_dataset('ypulse', data = spadPulse)
    dataFile.close()

if __name__ == '__main__':
    main()

