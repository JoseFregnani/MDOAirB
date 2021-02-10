"""
Function  : pax_cabine_length.py
Title     : Pax cabine length
Written by: Alejandro Rios
Date      : October/2019
Last edit : August/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This module calculates the pax cabine length

Future implementations:
    - 

Inputs:
    - Number of pax
    - Seating abreast number
    - Seat pitch
    - Aisle width
    - Seat width

Outputs:
    - Length fuselage
"""
########################################################################################
"""Importing Modules"""
########################################################################################
########################################################################################
"""Function definition"""
########################################################################################




import numpy as np
import os
def pax_cabine_length(vehicle):
    aircraft = vehicle['aircraft']
    fuselage = vehicle['fuselage']
    # Calcula variacao de CG devido aos passageiros
    # clear
    # clc
    # Definicoes
    # figure(7)
    GalleyProf = 1.1
    ToilletProf = 1.5
    # fuselage['aisle_width']  = 0.50  # [m]
    #fuselage['seat_width']   = 0.45
    SeatProf = 0.48  # [m]
    # fuselage['seat_pitch']   = 0.8128 # [m]
    #
    #fuselage['seat_abreast_number'] =5
    #aircraft['passenger_capacity'] =78
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
    # fill(x,y,'y')
    # hold on
    # **** Desenha Galley
    x0G = x0T + 1. + ToilletProf  # walking area with 1 m large
    LenFus = x0G
    # x[1)=x0G
    # y(1)=0
    # x(2)=x(1)+GalleyProf
    # y(2)=y(1)
    # x(3)=x(2)
    # y(3)=fuselage['seat_abreast_number']*fuselage['seat_width']+fuselage['aisle_width']
    # x(4)=x(1)
    # y(4)=y(3)
    # fill(x,y,'b')
    # hold on
    # # **** Desenha PaxCAB
    # x(1)=0
    # y(1)=0
    # x(2)=x(1)+ LenFus
    # y(2)=y(1)
    # x(3)=x(2)
    # y(3)=fuselage['seat_abreast_number']*fuselage['seat_width'] + fuselage['aisle_width']
    # x(4)=x(1)
    # y(4)=y(3)
    # plot(x,y,'k')
    # hold on
    # fprintf('\n Length of passenger cabin is #5.2f m \n',LenFus)
    # close(figure(7))
    # clear x y Naux1 Naux2
    # end # cgpax
    # #-------------------------------------------------------------------------
    return(LenFus)


def seattop_fileira(x0, fuselage, SeatProf):
    # descobre se fuselage['seat_abreast_number'] � par ou �mpar
    Naux1 = round(fuselage['seat_abreast_number']/2)
    Naux2 = fuselage['seat_abreast_number']/2 - Naux1
    if Naux2 > 0:  # numero impar de fileiras
        #fprintf('\n fuselage['seat_abreast_number'] � impar \n')
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
        # fprintf('\n fuselage['seat_abreast_number'] � par \n')
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

        y0 = (fuselage['seat_abreast_number']/2)*fuselage['seat_width'] + fuselage['aisle_width']
        for i in range(1, int(fuselage['seat_abreast_number']/2)):
            x.append(x0)

            y.append(y0 + (i-1)*fuselage['seat_width'])
            x.append(x[0]+SeatProf)
            y.append(y[0])
            x.append(x[1])
            y.append(y[1]+fuselage['seat_width'])
            x.append(x[0])
            y.append(y[2])
