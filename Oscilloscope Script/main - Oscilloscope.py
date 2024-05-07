from readtrc import Trc
import matplotlib.pyplot as plt
import numpy as np
from os.path import isfile, join
from os import listdir
import os
import netCDF4
import NCLoadMPL

'''
v = s/t 
s = vt/2 (ไป-กลับ)


def MoveAver(arr, window_size = 5):
    result = []
    arr = arr.copy()
    for i in range(len(arr) - window_size + 1):
        window = arr[i : i + window_size]
        aver = sum(window) / window_size
        result.append(aver)
    print(len(result), len(arr[round(window_size/2): -(round(window_size/2)+1)+1]))
    arr[round(window_size/2): -(round(window_size/2)+1)+1] = result
    return arr
'''

def MoveAver(arr, window_size=5):
    result = []
    arr_copy = arr.copy()  # Make a copy of the input array
    for i in range(len(arr_copy) - window_size + 1):
        window = arr_copy[i : i + window_size]
        aver = sum(window) / window_size
        result.append(aver)
    start_index = (window_size - 1) // 2  # Calculate start index
    end_index = len(arr_copy) - (window_size // 2)  # Calculate end index
    arr_copy[start_index:end_index] = result
    return arr_copy

def norm_arr(arr):
    max_value = arr.max()
    #min_value = arr.min()
    for i in range(len(arr)):
        #arr[i] = (arr[i] - min_value) / (max_value - min_value)
        arr[i] = (arr[i]) / (max_value)
        
# Fix Param
trc = Trc()
light_speed = 3e8

#-------------------------------------------------------------------------------
path        = r"C:\Users\Optics_Lab_010\Desktop\Work\Lidar\Cheer\ALiN PC test#1\03-04 20-35\\"
#plot_name = "1st On Sky Oscilloscope Captured Data"    #plot_name = "PMT in the front of the Laser"
plot_name   = "4 Apr 2024 Oscilloscope 200 Stacks Data Beam Expander (20:35)"
#-------------------------------------------------------------------------------

'''
Wave Data # time[1]-time[0]
Channel 1: PMT signal 
Channel 2: Laser Sync Laser
'''

### Data from Oscilloscope
C1_lst  = [trc.open(join(path, f))[1] for f in listdir(path) if isfile(join(path, f)) and 'C1' == f[:2]]
C1      = np.mean(C1_lst, axis=0)
C1      = (C1 * -1)

### Trig Data
C2_file = [join(path, f)  for f in listdir(path) if isfile(join(path, f)) and 'C2' == f[:2]]
C2_lst  = [trc.open(f)[1] for f in C2_file]
Trig    = np.mean(C2_lst, axis=0)
fName   = C2_file[0]
time    = trc.open(fName)[0]
time    = time-10e-6


'''
Trig = np.zeros(len(time))
Trig[time > 0] = 3
Trig[time > 1e-6] = 0
'''

### Time Travel
distance   = time*light_speed/2 
rs_C1_pure      = C1 * distance * distance
rs_C1           = MoveAver(rs_C1_pure, 39)
norm_arr(rs_C1)
### Logaritm Gradient Method
'''
np.array(np.diff(np.log(rs_C1))/(distance[1]-distance[0])).min()
'''

#------------------------------------------ Plot Distance ------------------------------------------#
fig, ax1 = plt.subplots()
fig.suptitle(plot_name)
plt.title('Corrected R-squared', fontsize = 10)


### PMT Signal and plot
color = 'tab:red'
ax1.set_ylabel('distance [m]')
ax1.set_xlabel('Digitizer Signal [$v*m^{2}$]',
               color=color)
lns1 = ax1.plot(rs_C1, distance,
                color=color, label='Oscilloscope')
ax1.tick_params(axis='y')

### LiDAR MPL
com_path        = NCLoadMPL.get(path = r'C:\Users\Optics_Lab_010\Desktop\Work\Lidar\Cheer\ALiN PC test#1\MPL_pull\\',
                                dateandtime = "202404031335") # dateandtime = "202403311245"

file2read       = netCDF4.Dataset(com_path, 'r')
com_distance    = np.array(file2read.variables["range_raw"])*1000
com_signal      = file2read.variables['copol_raw'][0] + \
                  file2read.variables['crosspol_raw'][0]
rs_com_signal   = com_signal * com_distance * com_distance
norm_arr(rs_com_signal)

### LiDAR MPL Plot
ax2 = ax1.twiny()                                                           # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_xlabel('LiDAR MPL Signal (range corrected)',
               color=color)                                                 # we already handled the x-label with ax1
lns2 = ax2.plot(rs_com_signal, com_distance,
                color=color, label='LiDAR MPL')
ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()                                                          # otherwise the right y-label is slightly clipped

### Label Integrate
lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0)

### Set limits for the x and y axes
ax1.set_ylim([0, max(distance)])
ax1.set_xlim(0, 1)
ax2.set_xlim(0, 1)
#ax1.set_xscale('log')
#plt.autoscale(axis='Y', tight=None)

plt.savefig('img\Oscilloscope altitude.png')
#plt.ion()



#----------------------------------------------- Plot Time ---------------------------------------------#
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
fig.suptitle(plot_name)
plt.title('time scale', fontsize = 10)

### PMT Signal
color = 'tab:red'
ax1.set_xlabel('time [us]')
ax1.set_ylabel('PMT Signal [V]', color=color)
ax1.plot(time*1e6, C1, color=color)
ax1.tick_params(axis='y', labelcolor=color)

### Laser Sync Signal
color = 'tab:blue'
ax2.set_ylabel('Laser Sync Signal [V]', color=color)  # we already handled the x-label with ax1
ax2.plot(time*1e6, Trig, color=color)
ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig('img\Oscilloscope time.png')
plt.show()

'''
# the sum of absolute differences
sad = []
max_win = 120
for k in range(3, max_win+3, 3):
  smoothedSignal = MoveAver(rs_C1_pure, k)
  sad.append(sum(abs(rs_C1_pure - smoothedSignal)))

idx = np.linspace(3, max_win, int(max_win/3))
plt.plot(idx, sad)
plt.show()
'''











































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
