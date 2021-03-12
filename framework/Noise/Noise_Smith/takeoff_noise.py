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

# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================
def takeoff_noise(time_vec,velocity_vec,distance_vec,velocity_horizontal_vec,altitude_vec,velocity_vertical_vec,trajectory_angle_vec,fan_rotation_vec,compressor_rotation_vec, throttle_position, takeoff_parameters,noise_parameters,aircraft_geometry,engine_parameters,vehicle):

    XA = noise_parameters['takeoff_longitudinal_distance_mic']
    dlat = noise_parameters['takeoff_lateral_distance_mic'] 
    for i in range(1,len(time_vec)):
        H1 = altitude_vec[i]
        XB = distance_vec[i]
        gamma = trajectory_angle_vec[i]
        L1 = np.abs(XB-XA)
        R = np.sqrt(H1**2 + L1**2 + dlat**2)
        termo1 = np.sqrt(((H1 - L1*np.tan(np.abs(gamma*deg_to_rad)))**2 + dlat**2)/(R**2))
        if XB > XA:
            theta = np.arcsin(termo1)/deg_to_rad
        elif XB == XA:
            theta = 90
        else:
            theta = 180-(np.arcsin(termo1)/deg_to_rad)
        
        vairp = velocity_vec[i]
        N1 = fan_rotation_vec[i]
        N2 = compressor_rotation_vec[i]

        fi = np.arctan(H1/dlat)/deg_to_rad
        if vairp == 0:
            vairp = 0.1
        
        FPhase = 1
        if H1 >= 100
            aircraft_geometry['main_landing_gear_position'] = 2
            aircraft_geometry['main_landing_gear_position'] = 2
        else:
            aircraft_geometry['main_landing_gear_position'] = 1
            aircraft_geometry['main_landing_gear_position'] = 1

        saidatemp = noise_airframe(time_vec,velocity_vec,distance_vec,velocity_horizontal_vec,altitude_vec,velocity_vertical_vec,trajectory_angle_vec,fan_rotation_vec,compressor_rotation_vec, throttle_position, takeoff_parameters,noise_parameters,aircraft_geometry,engine_parameters,vehicle, Fphase)     


    return frequencies, SPL, time
# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
