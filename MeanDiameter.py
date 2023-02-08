import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import resample
import cv2 as cv


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

average_cycle_point = np.mean(CyclePoint)
average_cycle = round(average_cycle_point, 2)
print(average_cycle)

# calculation of the points of each cycle
for i in range(len(CyclePoint)):
    CyclePoint[i] /= period
    CyclePoint[i] = round(CyclePoint[i], 2)
    CyclePoint[i] = int(CyclePoint[i])
print('The number of points for each cycle are:', CyclePoint)

# calculation of mean and median
for i in range(len(CyclePoint)):
    median = int(np.median(CyclePoint))
print('The median is:', median)

# limit value accept: 15% of median
rate_median = (median*15)/100
rate_median = round(rate_median)
print('The range relative to the median in percent is +/-', rate_median)

# delete bad cycles
CyclePoint_original = CyclePoint.copy()
DiaTime = DiaTime.tolist()#covert array in list and use 'pop' to remove the bad cycle
for i in range(len(CyclePoint_original)-1, -1, -1):
    if (CyclePoint_original[i] > (median + rate_median)) or (CyclePoint_original[i] < (median - rate_median)):
        CyclePoint.pop(i)
        DiaTime.pop(i)

for i in range(len(CyclePoint)):
    mean_Point = float(round(np.mean(CyclePoint), 2))
print('The average of the points per cycle is:', mean_Point)

max_CyclePoint = max(CyclePoint) #cycle max len
size_CyclePoint = len(CyclePoint) #number of goog cycle

# create a empty matrix
# mat filling

time_index = 0
matrix = [] #empty list
for n in range(len(DiaTime)):
    vet = [] #empty vector
    matrix.append(vet) #add every vet (list type) in one more big list

    while Time[time_index] < (DiaTime[n]-0.001):
        time_index += 1
    for i in range(CyclePoint[n]):
        vet.append(Diameter[time_index])
        time_index += 1

matrix = np.array(matrix, dtype=object)

# resize and interpolation with scipy function
for i in range(len(matrix)):
    matrix[i] = resample(matrix[i], max_CyclePoint)
mean_col = np.mean(matrix, axis=0)
#print(mean_col)

# resize and interpolation with OpenCv function
matrix_cv = matrix.copy()
for i in range(len(matrix_cv)):
    matrix_cv[i] = cv.resize(matrix[i], (1, max_CyclePoint), interpolation=cv.INTER_CUBIC)
mean_col_cv = np.mean(matrix_cv, axis=0)
print(mean_col_cv)


# plot of diameter variation over time
plt.figure(1)
plt.plot(Time[:], Diameter[:])
plt.xlabel("Time [ms]")
plt.ylabel("Diameter [mm]")
plt.title("diameter variation over time")

# plot of the time/diameter curve on average
plt.figure(2)
plt.plot(mean_col)
plt.title("mean time/diameter curve (scipy)")

# plot of the time/diameter curve on average with OpenCV
plt.figure(3)
plt.plot(mean_col_cv)
plt.title("mean time/diameter curve (OpenCV)")
plt.show()
