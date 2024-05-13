import matplotlib.pyplot as plt
import numpy as np
from os.path import isfile, join
from os import listdir
import os
import netCDF4
from SolExDataCube import *
from scipy.interpolate import interp2d
from datetime import datetime
import matplotlib.dates as mdates

### LiDAR MPL List
com_path = r"C:\Users\Cheer\Documents\_PostGrad\NARIT\LiDAR\28-03 MPL\\"
com_namelst = Dir_Read('s', com_path)[3:]

def totime(fname):
    return datetime.strptime(fname , 'MPL_5038_%Y%m%d%H%M.nc')
'''
for i in file2read.variables:
    if 'range' in i or 'pol' in i:
        print(i)

		
range_raw
crosspol_raw

crosspol_background

crosspol_snr
range_vbp
range_nrb
range_radiometer
crosspol_nrb
depolarization_ratio

copol_raw 1000
copol_snr 1000
copol_nrb 664
copol_background 1
'''
data_2d, datalst = [], []
n = len(com_namelst)
print("number of file", n)
for i in range(n):
    file2read = netCDF4.Dataset(com_path+com_namelst[i], 'r')
    '''
    if i == 0:
        com_distance = np.array(file2read.variables["range_raw"])*1000
    com_signal = file2read.variables['copol_raw'][0] + \
                 file2read.variables['crosspol_raw'][0]
    com_signal = com_signal * com_distance * com_distance
    '''
    if i == 0:
        com_distance = np.array(file2read.variables["range_nrb"])
    com_signal = file2read.variables['crosspol_nrb'][0] + \
                 file2read.variables['copol_nrb'][0]
    
    data_2d.append(com_signal)
    datalst.append(datetime.strptime(com_namelst[i].split('_')[-1],
                                     "%Y%m%d%H%M.nc"))
    file2read.close()
data_2d = np.array(data_2d)

### Interpolate
dist_idx = com_signal.shape[0]
x = np.linspace(1, dist_idx, dist_idx) 
y = np.linspace(1, n, n)

### Create interpolation function
f = interp2d(x, y, data_2d, kind='linear')
y_new = np.linspace(1, n, dist_idx)
interpolate_data_2d = f(x, y_new)


print('Original shape', data_2d.shape)
print('Interpolated shape', interpolate_data_2d.shape)

### Dont Interpolated
#interpolate_data_2d = data_2d
interpolate_data_2d = interpolate_data_2d.T
result = np.log(interpolate_data_2d/interpolate_data_2d.max())
result = interpolate_data_2d/interpolate_data_2d.max()

### Plot Imshow
fig, ax = plt.subplots()
#fig.suptitle('Pupil Plane', fontsize = 14)

# time X AXIS
x_lims = mdates.date2num([totime(com_namelst[0]),
                          totime(com_namelst[-1])])


im = ax.imshow(interpolate_data_2d
           , cmap='rainbow'
           , origin='lower'
           , extent=[x_lims[0], x_lims[-1],
                     com_distance[0], com_distance[-1]]
           , interpolation='none'
           , aspect='auto')
           #, vmin=-3, vmax=0)


ax.xaxis_date()
date_format = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()

#plt.axhline(0, color = 'r')
ax.set_title('LiDAR MPL NRB') # Raw Ranged Correction
ax.set_ylabel('distance [km]')
ax.set_xlabel('UTC time zone')
ax.set_ylim(0, 10)
plt.autoscale(False)
fig.colorbar(im)
plt.grid(axis='x')
plt.show()
