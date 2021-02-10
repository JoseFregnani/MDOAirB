"""
Function  :low_pressure_turbine_parameters.py
Title     :
Written by:
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
from framework.Attributes.Atmosphere.temperature_dependent_air_properties import FAIR
from framework.Performance.Engine.mass_flow_parameter import MASSFP
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================


def TURB(Tti, f, AidAe, Mi, Me, eta_ti, TteR):
    # Inputs: Tti, f, (Ai /Ae), Mi, Me, eta_t, TteR
    # Outputs: pi_t, Tau_t, Tte

    _, hti, Prti, phiti, cpti, Rti, gammati, ati = FAIR(item=1, f=f, T=Tti)
    Ti, _, MFPi = MASSFP(Tt=Tti, f=f, M=Mi)
    T_te = TteR
    while True:  # Label 1
        Te, Pe, MFPe = MASSFP(Tt=T_te, f=f, M=Me)
        _, hte, Prte, phite, cpte, Rte, gammate, ate = FAIR(
            item=1, f=f, T=T_te)

        # T, h, Pr, phi, Cp, R, gamma, a

        pi_t = (MFPi/MFPe)*AidAe*np.sqrt(T_te/Tti)
        Prtei = pi_t*Prti
        Ttei, htei, _, phitei, cptei, Rtei, gammatei, atei = FAIR(
            item=3, f=f, Pr=Prtei)
        hte = hti - eta_ti*(hti - htei)
        Tau_t = (hte/hti)
        Tten, _, Prte, phite, cpte, Rte, gammate, ate = FAIR(
            item=2, f=f, h=hte)
        Tte_error = np.abs(T_te - Tten)
        if Tte_error > 0.01:
            T_te = Tten
            continue  # Go to 1
        else:
            break
    return pi_t, Tau_t, T_te
# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
# print(TURB(1.0404e3, 0.0189, 0.4365, 1, 1, 0.8525, 984.0251))
