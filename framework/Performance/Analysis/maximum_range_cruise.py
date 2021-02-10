"""
File name : Maximum range cruise
Author    : Alejandro Rios
Email     : aarc.88@gmail.com
Date      : November/2020
Last edit : November/2020
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
# from framework.Aerodynamics.aerodynamic_coefficients import zero_fidelity_drag_coefficient
from framework.Aerodynamics.aerodynamic_coefficients_ANN import aerodynamic_coefficients_ANN
from framework.Attributes.Airspeed.airspeed import V_cas_to_V_tas, mach_to_V_tas
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation


import numpy as np
import matplotlib.pyplot as plt
from framework.baseline_aircraft import baseline_aircraft
import operator
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================
# def maximum_range_cruise_speed():
global GRAVITY
GRAVITY = 9.80665


def maximum_range_mach(mass, cruise_altitude, delta_ISA, vehicle):
    knots_to_meters_second = 0.514444
    wing  = vehicle['wing']
    wing_surface = wing['area']

    VMO = 340
    altitude = cruise_altitude

    VMO = V_cas_to_V_tas(VMO-10, altitude, delta_ISA)

    initial_mach = 0.2

    mach = np.linspace(initial_mach, 0.82, 100)

    V_tas = mach_to_V_tas(mach, altitude, delta_ISA)

    _, _, _, _, _, rho_ISA, a = atmosphere_ISA_deviation(altitude, delta_ISA)

    CL_required = (2*mass*GRAVITY) / \
        (rho_ISA*((knots_to_meters_second*V_tas)**2)*wing_surface)

    phase = 'cruise'

    # CD = zero_fidelity_drag_coefficient(aircraft_data, CL_required, phase)

    CD = []
    for i in range(len(CL_required)):
        # Input for neural network: 0 for CL | 1 for alpha
        switch_neural_network = 0
        alpha_deg = 1
        CD_aux, _ = aerodynamic_coefficients_ANN(
            vehicle, altitude, mach[i], float(CL_required[i]),alpha_deg,switch_neural_network)
        CD.append(CD_aux)

    MLD = mach*(CL_required/CD)

    index, value = max(enumerate(MLD), key=operator.itemgetter(1))

    mach_maximum_cruise = mach[index]

    V_maximum = mach_to_V_tas(mach_maximum_cruise, altitude, delta_ISA)

    if V_maximum > VMO:
        V_maximum = VMO
        mach_maximum_cruise = V_maximum/a

    return mach_maximum_cruise
# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
