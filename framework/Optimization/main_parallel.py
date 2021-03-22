"""
File name : Optimization function
Author    : Alejandro Rios
Email     : aarc.88@gmail.com
Date      : Dezember 2020
Last edit : February 2021
Language  : Python 3.8 or >
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This function configurate the genetic algorithm for the aircraft and
    network optimization. 
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
import random
import numpy as np
import os
import subprocess
import linecache

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from bokeh.io import push_notebook, show, output_notebook
from bokeh.layouts import row
from bokeh.plotting import figure
from framework.Optimization.objective_function import objective_function
from framework.Database.Aircrafts.baseline_aircraft_parameters import *

import multiprocessing

# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================
p = figure()

# Declare the kind of optimization (min or max)
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
# Define the individual list
creator.create("Individual", list, fitness=creator.FitnessMax)

IND_SIZE = 16  # Define the number of optimization variables

# Definition of all the atributes (design variables), their type and range
toolbox = base.Toolbox()
toolbox.register("attr_wing_surface", random.randint, 72, 130)  # [0] 
toolbox.register("attr_aspect_ratio", random.randint, 75, 100)  # [1] - real range 7.5 to 10
toolbox.register("attr_taper_ratio", random.randint, 25, 50)  # [2] - real range 0.25 to 0.5
toolbox.register("attr_wing_sweep", random.randint, 15, 35)  # [3]
toolbox.register("attr_twist_angle", random.randint, -5, -2)  # [4]
toolbox.register("attr_kink_position", random.randint, 32, 40)  # [5] - real range 0.32 to 0.4
toolbox.register("attr_engine_bypass_ratio", random.randint, 45, 65)  # [6] - real range 4.5 to 6.5
toolbox.register("attr_engine_fan_diameter", random.randint, 10, 20)  # [7] - real range 1 to 2
toolbox.register("attr_engine_overall_pressure_ratio", random.randint, 27, 30)  # [8]
toolbox.register("attr_engine_inlet_turbine_temperature",
                 random.randint, 1350, 1500)  # [9]
toolbox.register("attr_engine_fan_pressure_ratio", random.randint, 14, 25)  # [10] - real range 1.4 to 2.5
toolbox.register("attr_pax_number", random.randint, 50, 120)  # [11]
toolbox.register("attr_number_of_seat_abreast", random.randint, 4, 6)  # [12]
toolbox.register("attr_aircraft_range", random.randint, 1000, 2500)  # [13]
toolbox.register("attr_engine_design_point_pressure",
                 random.randint, 41000, 41000)  # [14]
toolbox.register("attr_engine_design_point_mach", random.randint, 78, 78)  # [15] - real range 0.78 to 0.78
toolbox.register("attr_engine_position", random.randint, 1, 1)  # [16]
toolbox.register("attr_winglet_presence", random.randint, 1, 1)  # [17]
toolbox.register("attr_slat_presense", random.randint, 1, 1)  # [18]
toolbox.register("attr_horizontal_tail_position", random.randint, 1, 1)  # [19]

toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attr_wing_surface, toolbox.attr_aspect_ratio, toolbox.attr_taper_ratio, toolbox.attr_wing_sweep, toolbox.attr_twist_angle, toolbox.attr_kink_position,
                  toolbox.attr_engine_bypass_ratio, toolbox.attr_engine_fan_diameter, toolbox.attr_engine_overall_pressure_ratio, toolbox.attr_engine_inlet_turbine_temperature,
                  toolbox.attr_engine_fan_pressure_ratio, toolbox.attr_pax_number, toolbox.attr_number_of_seat_abreast, toolbox.attr_aircraft_range, toolbox.attr_engine_design_point_pressure,
                  toolbox.attr_engine_design_point_mach, toolbox.attr_engine_position, toolbox.attr_winglet_presence, toolbox.attr_slat_presense, toolbox.attr_horizontal_tail_position),
                 n=1)



# Genetic algoritgm configuration
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register('mate', tools.cxTwoPoint)
toolbox.register('mutate', tools.mutGaussian, mu = 0, sigma = 0.2, indpb = 0.2)
toolbox.register('select', tools.selTournament, tournsize=2)

# Declaration of the objective function (network profit)


def obj_function(individual):
    # This function takes as inputs the current individual (vector of design variavbles) and
    # a predefined dictionary with pre-stored information of the vehicle (aircraft)
    net_profit = objective_function(individual, vehicle)
    return net_profit,

toolbox.register("evaluate", obj_function)
# toolbox.decorate("evaluate", tools.DeltaPenalty(feaseGeom, [1.0, ]))


if __name__ == '__main__':

    random.seed(5)
    # Process Pool of 4 workers
    pool = multiprocessing.Pool(processes=6)
    toolbox.register("map", pool.map)

    pop = toolbox.population(n=10)
    hof = tools.HallOfFame(2)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    logbooks = list()

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.3, mutpb=0.2, ngen=30, 
                        stats=stats, halloffame=hof)



    pool.close()

    # Save results to txt files
    with open("Database/Results/Optimization/optim_statistics.txt", "w") as file:
        file.write(str(log))

    with open("Database/Results/Optimization/optim_population.txt", "w") as file:
        file.write(str(pop))

    with open("Database/Results/Optimization/optim_hall_of_fame.txt", "w") as file:
        file.write(str(hof))
    

    best = hof.items[0]
    
    print("Best Solution = ", best)
    print("Best Score = ", best.fitness.values[0])


    # print('# =============================================================================######################')
    # print('Score:', best.fitness.values[0])
    # print('# =============================================================================######################')
    # =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================