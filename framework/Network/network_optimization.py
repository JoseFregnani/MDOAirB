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
from collections import defaultdict
import numpy as np
from pulp import *
import pandas as pd

from framework.Economics.revenue import revenue
from framework.baseline_aircraft import baseline_aircraft
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================


def network_optimization(distances, demand, DOC):
    # Definition of cities to be considered as departure_airport, first stop, final airport
    departure_airport = ['CD1', 'CD2', 'CD3', 'CD4',
                         'CD5', 'CD6', 'CD7', 'CD8', 'CD9', 'CD10']
    first_stop_airport = ['CD1', 'CD2', 'CD3', 'CD4',
                          'CD5', 'CD6', 'CD7', 'CD8', 'CD9', 'CD10']
    final_airport = ['CD1', 'CD2', 'CD3', 'CD4',
                     'CD5', 'CD6', 'CD7', 'CD8', 'CD9', 'CD10']

    # Define minimization problem
    problem = LpProblem("Network", LpMaximize)

    # print(distances)
    # print(DOC)
    doc = DOC

    # doc = {}
    # for i in departure_airport:
    #     for k in first_stop_airport:
    #         if i != k:
    #             doc[(i, k)] = np.round(doc0[i][k])
    #         else:
    #             doc[(i, k)] = np.round(doc0[i][k])
    aircraft_data = baseline_aircraft()

    # print(doc)
    pax_number = aircraft_data['passenger_capacity']
    pax_capacity = pax_number

    revenue_ik = defaultdict(dict)
    for i in departure_airport:
        for k in first_stop_airport:
            if i != k:
                revenue_ik[(i, k)] = round(
                    revenue(demand[i][k], distances[i][k], pax_capacity, pax_number))
            else:
                revenue_ik[(i, k)] = 0

    planes = {'P1': {'w': pax_number}}
    # =============================================================================
    # Decision variables definition
    # =============================================================================
    # Number of airplanes of a given type flying (i, k):
    nika = LpVariable.dicts('nika', [(i, k) for i in departure_airport
                                     for k in first_stop_airport],
                            0, None, LpInteger)

    # Number of passengers transported from route (i, j, k)
    xijk = LpVariable.dicts('numPac',
                            [(i, j, k) for i in departure_airport
                             for j in final_airport
                             for k in first_stop_airport],
                            0, None, LpInteger)

    # Route capacity:
    '''
    Capacidade da rota (i, k) definida pela somatória de numero de aviões do tipo P fazendo a rota (i, k) vezes a capacidade do avião P
    '''
    G = {}
    for i in departure_airport:
        for k in first_stop_airport:
            G[(i, k)] = nika[(i, k)]*planes['P1']['w']

    # =============================================================================
    # Objective function
    # =============================================================================

    problem += lpSum(revenue_ik) - lpSum(nika[(i, k)]*2*doc[(i, k)]
                                         for i in departure_airport for k in first_stop_airport if i != k)

    # problem += lpSum(revenue) - lpSum(nika[(i, k)]*doc[(i, k)] for i in departure_airport for k in first_stop_airport if i != k)
    # =============================================================================
    # Constraints
    # =============================================================================
    # Demand constraint
    for i in departure_airport:
        for j in final_airport:
            for k in first_stop_airport:
                if i != j:
                    problem += lpSum(xijk[(i, j, k)]
                                     for k in first_stop_airport) == demand[i][j]

    # Capacity constraint
    for i in departure_airport:
        for j in final_airport:
            for k in first_stop_airport:
                if i != k:
                    problem += lpSum(xijk[(i, j, k)]
                                     for j in final_airport) <= G[(i, k)]

    # Capacity constraint
    for i in departure_airport:
        for j in final_airport:
            for k in first_stop_airport:
                if k != j:
                    problem += lpSum(xijk[(i, j, k)]
                                     for i in departure_airport) <= G[(j, k)]

    # =============================================================================
    # Solve problem
    # =============================================================================

    problem.solve(GLPK(msg=0, timeLimit=60*5))

    # print('Status:', LpStatus[problem.status])
    # Print solution to CONTINUOUS
    pax = []
    for v in problem.variables():
        # print(v.name, "=", v.varValue)
        pax.append(v.varValue)

    # print(sum(pax))
    df4 = pd.DataFrame(pax)
    df4.to_csv('PAX.csv')
    # Print optimal
    # print('Total profit [$US]:', value(problem.objective))

    profit = value(problem.objective)
    return profit
# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
