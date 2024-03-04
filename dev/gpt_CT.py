import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import CloughTocher2DInterpolator

# Generate sample data
x = np.array([0, 1, 2, 3, 4])
y = np.array([0, 1, 2, 3, 4])
z = np.array([[0, 0, 0, 0, 0],
              [0, 1, 4, 9, 16],
              [0, 4, 16, 36, 64],
              [0, 9, 36, 81, 144],
              [0, 16, 64, 144, 256]])

# Reshape z to match the shape of x and y
z_flat = z.flatten()
x_flat, y_flat = np.meshgrid(x, y)
x_flat = x_flat.flatten()
y_flat = y_flat.flatten()

# Create CloughTocher2DInterpolator object
interp = CloughTocher2DInterpolator(points=[x_flat, y_flat], values=z_flat)

# Define new coordinates for extrapolation
x_new = np.linspace(0, 8, 100)
y_new = np.linspace(0, 8, 100)

# Perform extrapolation
X_new, Y_new = np.meshgrid(x_new, y_new)
Z_new = interp((X_new.flatten(), Y_new.flatten())).reshape(X_new.shape)

# Plot 2D wire mesh
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_wireframe(X_new, Y_new, Z_new, color='red')

# Add original data points
ax.scatter(x, y, z, color='blue')

# Label axes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.title('Clough-Tocher 2D Interpolation')
plt.show()

