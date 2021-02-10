"""
Function  :main.py
Title     : main function
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
from framework.Performance.Mission.mission import mission
from framework.Network.network_optimization import network_optimization
from framework.Economics.revenue import revenue
from framework.Sizing.airplane_sizing_check import airplane_sizing
from framework.baseline_aircraft_parameters import *
import pandas as pd
import pickle
import numpy as np
from datetime import datetime
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================

# =============================================================================
# MAIN
# =============================================================================
def network_profit(x,vehicle):
    
    status, vehicle = airplane_sizing(x,vehicle)

    performance = vehicle['performance']

    if status == 0:

        print('Aircraft OK')

        market_share = 0.1

        df1 = pd.read_csv('Database/distance.csv')
        df1 = (df1.T)
        distances = df1.to_dict()
        df2 = pd.read_csv('Database/demand.csv')
        df2 = round(market_share*(df2.T))
        demand = df2.to_dict()
        pax_capacity = x[11]

        departures = ['CD1', 'CD2', 'CD3', 'CD4',
                    'CD5', 'CD6', 'CD7', 'CD8', 'CD9', 'CD10']
        arrivals = ['CD1', 'CD2', 'CD3', 'CD4',
                    'CD5', 'CD6', 'CD7', 'CD8', 'CD9', 'CD10']

        pax_number = 78
        load_factor = pax_number/pax_capacity
        revenue_ik = {}
        for i in departures:
            for k in arrivals:
                if i != k:
                    # revenue_ik[(i, k)] = revenue(distances[i][k], load_factor, pax_capacity, pax_number)
                    revenue_ik[(i, k)] = revenue(
                        demand[i][k], distances[i][k], pax_capacity, pax_number)
                else:
                    revenue_ik[(i, k)] = 0

        # print(revenue_ik)

        DOC_ik = {}

        for i in departures:
            for k in arrivals:
                if i != k:
                    performance['range'] = (distances[i][k]) * distances[i][k]
                    DOC_ik[(i, k)] = float(mission(vehicle))
                    print(DOC_ik[(i, k)])
                else:
                    DOC_ik[(i, k)] = 0

        profit = network_optimization(distances, demand, DOC_ik)
    else:
        profit = 0

    return float(profit)

# =============================================================================
# TEST
# =============================================================================
# global NN_induced, NN_wave, NN_cd0, NN_CL, num_Alejandro
# num_Alejandro = 100000000000000000000000
# global NN_induced, NN_wave, NN_cd0, NN_CL

# x = [72, 8, 0.25, 15, -2, 0.30, 4, 1, 27, 1405, 1.6, 50, 4, 1600, 41000, 0.78, 1, 1, 1, 1]

# result = network_profit(x,vehicle)
# print(result)