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
import sys
import pickle
import numpy as np
import csv
from datetime import datetime

from framework.utilities.logger import get_logger
from framework.utilities.output import write_optimal_results, write_kml_results, write_bad_results, write_newtork_results
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
    try:
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
            departures = ['CD1', 'CD2', 'CD3', 'CD4',
                            'CD5', 'CD6', 'CD7', 'CD8', 'CD9', 'CD10']
            arrivals = ['CD1', 'CD2', 'CD3', 'CD4',
                        'CD5', 'CD6', 'CD7', 'CD8', 'CD9', 'CD10']

            # departures = ['CD1', 'CD2', 'CD3', 'CD4']
            # arrivals = ['CD1', 'CD2', 'CD3', 'CD4']

            # =============================================================================
            log.info('---- Start DOC calculation ----')
            # The DOC is estimated for each city pair and stored in the DOC dictionary
            city_matrix_size = len(departures)*len(arrivals)
            DOC_ik = {}
            fuel_mass = {}
            total_mission_flight_time = {}
            mach = {}
            passenger_capacity = {}

            for i in range(len(departures)):
                DOC_ik[departures[i]] = {}
                fuel_mass[departures[i]] = {}
                total_mission_flight_time[departures[i]] = {}
                mach[departures[i]] = {}
                passenger_capacity[departures[i]] = {}

                for k in range(len(arrivals)):
                    if (i != k) and (distances[departures[i]][arrivals[k]] <= x[13]):
                        airport_departure['elevation'] = data_airports.loc[data_airports['APT2']
                                                                        == departures[i], 'ELEV'].iloc[0]
                        airport_destination['elevation'] = data_airports.loc[data_airports['APT2']
                                                                            == arrivals[k], 'ELEV'].iloc[0]
                        airport_departure['takeoff_field_length'] = data_airports.loc[data_airports['APT2']
                                                                                    == departures[i], 'TORA'].iloc[0]
                        airport_destination['takeoff_field_length'] = data_airports.loc[data_airports['APT2']
                                                                                        == arrivals[k], 'TORA'].iloc[0]
                        mission_range = distances[departures[i]][arrivals[k]]
                        fuel_mass[departures[i]][arrivals[k]], total_mission_flight_time[departures[i]][arrivals[k]], DOC,mach[departures[i]][arrivals[k]],passenger_capacity[departures[i]][arrivals[k]]  = mission(mission_range,vehicle)

                        DOC_ik[departures[i]][arrivals[k]] = int(DOC*distances[departures[i]][arrivals[k]])                       
                        # print(DOC_ik[(i, k)])
                    else:
                        DOC_ik[departures[i]][arrivals[k]] = 0
                        fuel_mass[departures[i]][arrivals[k]]  = 0
                        total_mission_flight_time[departures[i]][arrivals[k]]  = 0
                        mach[departures[i]][arrivals[k]]  = 0
                        passenger_capacity[departures[i]][arrivals[k]]  = 0

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
            profit, vehicle, kpi_df1, kpi_df2 = network_optimization(
                arrivals, departures, distances, demand, DOC_ik, pax_capacity, vehicle)

            log.info('Network profit [$USD]: {}'.format(profit))
            # =============================================================================

            def flatten_dict(dd, separator ='_', prefix =''):
                return { prefix + separator + k if prefix else k : v
                        for kk, vv in dd.items()
                        for k, v in flatten_dict(vv, separator, kk).items()
                        } if isinstance(dd, dict) else { prefix : dd }

            
            mach_flatt = flatten_dict(mach)
            mach_df =  pd.DataFrame.from_dict(mach_flatt,orient="index",columns=['mach'])
            passenger_capacity_flatt = flatten_dict(passenger_capacity)
            passenger_capacity_df =  pd.DataFrame.from_dict(passenger_capacity_flatt,orient="index",columns=['pax_num'])
            fuel_used_flatt = flatten_dict(fuel_mass)
            fuel_used_df =  pd.DataFrame.from_dict(fuel_used_flatt,orient="index",columns=['fuel'])
            mission_time_flatt = flatten_dict(total_mission_flight_time)
            mission_time_df =  pd.DataFrame.from_dict(mission_time_flatt,orient="index",columns=['time'])

            kpi_df2['mach'] = mach_df['mach'].values
            kpi_df2['pax_num'] = passenger_capacity_df['pax_num'].values
            kpi_df2['fuel'] = fuel_used_df['fuel'].values
            kpi_df2['time'] = mission_time_df['time'].values

            # Number of active nodes
            kpi_df2['active_arcs'] = np.where(kpi_df2["aircraft_number"] > 0, 1, 0)

            # Number of aircraft
            kpi_df2['aircraft_number'] = kpi_df2['aircraft_number'].fillna(0)
            
            # Average cruise mach
            kpi_df2['mach_tot_aircraft'] = kpi_df2['aircraft_number']*kpi_df2['mach']

            # Total fuel
            kpi_df2['total_fuel'] = kpi_df2['aircraft_number']*kpi_df2['fuel']

            # Total distance
            kpi_df2['total_distance'] = kpi_df2['aircraft_number']*kpi_df2['distances']

            # Total pax
            kpi_df2['total_pax'] = kpi_df2['aircraft_number']*kpi_df2['pax_num']

            # Total cost
            kpi_df2['total_cost'] = 2*kpi_df2['aircraft_number']*kpi_df2['doc']


            write_optimal_results(profit, DOC_ik, vehicle, kpi_df2)
            write_kml_results(arrivals, departures, profit, vehicle)
            write_newtork_results(profit,kpi_df1,kpi_df2)

        else:
            profit = 0
            log.info(
                'Aircraft did not pass sizing and checks, profit: {}'.format(profit))

            
    except:

        error = sys.exc_info()[0]

        profit = 0
        log.info('Exception ocurred during calculations')
        log.info('Aircraft not passed sizing and checks, profit: {}'.format(profit))

        write_bad_results(x,error)

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
# global NN_induced, NN_wave, NN_cd0, NN_CL, num_Alejandro
# num_Alejandro = 100000000000000000000000
# global NN_induced, NN_wave, NN_cd0, NN_CL
# from framework.Database.Aircrafts.baseline_aircraft_parameters import *

# # x = [130, 8.204561481970153, 0.3229876327660606, 31, -4, 0.3896951781733875, 4.826332970409506, 1.0650795018081771, 27, 1485, 1.6, 101, 4, 2185, 41000, 0.78, 1, 1, 1, 1]
# # # x = [73, 8.210260198894748, 0.34131954092766925, 28, -5, 0.32042307969643524, 5.000456116634125, 1.337333818504011, 27, 1442, 1.6, 106, 6, 1979, 41000, 0.78, 1, 1, 1, 1]
# # # x = [106, 9.208279852593964, 0.4714790814543369, 16, -3, 0.34987438995033143, 6.420120321538892, 1.7349297171205607, 29, 1461, 1.6, 74, 6, 1079, 41000, 0.78, 1, 1, 1, 1]

# print(result)
# x =[0, 77, 35, 19, -3, 33, 63, 17, 29, 1396, 25, 120, 6, 2280, 41000, 78]

# result = objective_function(x, vehicle)