"""
File name : Network profit function
Author    : Alejandro Rios
Email     : aarc.88@gmail.com
Date      : July 2020
Last edit : February 2021
Language  : Python 3.8 or >
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This module calculates the network profit following the following steps:
        - Vehicle sizing and checks (airplane_sizing)
        - Revenue calculation (reveneu)
        - Direct operational cost calculation (mission)
        - Profit calculation (network_optimization)

Inputs:
    - Optimization variables (array x)
    - Mutable dictionary with aircraft, perfomance, operations and airports
    departure and destiny information
Outputs:
    - Profit wich is the objective function
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
import pandas as pd
import pickle
import numpy as np
import csv
from datetime import datetime

from framework.utilities.logger import get_logger
from framework.utilities.output import write_optimal_results, write_kml_results
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================
log = get_logger(__file__.split('.')[0])

def objective_function(x, vehicle):
    
    log.info('==== Start network profit module ====')
    start_time = datetime.now()

    # Try running profit calculation. If error appears during run profit = 0
# try:
    # =============================================================================
    # Airplane sizing and checks
    status, vehicle = airplane_sizing(x, vehicle)

    performance = vehicle['performance']
    airport_departure = vehicle['airport_departure']
    airport_destination = vehicle['airport_destination']
    data_airports = pd.read_csv("Database/Airports/airports.csv")
    # =============================================================================
    # If airplane pass checks, status = 0, else status = 1 and profit = 0
    if status == 0:
        log.info('Aircraft passed sizing and checks status: {}'.format(status))

        market_share = 0.1

        # Load origin-destination distance matrix [nm]
        distances_db = pd.read_csv('Database/Distance/distance.csv')
        distances_db = (distances_db.T)
        distances = distances_db.to_dict()  # Convert to dictionaty

        # Load daily demand matrix and multiply by market share (10%)
        demand_db = pd.read_csv('Database//Demand/demand.csv')
        demand_db = round(market_share*(demand_db.T))
        demand = demand_db.to_dict()

        pax_capacity = x[11]  # Passenger capacity

        # Airports:
        # ["FRA", "LHR", "CDG", "AMS",
        #          "MAD", "BCN", "FCO","DUB","VIE","ZRH"]
        departures = ['CD1', 'CD2', 'CD3', 'CD4']
        arrivals = ['CD1', 'CD2', 'CD3', 'CD4']

        # =============================================================================
        log.info('---- Start DOC calculation ----')
        # The DOC is estimated for each city pair and stored in the DOC dictionary
        city_matrix_size = len(departures)*len(arrivals)
        DOC_ik = {}
        for i in departures:
            DOC_ik[i] = {}
            for k in arrivals:
                if (i != k) and (distances[i][k] <= x[13]):
                    airport_departure['elevation'] = data_airports.loc[data_airports['APT2']
                                                                    == i, 'ELEV'].iloc[0]
                    airport_destination['elevation'] = data_airports.loc[data_airports['APT2']
                                                                        == k, 'ELEV'].iloc[0]
                    airport_departure['takeoff_field_length'] = data_airports.loc[data_airports['APT2']
                                                                                == i, 'TORA'].iloc[0]
                    airport_destination['takeoff_field_length'] = data_airports.loc[data_airports['APT2']
                                                                                    == k, 'TORA'].iloc[0]
                    mission_range = distances[i][k]
                    DOC_ik[i][k]= int(
                        mission(mission_range,vehicle))*distances[i][k]
                    
                    # print(DOC_ik[(i, k)])
                else:
                    DOC_ik[i][k] = 0

                city_matrix_size = city_matrix_size - 1
                print('INFO >>>> city pairs remaining to finish DOC matrix fill: ',city_matrix_size)

        # np.save('Database/DOC/DOC.npy',DOC_ik)

        with open('Database/DOC/DOC.csv', 'w') as f:
            for key in DOC_ik.keys():
                f.write("%s,%s\n"%(key,DOC_ik[key]))

        log.info('Aircraft DOC matrix: {}'.format(DOC_ik))
        # =============================================================================
        log.info('---- Start Network Optimization ----')
        # Network optimization that maximizes the network profit
        profit, vehicle = network_optimization(
            arrivals, departures, distances, demand, DOC_ik, pax_capacity, vehicle)

        log.info('Network profit [$USD]: {}'.format(profit))
        # =============================================================================

        write_optimal_results(profit, DOC_ik, vehicle)
        write_kml_results(arrivals, departures, profit, vehicle)

    else:
        profit = 0
        log.info(
            'Aircraft did not pass sizing and checks, profit: {}'.format(profit))
# except:

#     profit = 0
#     log.info('Exception ocurred during calculations')
#     log.info('Aircraft not passed sizing and checks, profit: {}'.format(profit))

    end_time = datetime.now()
    log.info('Network profit excecution time: {}'.format(end_time - start_time))
    log.info('==== End network profit module ====')

    return float(profit)



# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
from framework.Database.Aircrafts.baseline_aircraft_parameters import *

#   0   1   2   3    4   5   6   7   8    9   10   11  12   13   14  
# x[72, 77, 35, 19, -3, 33, 40, 10, 27, 1410, 16, 120, 6, 2280, 41000, 78, 1, 1, 1, 1]
x =[108, 77, 35, 19, -3, 33, 40, 10, 27, 1410, 16, 120, 6, 2280, 41000, 78, 1, 1, 1, 1]

result = objective_function(x, vehicle)
print(result)
