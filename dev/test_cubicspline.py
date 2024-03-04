import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Generate sample data
x = np.array([1, 2, 3, 4, 5])
y = np.array([1, 4, 9, 16, 25])

# Create CubicSpline interpolation object
cs = CubicSpline(x, y)

# Define new coordinates for extrapolation
x_new = np.linspace(0, 6, 100)
y_new = np.linspace(0, 30, 100)

# Perform extrapolation
z_new = cs(x_new)

# Plot original data
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='blue', label='Original Data')

# Plot extrapolation
plt.plot(x_new, z_new, color='red', label='Extrapolation')

# Add legend and labels
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')

# Show plot
plt.title('Cubic Spline Extrapolation')
plt.show()

