import matplotlib.pyplot as plt
import numpy as np
import h5py


def ampVsTime():
    fig, ax = plt.subplots()
    
    amps = []
    times = []
    file = h5py.File("mergedData.h5")
    for i in range(0, 100000):
        
        data = file.get(f"Parameters{i}")
        data = np.array(data)
        if np.size(data) > 1:
            maxL = np.size(data)/6
            for p in range(0, int(maxL)):
                amps.append(data[p*6]/167)
                times.append(data[p*6 + 1])
        file.close()    
    
    file.close()
    plt.xscale("log")
    plt.xlim([0, 200000])
    ax.scatter(times, amps)
    plt.show()

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
        if np.size(data) > 1:
            amps.append(data[0])

    ax.hist(amps, range(120, 540, 5))
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




def main():
    #ampVsTime()
    #APAtTime()
    #ampdistro()
    APAmps()


if __name__ == "__main__":
    main()




