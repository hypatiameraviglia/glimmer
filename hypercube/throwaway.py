import numpy as np
import csv

# Example data
temp = np.array([100, 110, 120])
wavel = np.array([1.0, 1.1, 1.2])
data = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]])

# Transpose the data to match the required format
data_transposed = data.T

# Write to CSV
with open('throwaway.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row (temperatures)
    header = ['Wavelength'] + temp.tolist()
    writer.writerow(header)

    # Write the data rows (wavelengths and corresponding data)
    for i, w in enumerate(wavel):
        row = [w] + data_transposed[i].tolist()
        writer.writerow(row)

print("Data written to interpolated_data.csv successfully.")

