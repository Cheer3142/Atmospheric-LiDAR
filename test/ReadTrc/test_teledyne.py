from readtrc import Trc
import matplotlib.pyplot as plt
import numpy as np

# Wave Data
# time[1]-time[0]
trc                 = Trc()
fName               = "C2--100ms--00000.trc" # 
time, datY, d       = trc.open(fName)


print(fName)
for i in d:
    if i == "PNTS_PER_SCREEN" or i == "HORIZ_INTERVAL":
        print(i, d[i])

'''
# Or alternatively
plt.plot(trc.x, trc.y)
#print(trc.d)

'''
