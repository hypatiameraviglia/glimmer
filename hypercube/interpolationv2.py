# Inspired by inteprolation method described for topo maps of Titan in Lorenz et al. 2013
# Drafted with ChatGPT
# Needs to be revised to accept the data format here but might well work!!!

import numpy as np
from scipy.interpolate import UnivariateSpline

# Example 2D dataset with gaps (NaNs)
T = 10
W = 5
data = np.array([
    [1.0, np.nan, 3.0, 4.0, np.nan],
    [2.0, 2.5, np.nan, 4.5, 5.0],
    [np.nan, 3.0, 3.5, np.nan, 6.0],
    [1.5, np.nan, 3.2, 4.1, np.nan],
    [np.nan, 3.3, 3.7, 4.6, 6.2],
    [2.1, np.nan, 3.9, 4.8, np.nan],
    [np.nan, 3.6, 4.2, np.nan, 6.5],
    [2.3, np.nan, 4.5, 5.0, np.nan],
    [np.nan, 3.9, 4.7, 5.2, 6.8],
    [2.5, np.nan, 4.9, 5.4, np.nan]
])

# Interpolating/extrapolating along the T axis
for w in range(W):
    y = data[:, w]
    x = np.arange(T)
    mask = ~np.isnan(y)
    if np.sum(mask) > 1:
        spline = UnivariateSpline(x[mask], y[mask], s=0, ext=0)
        y_interp = spline(x)
        data[:, w][~mask] = y_interp[~mask]  # Only fill in gaps

# Interpolating/extrapolating along the W axis
for t in range(T):
    y = data[t, :]
    x = np.arange(W)
    mask = ~np.isnan(y)
    if np.sum(mask) > 1:
        spline = UnivariateSpline(x[mask], y[mask], s=0, ext=0)
        y_interp = spline(x)
        data[t, :][~mask] = y_interp[~mask]  # Only fill in gaps

print("Interpolated/Extrapolated Data:")
print(data)

