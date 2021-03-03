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
def ground_proximity_effect (Velocity_mixed,sound_ambient,theta_m,engine_height,Diameter_mixed,frequency):

    # Ground proximity is applied only for the mixed jet component
    GPROX_m = (5*Velocity_mixed/sound_ambient)*np.exp(-(9*(theta_m/np.pi)-6.75)**2- \
        ((engine_height/Diameter_mixed)-2.5)**2)*(1+(np.sin((np.pi*engine_height*frequency/sound_ambient)-np.pi/2))**2)/ \
        (2+np.abs((engine_height*frequency/sound_ambient)-1))

    return GPROX_m
# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
