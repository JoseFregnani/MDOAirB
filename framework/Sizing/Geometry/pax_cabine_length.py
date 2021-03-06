"""
File name : Pax cabine length
Written by: Alejandro Rios
Author    : Alejandro Rios
Email     : aarc.88@gmail.com
Date      : Octobe 2019
Last edit : February 2021
Language  : Python 3.8 or >
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This module calculates the pax cabine length

Inputs:
    - Vehicle dictionary

Outputs:
    - pax cabine lenght [m]

TODO's:
    - Clean code
    - Rename variables

"""
# =============================================================================
# IMPORTS
# =============================================================================
import numpy as np
import os
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================


def pax_cabine_length(vehicle):
    aircraft = vehicle['aircraft']
    fuselage = vehicle['fuselage']

    GalleyProf = 1.1
    ToilletProf = 1.5
    SeatProf = 0.48  # [m]

    # ---------------------------------- BEGIN -------------------------
    DeltaSeats = fuselage['seat_pitch'] - SeatProf
    N1 = round(aircraft['passenger_capacity']/fuselage['seat_abreast_number'])
    N2 = aircraft['passenger_capacity']/fuselage['seat_abreast_number'] - N1
    Nrow = N1
    if N2 > 0:
        Nrow = N1+1

    x0 = 1.7  # entrance area
    for j in range(Nrow):
        seattop_fileira(x0, fuselage, SeatProf)
        x0 = x0+SeatProf+DeltaSeats
    # **** Desenha Toillet
    # Descobre lado de maior largura
    Naux1 = round(fuselage['seat_abreast_number']/2)
    Naux2 = fuselage['seat_abreast_number']/2 - Naux1
    if Naux2 > 0:
        fuselage['seat_abreast_number'] = Naux1 + 1
    else:
        fuselage['seat_abreast_number'] = Naux1

    x0T = x0 - DeltaSeats + 0.1
    #LenFus = x0T
    x = []
    y = []
    x.append(x0T)
    y.append(Naux1*fuselage['seat_width'] + fuselage['aisle_width'])
    x.append(x[0] + ToilletProf)
    y.append(y[0])
    x.append(x[1])
    y.append(y[1] + fuselage['seat_abreast_number']*fuselage['seat_width'])
    x.append(x[0])
    y.append(y[2])

    x0G = x0T + 1. + ToilletProf  # walking area with 1 m large
    LenFus = x0G

    return(LenFus)


def seattop_fileira(x0, fuselage, SeatProf):

    Naux1 = round(fuselage['seat_abreast_number']/2)
    Naux2 = fuselage['seat_abreast_number']/2 - Naux1
    if Naux2 > 0:  # numero impar de fileiras
        y0 = 0
        x = []
        y = []
        for i in range(1, Naux1):
            x.append(x0)
            y.append(y0 + (i-1)*fuselage['seat_width'])
            x.append(x[0]+SeatProf)
            y.append(y[0])
            x.append(x[1])
            y.append(y[1]+fuselage['seat_width'])
            x.append(x[0])
            y.append(y[2])
            # fill(x,y,'r')
            # hold on

        y0 = Naux1*fuselage['seat_width'] + fuselage['aisle_width']
        for i in range(1, (fuselage['seat_abreast_number']-Naux1)):
            x.append(x0)
            y.append(y0 + (i-1)*fuselage['seat_width'])
            x.append(x[0]+SeatProf)
            y.append(y[0])
            x.append(x[1])
            y.append(y[1]+fuselage['seat_width'])
            x.append(x[0])
            y.append(y[2])
            # fill(x,y,'r')
            # hold on
    else:  # numero par de fileiras
        # fprintf('\n fuselage['seat_abreast_number'] ??? par \n')
        x = []
        y = []
        y0 = 0
        for i in range(1, int(fuselage['seat_abreast_number']/2)):
            x.append(x0)
            y.append(y0 + (i-1)*fuselage['seat_width'])
            x.append(x[0]+SeatProf)
            y.append(y[0])
            x.append(x[1])
            y.append(y[1]+fuselage['seat_width'])
            x.append(x[0])
            y.append(y[2])
            # fill(x,y,'r')
            # hold on

        y0 = (fuselage['seat_abreast_number']/2) * \
            fuselage['seat_width'] + fuselage['aisle_width']
        for i in range(1, int(fuselage['seat_abreast_number']/2)):
            x.append(x0)

            y.append(y0 + (i-1)*fuselage['seat_width'])
            x.append(x[0]+SeatProf)
            y.append(y[0])
            x.append(x[1])
            y.append(y[1]+fuselage['seat_width'])
            x.append(x[0])
            y.append(y[2])

    return

# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
