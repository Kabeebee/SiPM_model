import Datareader as dr
import numpy as np
import numpy.random as rand
import h5py
import matplotlib.pyplot as plt

# Simulation Parameters
NUMSIMS = 100
deadTime = 20
recoveryTime = 200
crossTalkProbTotal = 0.5
neighbours = 4
crossTalkProb = 1 - (1 - crossTalkProbTotal)**(1/neighbours)
XLEN = 2000
AFTERPULSEPROB = 0.05
TAU = 100

def main():
    counter = 0
    fig, ax = plt.subplots()
    xdata = np.array([])
    ydata = np.array([])
    xdata, ydata = dr.reader("londat.csv")

    while counter < NUMSIMS:
       
        xdata = np.arange(XLEN)
        spadPulse = np.zeros(XLEN)
        ydata.resize(spadPulse.shape)
        spadPulse = spadPulse + ydata


        #use binomial distrobution along with total afterpulse prob to determin number of afterpulses
        afterPulses = rand.poisson(AFTERPULSEPROB)
        if afterPulses > 0:
            afterpulsing(ydata, spadPulse, xdata, afterPulses)

        
        triggered = rand.randint(0, neighbours)
        crossPulses = rand.binomial(n = triggered, p=crossTalkProb)
        if crossPulses > 0:
            crossTalk(ydata, spadPulse, xdata, crossPulses)
       

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
def afterpulsing(ydata, spadPulse, xdata, pulses):
    counter = deadTime
    pulsed = 0
    invprobability = 1 - (3 / TAU)
    while counter < XLEN and pulsed < pulses:
        if rand.rand() > invprobability:
            

        counter += 1

#**************************************************************************************
# Add Crosstalk 

def crossTalk(ydata, spadPulse, xdata, Pulses):
    promptProb = 0.5
    delayed = 0
    for _ in range(0, Pulses):
        if rand.rand() < promptProb:
            spadPulse += ydata
        else:
            delayed += 1
            
    afterpulsing(ydata, spadPulse, xdata, delayed)


#**************************************************************************************
# make the data file and fill it with data : )
def saveData(iteration, xdata,  spadPulse):
    dataFile = h5py.File('data.h5', 'w')
    dataFile.create_dataset('xdata', data = xdata)
    dataFile.create_dataset('ypulse', data = spadPulse)
    dataFile.close()

if __name__ == '__main__':
    main()

