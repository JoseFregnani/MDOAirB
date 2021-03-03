"""
File name :
Author    : 
Email     : aarc.88@gmail.com
Date      : 
Last edit :
Language  : Python 3.8 or >
Aeronautical Institute of Technology - Airbus Brazil

Description:
    -
Inputs:
    -
Outputs:
    -
TODO's:
    -

"""
# =============================================================================
# IMPORTS
# =============================================================================
import numpy as np
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================
def noise_counterplot(noise_segment,analyses,config):
    
    #unpack
    position_vector = noise_segment.conditions.frames.inertial.position_vector
    mic_position    = analyses.mic_array
    
    #X,Y,Z position of the aircraft
    x_aircraft      = position_vector[:,0]
    altitude        = -position_vector[:,2]
    z_aircraft      = position_vector[:,1]
     
    n_steps = len(altitude)  #number of time steps (space discretization)
    
    # Preparing the matrix: Angles
    phi = np.zeros(n_steps)
    theta = np.zeros(n_steps)   
   
    #X,Y,Z position of each microphone
    x_mic = np.float(mic_position[0])
    y_mic = np.float(mic_position[1])
    z_mic = np.float(mic_position[2])

    dist = np.sqrt((x_aircraft-x_mic)**2+(altitude-y_mic)**2+(z_aircraft-z_mic)**2)
    phi   = np.arctan(np.abs(z_mic)/altitude)

    for i in range (0,n_steps):
        if (x_aircraft[i]-x_mic)< 0.:
            theta[i] = np.arctan(np.abs(altitude[i]/(x_aircraft[i]-x_mic)))
        else:
            theta[i] = np.pi - np.arctan(np.abs(altitude[i]/(x_aircraft[i]-x_mic))) 
                
    # Pack the results
    noise_segment.dist  = dist
    noise_segment.theta = theta
    noise_segment.phi   = phi 

    return noise_segment

# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
