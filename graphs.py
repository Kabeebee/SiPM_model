import matplotlib.pyplot as plt
import numpy as np
import h5py
import Datareader as dr

def ampVsTime():
    #fig, ax = plt.subplots()
    
    amps = []
    times = []
    file = h5py.File("mergedData.h5")
    for i in range(0, 100000, 20):
        data = file.get(f"Parameters{i}")
        data = np.array(data)
        if np.size(data) > 1:
            maxL = np.size(data)/6
            for p in range(0, int(maxL)):
                amps.append(data[p*6])
                times.append(data[p*6 + 1])
            
    
    file.close()
    #plt.xscale("log")
    #plt.xlim([0, 200000])
    #ax.scatter(times, amps)
    #plt.show()
    return(times, amps)
   

def APAtTime():
    fig, ax = plt.subplots()
    times = []
    file = h5py.File("mergedData.h5")
    for i in range(0, 100000):
        
        data = file.get(f"Parameters{i}")
        data = np.array(data)
        
        if np.size(data) > 6:
            maxL = np.size(data)/6
            for p in range(1, int(maxL)):
                if data[p*6 + 1] > 999:
                    times.append(data[p*6 + 1])
    file.close()
    
    ax.hist(times, range(0, 200000, 1000))
    plt.show()


def ampdistro():
    fig, ax = plt.subplots()
    amps = []
    file = h5py.File("mergedData.h5")
    for i in range(0, 100000):
        
        data = file.get(f"Parameters{i}")
        data = np.array(data)
        if np.size(data) > 6:
            if data[7] < 999 and data[6] > 275 and data[6] < 300:
                print(i)

    plt.plot([169]*230, range(0, 2300, 10), "r--", label="True Mean Value" )
    ax.hist(amps, range(120, 300, 5), color="b")
    plt.ylabel("Number of Pulses")
    plt.xlabel("Amplitude (mv)")
    plt.show()


def APAmps():
    fig, ax = plt.subplots()
    amps = []
    file = h5py.File("mergedData.h5")
    for i in range(0, 100000):
        
        data = file.get(f"Parameters{i}")
        data = np.array(data)
        
        if np.size(data) > 6:
            maxL = np.size(data)/6
            for p in range(1, int(maxL)):
                if data[p*6 + 1] > 999:
                    amps.append(data[p*6])

    file.close()
    
    ax.hist(amps, range(120, 350, 5))
    plt.show()


def singlepulse():
    xvals, yvals = dr.reader("londat.csv")
    plt.xlabel("Time (ns)")
    plt.ylabel(u"Voltage (mv)")
    plt.yticks(range(0, 180, 10))
    plt.xticks(list(range(0, 180, 10)) + [10])
    plt.plot(xvals, yvals, "r", label="SPAD Pulse")
    plt.plot([3.6]* 175, range(0, 175), "b--", label="t = 3.6ns")
    plt.legend()
    plt.show()


def PlotAll():
    fig = plt.figure()
    ax = fig.add_subplot()
    ins = ax.inset_axes([0.55, 0.55, 0.38, 0.38])
    file = h5py.File(r"F:\data.h5")
    l = 0
    for i in range(0, 100000, 50):
        data = file.get(f"SPADPulse{i}")
        data = np.array(data)
        if np.size(data) > 1:
            plt.plot(range(0, 150000), data)
            l +=1
            ins.plot(range(0, 150), data[:150])

    print(l)

    plt.ylabel("Voltage (mv)")
    plt.xlabel("Time (ns)")
    plt.show()

        
def truthvsreal():
    amps = []
    times = []
    amps2 = []
    times2 = []
    file = h5py.File(r"F:\data.h5")
    for i in range(0, 100000, 20):
        try:

            data = file.get(f"APData{i}")
            data = np.array(data)
            
            for p in range(0, int(data[0])):
                amps.append(data[2* p + 2] * 167)
                times.append(data[2* p + 1])
                
                
            data2 = file.get(f"CTData{i}")
            data2 = np.array(data2)
            amps.append((1 + data2[0]) * 167 + np.random.normal(0 , 2, 1))
            times.append(0)

            for p in range(0, data2[1]):
                amps.append(167 + np.random.normal(0 , 2, 1))
                times.append(data2[p + 2])
            
            if np.size(data2) < 1:
                amps.append(167 + np.random.normal(0 , 2, 1))
                times.append(0)
            
        except:
            amps.append(167 + np.random.normal(0 , 2, 1))
            times.append(0)

    file.close()

    fig, ax = plt.subplots()
    
    plt.xscale("log")
    plt.xlim([5, 200000])
    plt.xlabel("Time (ns)")
    plt.ylabel("Voltage (mv)")
    times2, amps2 = ampVsTime()
    ax.scatter(times2, amps2, c="k", marker=".")
    ax.scatter(times, amps, c="r", marker="x", linewidths=0.75)
    plt.show()

        


def main():
    #ampVsTime()
    #APAtTime()
    ampdistro()
    #APAmps()
    #singlepulse()
    #PlotAll()
    #truthvsreal()

if __name__ == "__main__":
    main()




