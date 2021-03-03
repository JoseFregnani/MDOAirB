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
def external_plug_effect(Velocity_primary,Velocity_secondary, Velocity_mixed, Diameter_primary,
                         Diameter_secondary,Diameter_mixed, Plug_diameter, sound_ambient, theta_p,theta_s,theta_m):

    # Primary jet
    PG_p = 0.1*(Velocity_primary/sound_ambient)*(10-(18*theta_p/np.pi))*Plug_diameter/Diameter_primary
    
    # Secondary jet
    PG_s = 0.1*(Velocity_secondary/sound_ambient)*(6-(18*theta_s/np.pi))*Plug_diameter/Diameter_secondary
    
    # Mixed jet
    PG_m = 0.1*(Velocity_primary*Velocity_mixed/(sound_ambient**2))*(9-(18*theta_m/np.pi))*Plug_diameter/Diameter_mixed
    
    # Pack Results 
    jet_plug_effects = Data()
    jet_plug_effects.PG_p = PG_p
    jet_plug_effects.PG_s = PG_s
    jet_plug_effects.PG_m = PG_m 

    return jet_plug_effects

# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
