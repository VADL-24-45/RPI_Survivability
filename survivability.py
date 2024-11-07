# Constants 
omega = 52.90
zeta = 0.224
g = 9.81
threshold = -10.0

# Globals
#X = 0.0 #Spinal Displacement
#X_dot = 0.0 #Spinal Velocity
#X_max = 0.0 #Maximum Spinal Compression (used for final DRI calculation)
debug = True
landedState = False
landingEventConditions = False # Set this to true once landing event begins. 


def read_IMU(in_row):
    z_ddot = float(in_row[6]) - g # vertical accel value in IMU
                                # find a more exception safe method to do this
    return z_ddot

def updateDRI(z_ddot, X_dot, X_max, X, dt):
    # z_ddot: vertical accel val from IMU
    # dt: time interval corresponding to sampling rate

    # filtering non-landing events
    if (z_ddot < threshold):

        X_ddot = z_ddot - (2 * zeta * omega * X_dot) - (pow(omega, 2) * X)

        # Update velocity using Euler's Method
        X_dot += X_ddot * dt
        X += X_dot * dt

        # max displacement updating
        if (abs(X) > X_max):
            X_max = abs(X)
    
    return X_max

# calculate index value based on max displacement
def calculateDRI(X_max):
    return (pow(omega, 2) / g) * X_max

def main():
    dt = 0.01 # time interval (default 0.01 -> 100 Hz sample rate)

    while True:
        z_ddot = read_IMU()

        # implement timer to begin DRI logic

        updateDRI(z_ddot, dt)

        if (landedState):
            dri_val = calculateDRI()
            if debug:
                print(f"DRI Value: {dri_val}")
        
if __name__ == "__main__":
    main()


# NOTE: landingDetected flag should only occur at the end of the landing event
# as such DRI calculations should continually occur until this point, where the 
# value is published to the RF node. 