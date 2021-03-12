import csv
import numpy as np

def reader(filename):

    datlist = []
    dial = "Space"
    xVals = np.array([])
    Voltage = np.array([])


    csv.register_dialect("Space", delimiter=" ")

    with open(filename, "r", newline='') as file:
        data = csv.reader(file, dialect=dial)
        for row in data:
            datlist.append(row)

        for index in range(0, len(datlist), 1):
            if datlist[index][5] != "-nan":
                xVals = np.append(xVals, float(datlist[index][2]) * 10**9)
                Voltage = np.append(Voltage, float(datlist[index][5]) * 10**3)

    return(xVals, Voltage)
         
