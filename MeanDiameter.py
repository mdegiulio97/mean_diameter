import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d, interpolate

df = pd.read_csv(r"C:\Users\info\PycharmProject\mean_diameter\test\test2.csv", sep=";", decimal=',', encoding="latin-1")

DiaTime = df['Diastolic Time [sec]']# Diastolic time (time of min)
DiaTime = np.array(DiaTime)
DiaTime = DiaTime[~np.isnan(DiaTime)]

SysTime = df['Systolic Time [sec]']# Systolic time (time of max)
SysTime = np.array(SysTime)

EndPulse = df['End Pulse Time [sec]']# Cycle end point
EndPulse = np.array(EndPulse)
EndPulse = EndPulse[~np.isnan(EndPulse)]

Time = df['Tempo [ms]']# Time of simulation
Time = np.array(Time)

Diameter = df['Diametro [mm]']# Diameter value for each instant of time
Diameter = np.array(Diameter)

diameterDia = df['Diametro Diastolico [mm]']# Diameter diastolic
diameterDia = np.array(diameterDia)

diameterSys = df['Diametro Sistolico [mm]']# Diameter systolic
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
    CyclePoint.append(numPoint)
print('Cycle point :', CyclePoint)

# calculation of the points of each cycle
for i in range(len(CyclePoint)):
    CyclePoint[i] /= period
    CyclePoint[i] = round(CyclePoint[i], 2)
    CyclePoint[i] = int(CyclePoint[i])
print('The number of points for each cycle are:', CyclePoint)

# calculation of mean and median
for i in range(len(CyclePoint)):
    meanPoint = np.mean(CyclePoint)
    meanPoint = round(meanPoint)
    meanPoint = int(meanPoint)
    median = np.median(CyclePoint)
    median = int(median)
print('The average of the points per cycle is:', meanPoint)
print('The median is:', median)

# limit value accept: 15% of median
rate_median = (median*15)/100
rate_median = round(rate_median)
print('The range relative to the median in percent is +/-', rate_median)

# delete bad cycle
CyclePoint_original = CyclePoint.copy()
DiaTime = DiaTime.tolist()#covert array in list and use 'pop' to remove the bad cycle
for i in range(len(CyclePoint_original)-1, -1, -1):
    if (CyclePoint_original[i] > (median + rate_median)) or (CyclePoint_original[i] < (median - rate_median)):
        CyclePoint.pop(i)
        DiaTime.pop(i)

max_CyclePoint = max(CyclePoint)
size_CyclePoint = len(CyclePoint)

# create a empty matrix

# matrix filling
matrix = [[float('NaN')] * max_CyclePoint for i in range(size_CyclePoint)] #create a empty matrix
time_index = 0
x_new = np.linspace(0, 10, num=max_CyclePoint, endpoint=True)
for n in range(len(DiaTime)):
    vet = []
    while Time[time_index] < (DiaTime[n]-0.001):
        time_index += 1
    for i in range(CyclePoint[n]):
        vet.append(Diameter[time_index])
        time_index += 1
    x = np.linspace(0, 10, num=i+1, endpoint=True)
    f = interp1d(x, vet, kind='cubic')
    y_new = f(x_new)
    matrix.insert(n, vet)
print(matrix)

#matrix[n][i] = Diameter[time_index]





#print(matrix.shape)
matrix = np.array(matrix)
meanCol = np.mean(matrix, axis=0)
#print(meanCol) 


# plot of diameter variation over time
plt.figure(1)
plt.plot(Time[:], Diameter[:])
plt.xlabel("Time [ms]")
plt.ylabel("Diameter [mm]")
plt.title("diameter variation over time")

# plot of the time/diameter curve on average
plt.figure(2)
plt.plot(meanCol)
plt.title("mean time/diameter curve")
plt.show()
