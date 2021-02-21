import Datareader as dr
import numpy as np
import numpy.random as rand
import h5py
import matplotlib.pyplot as plt

# Simulation Parameters
NUMSIMS = 100
deadTime = 1000
recoveryTime = 200
crossTalkProbTotal = 0.25
neighbours = 4
crossTalkProb = 1 - (1 - crossTalkProbTotal)**(1/neighbours)
XLEN = 150000
AFTERPULSEPROB = 0.05
TAU = 50000
FILEOUTPUT = "data.h5"

def main():

    dataFile = h5py.File(FILEOUTPUT, 'w')
    dataFile.close()

    counter = 0
    xdata = np.array([])
    ydata = np.array([])
    xdata, ydata = dr.reader("londat.csv")
    xdata = np.arange(XLEN)

    # Save teh xdata into the h5py file
    dataFile = h5py.File(FILEOUTPUT, 'a')
    dataFile.create_dataset("xdata", data = xdata)

    spadPulse = np.zeros(XLEN)
    ydata.resize(spadPulse.shape)
    spadPulse = spadPulse + ydata

    dataFile.create_dataset("referenceData", data = spadPulse)

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
         

        saveData(spadPulse, afterpulseData, crossTalkData, counter)
        
        plt.plot(xdata, spadPulse)
        
        counter += 1
        if counter%10000 == 0:
            print(counter)

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
            scale = (1 - np.exp(-(time - deadTime)/4500)) # still an arbitrary scale factor
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
    promptProb = 0.6
    delayed = 0
    CTData = np.array([0, 0])
    for _ in range(0, Pulses):
        if rand.rand() < promptProb:
            spadPulse += ydata
            CTData[0] += 1
        else:
            time = rand.randint(10, 100)
            CTData = np.append(CTData, time)
            for i in range(time, len(ydata)):
                spadPulse[i] = (spadPulse[i] + (ydata[(i - time)]))
            
            
            delayed += 1
    
    CTData[1] = delayed
    return(CTData)


#**************************************************************************************
# make the data file and fill it with data : )
def saveData(Data2Save, APData, CTData, DataNumber):
    # Open data file
    dataFile = h5py.File(FILEOUTPUT, 'a')
    if APData[0] != 0 or CTData[1] != 0 or CTData[0] != 0:
        # Append the spad data and truth data to the file
        dataFile.create_dataset(f"SPADPulse{DataNumber}", data = Data2Save)
        dataFile.create_dataset(f"APData{DataNumber}", data = APData)
        dataFile.create_dataset(f"CTData{DataNumber}", data = CTData)
    else:
        dataFile.create_dataset(f"SPADPulse{DataNumber}", data = [0])

    # Close the file
    dataFile.close()


if __name__ == '__main__':
    main()

