# =============================================================================
# IMPORTS
# =============================================================================
import logging
import logging.config
import concurrent.futures
import copy
from datetime import datetime
import pandas as pd
from framework.Performance.Mission.mission import mission
from framework.Sizing.airplane_sizing_check import airplane_sizing

logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)

# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================

# FUNCTIONS
# =============================================================================
def process_mission(args):
    start_time = datetime.now()
    DOC = 0
    if args[1][0] != 0:
        DOC = int(mission(*args[1]))*args[1][0]
    log.info(f'==== End DOC calculation ====: {args[0]} | {DOC} | {datetime.now() - start_time}')
    return args[0], DOC

def process_data(departures, arrivals, distances, data_airports, vehicle_base, distance_max):
    for i in departures:
        for k in arrivals:
            distance = 0
            if (i != k) and (distances[i][k] <= distance_max):
                vehicle_base['airport_departure']['elevation'] = \
                    data_airports.loc[data_airports['APT2'] == i, 'ELEV'].iloc[0]
                vehicle_base['airport_destination']['elevation'] = \
                    data_airports.loc[data_airports['APT2'] == k, 'ELEV'].iloc[0]
                vehicle_base['airport_departure']['takeoff_field_length'] = \
                    data_airports.loc[data_airports['APT2'] == i, 'TORA'].iloc[0]
                vehicle_base['airport_destination']['takeoff_field_length'] = \
                    data_airports.loc[data_airports['APT2'] == k, 'TORA'].iloc[0]
                distance = distances[i][k]
            yield (i,k), (distance,copy.deepcopy(vehicle_base))

def objective_function(variables, vehicle_base):
    log.info('==== Start network profit module ====')
    start_time = datetime.now()
    log_time = start_time

    status, vehicle_base = airplane_sizing(variables, vehicle_base)
    log.info(f'==== End airplane sizing ====: {datetime.now() - log_time}')
    log_time = datetime.now()

    data_airports = pd.read_csv("Database/Airports/airports.csv")
    log.info(f'==== End read airports ====: {datetime.now() - log_time}')
    log_time = datetime.now()

    if status == 0:
        log.info(f'Aircraft passed sizing and checks status: {status}')

        distances_db = pd.read_csv('Database/Distance/distance.csv')
        distances_db = (distances_db.T)
        distances = distances_db.to_dict()  # Convert to dictionaty
        log.info(f'==== End read distances ====: {datetime.now() - log_time}')
        log_time = datetime.now()

        departures = ['CD1', 'CD2', 'CD3', 'CD4']
        arrivals = ['CD1', 'CD2', 'CD3', 'CD4']

        # =============================================================================
        log.info('---- Start DOC calculation ----')

        DOC_ik_results2 = {}
        with concurrent.futures.ProcessPoolExecutor() as executor:
            DOC_results = executor.map(
                process_mission,
                process_data(
                    departures, arrivals, distances,
                    data_airports, vehicle_base, variables[13]
                )
            )
            for (i,k),DOC_result in DOC_results:
                if i not in DOC_ik_results2:
                    DOC_ik_results2[i] = {}
                DOC_ik_results2[i][k] = DOC_result

        log.info(f'==== End DOC calculation 2 ====: {datetime.now() - log_time}')
        log_time = datetime.now()

        profit = 0

        log.info(f'Aircraft DOC matrix Result2: {DOC_ik_results2}')
    else:
        profit = 0
        log.info(f'Aircraft did not pass sizing and checks, profit: {profit}')

    log.info(f'Network profit excecution time: {datetime.now() - start_time}')
    log.info('==== End network profit module ====')

    return float(profit)



# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
from framework.Database.Aircrafts.baseline_aircraft_parameters import vehicle

if __name__ == '__main__':
    x = [100, 99, 40, 23, -4, 36, 59, 13, 27, 1385, 17, 90, 5, 2446, 41000, 78, 1, 1, 1, 1]

    result = objective_function(x, vehicle)
    print(result)
