import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import sys

#df = pd.read_csv(r"C:\Users\info\OneDrive\Desktop\test_28_06_2022.csv", sep=";", encoding="latin-1" )
#df.columns = ['Diametro Diastolico', 'Diametro Sistolico', 'Tempo', 'Diametro', 'IMT medio']

df = pd.read_csv(r"C:\Users\info\OneDrive\Desktop\test_03_08_2022.csv", sep=";", encoding="latin-1" )
print (df)

""""
#per test(22-06-2022)
t = df['Tempo']
tempo = np.array(t)

d = df['Diametro'][25:241]
diametro = np.array(d)
diametro = diametro.astype(float) #[25:241]

min = df['Diametro Diastolico'][0:10]
min = np.array(min)
min = min.astype(float)
"""

"""
#per test(22-06-2022)
lista_indici = []
for i in min:
    for j in diametro:
        compare = math.isclose(min[i],diametro[j])
        if compare == True:
            lista_indici.append(j)
            index = j
            i += 1
            j += index
        else:
            index = j
            j += index
print (lista_indici)
"""

"""
#andamento del diametro nel tempo con i dati ottenuti direttamnte dal CVSuite
plt.figure()
plt.plot(tempo[:], diametro[:])
plt.xlabel("Tempo [ms]")
plt.ylabel ("Diametro [mm]")
plt.title("variazione nel tempo del diametro")
plt.show()
"""














