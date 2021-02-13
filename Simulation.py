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

    dataFile = h5py.File('data.h5', 'w')
    dataFile.close()

    counter = 0

    fig, ax = plt.subplots()
    xdata = np.array([])
    ydata = np.array([])
    xdata, ydata = dr.reader("londat.csv")
    xdata = np.arange(XLEN)

    # Save teh xdata into the h5py file
    dataFile = h5py.File('data.h5', 'a')
    dataFile.create_dataset("xdata", data = xdata)

    while counter < NUMSIMS:

        # define truth arrays for this pulse
        afterpulseData = np.array([0])
        crossTalkData = np.array([0, 0])
       
        spadPulse = np.zeros(XLEN)
        ydata.resize(spadPulse.shape)
        spadPulse = spadPulse + ydata


        #use binomial distrobution along with total afterpulse prob to determin number of afterpulses
        afterPulses = rand.poisson(AFTERPULSEPROB)
        if afterPulses > 0:
            afterpulseData[0] = afterPulses
            afterpulseData = afterpulsing(ydata, spadPulse, xdata, afterPulses)

        
    
        crossPulses = rand.binomial(n = neighbours, p=crossTalkProb)
        if crossPulses > 0:
            crossTalkData = crossTalk(ydata, spadPulse, xdata, crossPulses)
       

        randNoise(spadPulse, 1)
         
        ax.plot(xdata, spadPulse)

        saveData(spadPulse, afterpulseData, crossTalkData, counter)
        
        print(f"AP{counter}: {afterpulseData}")
        print(f"CT{counter}: {crossTalkData}")
        counter += 1

    plt.show()


#**************************************************************************************
# add random fluctuations to data

def randNoise(Pulse, stdev):
    Pulse += rand.normal(0, stdev, len(Pulse))


#**************************************************************************************
# Afterpulsing
def afterpulsing(ydata, spadPulse, xdata, pulses):
    time = deadTime
    APData = np.array([pulses])
    pulsed = 0
    # calculate (1 - probability) so that random number can just be generated and compared
    invprobability = 1 - (3 / TAU) # this is 1 - dt/tau where tau is expected time for recombination
    while time < XLEN and pulsed < pulses: 
        if rand.rand() > invprobability:
            # add position dat to truth values
            APData = np.append(APData, time)
            
            #scaling factor for pulse amplitude
            scale = (1 - np.exp(-(time - deadTime/800.68588))) # still an arbitrary scale factor
            APData = np.append(APData, scale)
            
            # Add the pulse on
            for i in range(time, len(ydata)):
                spadPulse[i] = (spadPulse[i] + (ydata[(i - time)])) * scale

            #skip over dead time
            time += 20
            pulsed += 1
            

        time += 1
    return(APData)

#**************************************************************************************
# Add Crosstalk 

def crossTalk(ydata, spadPulse, xdata, Pulses):
    #promptProb = 0.5
    delayed = 0
    CTData = np.array([0, 0])
    for _ in range(0, Pulses):
        if rand.rand() > AFTERPULSEPROB:
            spadPulse += ydata
            CTData[0] += 1
        else:
            delayed += 1
    
  
    CTData[1] = delayed
    return(CTData)


#**************************************************************************************
# make the data file and fill it with data : )
def saveData(Data2Save, APData, CTData, DataNumber):
    # Open data file
    dataFile = h5py.File('data.h5', 'a')
    
    # Append the spad data and truth data to the file
    dataFile.create_dataset(f"SPADPulse{DataNumber}", data = Data2Save)
    dataFile.create_dataset(f"APData{DataNumber}", data = APData)
    dataFile.create_dataset(f"CTData{DataNumber}", data = CTData)
    # Close the file
    dataFile.close()


if __name__ == '__main__':
    main()

