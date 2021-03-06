"""
Function  :
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
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================


def skew(n):
    n = np.squeeze(n)
    n_tilde = np.array([[0, -n[2], n[1]],
                        [n[2], 0, -n[0]],
                        [-n[1], n[0], 0]])
    return n_tilde
# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
# n = np.array([0, -0.0013, 0.1230])
# print(skew(n))
