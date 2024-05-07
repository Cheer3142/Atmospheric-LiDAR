import matplotlib.pyplot as plt
import numpy as np
from os.path import isfile, join
from os import listdir
import os
import pandas as pd
import netCDF4

# Fix Param v = s/t >> s = vt/2
file_path = '24-03-2024.dat'
plot_name = "24 Mar 2024 TR 500 stacks"

with open(file_path, 'r') as file:
    headrow = 0
    for line in file:
        if "BT0" in line:
            bin_num = float(line.split()[6])
        if "Analog" in line: break
        headrow += 1
print(headrow)

# Wave Data # time[1]-time[0]
'''
Channel 1: PMT signal 
Channel 2: Laser Sync Laser
'''
df          = pd.read_csv(file_path, delimiter='\t', skiprows=headrow)
distance    = df.index*bin_num/2 - 750

#print(d)

# Trig Data
'''
Trig = np.zeros(len(time))
Trig[time > 0] = 3
Trig[time > 1e-6] = 0
distance = time*light_speed/2 # Time Travel
'''
data       = df.iloc[:, 0] + df.iloc[:, 2]
rs_data    = data * distance * distance

# Logaritm Gradient Method
'''
np.array(np.diff(np.log(rs_C1))/(distance[1]-distance[0])).min()
'''
#---------------------------- Plot Distance ----------------------------#
fig, ax1 = plt.subplots()
fig.suptitle(plot_name)
plt.title('Corrected R-squared', fontsize = 10)


# PMT Signal
color = 'tab:red'
ax1.set_ylabel('distance [m]')
ax1.set_xlabel('Digitizer Signal [$v*m^{2}$]', color=color)
lns1 = ax1.plot(rs_data, distance, color=color, label='TR')
ax1.tick_params(axis='y')

### LiDAR MPL
com_path = r"C:\Users\Optics Lab 2\Documents\Cheer\Laser Lidar\LiDARIntercomparison\\"
com_fname = "MPL_5038_202403241215.nc"

file2read = netCDF4.Dataset(com_path+com_fname, 'r')
com_distance = np.array(file2read.variables["range_raw"])*1000
com_signal = file2read.variables['copol_raw'][0] + \
             file2read.variables['crosspol_raw'][0]
rs_com_signal = com_signal * com_distance * com_distance

### LiDAR MPL Plot
ax2 = ax1.twiny()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_xlabel('LiDAR MPL Signal (range corrected)', color=color)  # we already handled the x-label with ax1
lns2 = ax2.plot(rs_com_signal, com_distance, color=color, label='LiDAR MPL')
ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()  # otherwise the right y-label is slightly clipped

### Label Integrate
lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0)

# Set limits for the x and y axes
#ax1.set_ylim([0, 3500])
#ax1.set_ylim([0.04, max(C1)])
#ax1.set_xscale('log')
#plt.gca().invert_xaxis()
#plt.autoscale(axis='Y', tight=None)
start, stop = 0, 3500
'''
ax1.set_xlim([min(rs_data[round(start*2/3.75):round(stop*2/3.75)]),
              max(rs_data[round(start*2/3.75):round(stop*2/3.75)])])
'''
ax1.set_ylim([start, stop])

plt.savefig('TR altitude.png')
plt.ion()
plt.show()

### Full Range
fig, ax1 = plt.subplots()
fig.suptitle(plot_name)
plt.title('Corrected R-squared', fontsize = 10)


# PMT Signal
color = 'tab:red'
ax1.set_ylabel('distance [m]')
ax1.set_xlabel('Digitizer Signal [$v*m^{2}$]', color=color)
ax1.plot(rs_data, distance, color=color)
ax1.tick_params(axis='y', labelcolor=color)

'''
# Laser Sync Signal
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('Laser Sync Signal (V)', color=color)  # we already handled the x-label with ax1
ax2.plot(distance, Trig, color=color)
ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
'''

# Set limits for the x and y axes
#ax1.set_ylim([0, 3500])
#ax1.set_ylim([0.04, max(C1)])
#ax1.set_xscale('log')
#plt.gca().invert_xaxis()
#plt.autoscale(axis='Y', tight=None)

plt.savefig('TR full range.png')
plt.ion()
plt.show()

'''
#---------------------------- Plot Average ----------------------------#
plt.plot(time_cat, datY_cat, color=color)
plt.show()
'''
























'''
# Or alternatively
plt.plot(trc.x, trc.y)
#print(trc.d)

'''
'''
datY_cat = np.concatenate([datY]*clone, axis=None)
time = time+1e-6    # Offset Time
time_cat = np.linspace(time[0], time[0]+(time[1]-time[0])*(datY_cat.shape[0]-1), datY_cat.shape[0])
'''
