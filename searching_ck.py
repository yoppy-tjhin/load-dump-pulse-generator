# A Python code to find the value of Ck,
# by searching Ck until the target rise time is found.

import numpy as np
from scipy.optimize import brentq
import matplotlib.pyplot as plt

Cb = 43e-3          # 43 mF
R1 = 2              # 2 ohm
R2 = 4              # 4 ohm
V1_0 = 100          # Let V1(0) = 100 volt
target_rt = 0.01    # 10 ms
 
t = np.linspace(0,0.2,20000)


def V2_waveform(Ck):
    print(Ck)
    trA = -( (1/R1 + 1/R2)/Cb + 1/(R1*Ck) )
    detA = 1/(R1*R2*Cb*Ck)

    disc = np.sqrt(trA**2 - 4*detA)

    l1 = (trA + disc)/2
    l2 = (trA - disc)/2

    K = V1_0/(R1*Ck*(l1-l2))

    V2 = K*(np.exp(l1*t)-np.exp(l2*t))

    return V2


def rise_time(Ck):
    V2 = V2_waveform(Ck)
    peak = np.max(V2)
    v10 = 0.1*peak
    v90 = 0.9*peak

    try:
        t10 = t[np.where(V2>=v10)[0][0]]
        t90 = t[np.where(V2>=v90)[0][0]]
    except:
        return None

    return t90 - t10

def objective(Ck):
    rt = rise_time(Ck)

    if rt is None:
        return 1

    return rt - target_rt   # 10 ms target


Ck = brentq(objective, 1e-6, 0.5)       # Ck boundary: 1uF - 0.5 F

print("Ck =",Ck,"F")

V2 = V2_waveform(Ck)

plt.plot(t,V2)
plt.xlabel("Time (s)")
plt.ylabel("V2 (V)")
plt.grid()
plt.show()
