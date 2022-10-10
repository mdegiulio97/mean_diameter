import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import sys

#open file csv and plot the file
df = pd.read_csv(r"C:\Users\info\OneDrive\Desktop\test2.csv", sep=";", decimal = ',', encoding="latin-1" )



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

#-#-#-#-#-#-#-#-#-#-#
#print(math.isnan(EndPulse[0]))
#calculation of points for each cardiac cycle

period = Time[1] - Time[0]
period = round(period, 2)
print('Period (s) :',period)

freq = 1/period
freq = round(freq, 2)
print('Frequency (Hz) :', freq)

CyclePoint = []
for i in range (len(EndPulse)):
    numPoint = EndPulse[i] - DiaTime[i]
    CyclePoint.append((numPoint))
#print(CyclePoint)

#calculation of the points of each cycle
for i in range (len(CyclePoint)):
    CyclePoint[i] /= period
    CyclePoint[i] = round(CyclePoint[i], 2)
    CyclePoint[i] = int(CyclePoint[i])
print('The number of points for each cycle are:',CyclePoint)

#calculation of mean and median
for i in range (len(CyclePoint)):
    meanPoint = np.mean(CyclePoint)
    meanPoint = round(meanPoint)
    meanPoint = int(meanPoint)
    median = np.median(CyclePoint)
    median = int(median)
print('The average of the points per cycle is:',meanPoint)
print('The median is:', median)

# limit value accept: 10% of median
rate_median = (median*15)/100
rate_median = round(rate_median)
print(rate_median)







#plot1 :
#plt.figure()
plt.plot(Time[:], Diameter[:])
plt.xlabel("Time [ms]")
plt.ylabel ("Diameter [mm]")
plt.title("variazione nel tempo del diametro")
#plt.show()


