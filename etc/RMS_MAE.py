import matplotlib.pyplot as plt
import numpy as np


def RMSE(y, y_pre):
    delta = y - y_pre
    sigma_delta_square = sum(delta**2)
    rmse = (sigma_delta_square/len(y))**0.5
    return rmse

def MAE(y, y_pre):
    delta = y - y_pre
    abs_delta = sum(abs(delta))
    mae = abs_delta/len(y)
    return mae

### Initial Data    
x       = np.ones(10)
x[5]    = 10
y       = np.linspace(1, 10, 10)
x_pre   = np.zeros(10)

### Error Calculation
rms = RMSE(x, x_pre)
mae = MAE(x, x_pre)

### Ploting
fig, ax = plt.subplots(1, 2, figsize = (8, 5))
fig.suptitle("RMSE and MAE Comparison")

# Plot 
ax[0].plot(x, y, 'ro')
ax[0].axvline(x = rms, color='r', linestyle='-')
ax[1].plot(x, y, 'ro')
ax[1].axvline(x = mae, color='g', linestyle='-')

# Plot Name
ax[0].set_xlabel('error')
ax[1].set_xlabel('error')


ax[0].set_title('RMSE', fontsize=10)
ax[1].set_title('MAE', fontsize=10)
plt.setp(ax, xlim=(0, 12))

plt.show()
