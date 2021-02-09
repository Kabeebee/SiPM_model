import Datareader as dr
import numpy as np
import numpy.random as rand
import h5py
import matplotlib.pyplot as plt

# Simulation Parameters
NUMSIMS = 10
deadTime = 20
recoveryTime = 200
crossTalkProbTotal = 0.5
neighbours = 4
crossTalkProb = 1 - (1 - crossTalkProbTotal)**(1/neighbours)
XLEN = 2000
AFTERPULSEPROB = 0.05
TAU = 100

# create array to store truth data
truthData = np.array([0, [], 0, 0, []], dtype=object)


def main():

    counter = 0

    fig, ax = plt.subplots()
    xdata = np.array([])
    ydata = np.array([])
    xdata, ydata = dr.reader("londat.csv")

    saveData(xdata, "Time")

    while counter < NUMSIMS:

        truthData[0] = 0
        truthData[1] = []
        truthData[2] = 0
        truthData[3] = 0
        truthData[4] = []
       
        xdata = np.arange(XLEN)
        spadPulse = np.zeros(XLEN)
        ydata.resize(spadPulse.shape)
        spadPulse = spadPulse + ydata


        #use binomial distrobution along with total afterpulse prob to determin number of afterpulses
        afterPulses = rand.poisson(AFTERPULSEPROB)
        if afterPulses > 0:
            truthData[0] = afterPulses
            afterpulsing(ydata, spadPulse, xdata, afterPulses)

        
        triggered = rand.randint(0, neighbours)
        crossPulses = rand.binomial(n = triggered, p=crossTalkProb)
        if crossPulses > 0:
            crossTalk(ydata, spadPulse, xdata, crossPulses)
       

        randNoise(spadPulse, 1)
         
        ax.plot(xdata, spadPulse)

        pulseDataName = "SpadPulse%d" % (counter)
        saveData(spadPulse, pulseDataName)
        counter += 1

    plt.show()


#**************************************************************************************
# add random fluctuations to data

def randNoise(Pulse, stdev):
    Pulse += rand.normal(0, stdev, len(Pulse))


#**************************************************************************************
# Afterpulsing
def afterpulsing(ydata, spadPulse, xdata, pulses, ap = True):
    time = deadTime
    pulsed = 0
    # calculate (1 - probability) so that random number can just be generated and compared
    invprobability = 1 - (3 / TAU) # this is 1 - dt/tau where tau is expected time for recombination
    while time < XLEN and pulsed < pulses: 
        if rand.rand() > invprobability:
            #scaling factor for pulse amplitude
            scale = (1 - np.exp(-(time - deadTime/8.68588))) # still an arbitrary scale factor
            #if scale > 1:
                #scale = 1
            # Adding pulses when required
            for i in range(time, len(ydata)):
                spadPulse[i] = (spadPulse[i] + (ydata[(i - time)])) * scale

            #add position dat to truth values
            if ap == True:
                truthData[1] = np.append(truthData[1], time)
            else:
                truthData[4] = np.append(truthData[4], time)
            #skip over dead time
            time += 20
            pulsed += 1
            

        time += 1

#**************************************************************************************
# Add Crosstalk 

def crossTalk(ydata, spadPulse, xdata, Pulses):
    #promptProb = 0.5
    delayed = 0
    for _ in range(0, Pulses):
        if rand.rand() > AFTERPULSEPROB:
            spadPulse += ydata
            truthData[2] += 1
        else:
            delayed += 1
    
    truthData[3] = delayed
    afterpulsing(ydata, spadPulse, xdata, delayed, ap = False)


#**************************************************************************************
# make the data file and fill it with data : )
def saveData(Data2Save, dataName):
    dataFile = h5py.File('data.h5', 'w')
    dataFile.create_dataset(dataName, data = Data2Save)

    dataFile.close()

    print("File entry [%s] saved to disk" % (dataName))

if __name__ == '__main__':
    main()

