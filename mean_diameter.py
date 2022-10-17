import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import sys

#open file csv and plot the file
df = pd.read_csv(r"test2.csv", sep=";", decimal=',' , encoding="latin-1" )

DiaTime = df ['Diastolic Time [sec]'] #diastolic time (time of min)
DiaTime = np.array(DiaTime)
DiaTime = DiaTime[~np.isnan(DiaTime)]

SysTime = df ['Systolic Time [sec]'] #systolic time (time of max)
SysTime = np.array(SysTime)

EndPulse = df['End Pulse Time [sec]'] #cycle end point
EndPulse = np.array(EndPulse)
EndPulse = EndPulse[~np.isnan(EndPulse)]

Time = df['Tempo [ms]'] #time of simulation
Time = np.array(Time)

Diameter = df['Diametro [mm]'] #Diameter value for each instant of time
Diameter = np.array(Diameter)

diameterDia = df['Diametro Diastolico [mm]'] #Diameter diastolic
diameterDia = np.array(diameterDia)

diameterSys = df['Diametro Sistolico [mm]'] #Diameter systolic
diameterSys = np.array(diameterSys)

period = Time[1] - Time[0]
period = round(period, 2)
print('Period (s) :', period)

freq = 1/period
freq = round(freq, 2)
print('Frequency (Hz) :', freq)

CyclePoint = []
for i in range(len(EndPulse)):
    numPoint = EndPulse[i] - DiaTime[i]
    CyclePoint.append((numPoint))
print('Cycle point :', CyclePoint)

#calculation of the points of each cycle
for i in range(len(CyclePoint)):
    CyclePoint[i] /= period
    CyclePoint[i] = round(CyclePoint[i], 2)
    CyclePoint[i] = int(CyclePoint[i])
print('The number of points for each cycle are:',CyclePoint)

#calculation of mean and median
for i in range(len(CyclePoint)):
    meanPoint = np.mean(CyclePoint)
    meanPoint = round(meanPoint)
    meanPoint = int(meanPoint)
    median = np.median(CyclePoint)
    median = int(median)
print('The average of the points per cycle is:',meanPoint)
print('The median is:', median)

#limit value accept: 15% of median
rate_median = (median*15)/100
rate_median = round(rate_median)
print('The range relative to the median in percent is +/-', rate_median)

#delete bad cycle
for i in range(len(CyclePoint)):
    if (CyclePoint[i] > (median + rate_median)) or (CyclePoint[i] < (median - rate_median)):
        CyclePoint.pop(i)
        DiaTime = DiaTime.tolist() #covert array in lisr and use 'pop' to remove the bad cycle
        DiaTime.pop(i)

max_CyclePoint = max(CyclePoint)
size_CyclePoint = len(CyclePoint)

#create a empty matrix
matrix = [[float('NaN')]*max_CyclePoint for i in range(size_CyclePoint)]

time_index = 0
for n in range(len(DiaTime)):
    while Time[time_index] < (DiaTime[n]-0.001):
        time_index += 1
    for i in range(CyclePoint[n]):
        matrix[n][i] = Diameter[time_index]
        time_index += 1
print(matrix)

MeanCol = []
Col = []
for i in range(size_CyclePoint):
    value = matrix[n][i]
    Col.append(value)
    n += 1
mean = np.mean(Col)
MeanCol.append(mean)


#plot1 :
#plt.figure()
plt.plot(Time[:], Diameter[:])
plt.xlabel("Time [ms]")
plt.ylabel ("Diameter [mm]")
plt.title("variazione nel tempo del diametro")
#plt.show()


