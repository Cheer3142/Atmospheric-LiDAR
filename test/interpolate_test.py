import numpy as np
from scipy.interpolate import interp2d

# Given 2D data
x = np.array([1, 2, 3, 4])
y = np.array([1, 2])
z = np.array([[1, 2, 3, 4],
              [5, 6, 7, 8]])

# Create interpolation function
f = interp2d(x, y, z, kind='linear')

# Define new points for interpolation
x_new = np.linspace(1, 4, 7)  # 7 points between 1 and 4
y_new = np.linspace(1, 4, 7)  # 7 points between 1 and 4

# Perform interpolation
z_new = f(x_new, y_new)

print("Interpolated values:")
for row in z_new:
    print(row)
