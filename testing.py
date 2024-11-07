import csv
from survivability import updateDRI, calculateDRI, read_IMU

groundLevel = 120.00 # AGL ground level
X = 0.0 #Spinal Displacement
X_dot = 0.0 #Spinal Velocity
X_max = 0.0 #Maximum Spinal Compression (used for final DRI calculation)
dt = 0.01

with open('2024-10-05 Xcopter Data2.csv', 'r') as file:
    in_data = csv.reader(file, delimiter=',')

    next(in_data) # skip header

    for row in in_data:
        z_ddot = read_IMU(row)

        if (float(row[0]) > 250): # temp way to isolate descent
            X_max = updateDRI(z_ddot, X_dot, X_max, X, dt)
            DRI_Val = calculateDRI(X_max)

        if (abs(z_ddot) > 110 and float(row[12]) < groundLevel): # landing detection conditional statement
            print(f"Final DRI Value was {DRI_Val}")
            # publish final DRI value to RF transmission node