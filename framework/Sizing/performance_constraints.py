"""
File name : Performance constraints
Author    : Alejandro Rios
Email     : aarc.88@gmail.com
Date      : September/2020
Last edit : September/2020
Language  : Python 3.8 or >
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This module calculate the regulated takeoff and landing weight according to
    sizing restrictions
Inputs:
    - Vehicle dictionaty
Outputs:
    - Regulated takeoff weight [kg]
    - Regulated landing weight [kg]
TODO's:
    -Add sigma effect of engine

"""
# =============================================================================
# IMPORTS
# =============================================================================
from framework.Performance.Analysis.balanced_field_length import balanced_field_length
from framework.Performance.Analysis.landing_field_length import landing_field_length
from framework.Performance.Analysis.second_segment_climb import second_segment_climb
from framework.Performance.Analysis.missed_approach_climb import missed_approach_climb_AEO, missed_approach_climb_OEI
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation
from framework.Performance.Analysis.cruise_performance import cruise_performance
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================
global GRAVITY
GRAVITY = 9.80665
lb_to_kg = 0.453592


def takeoff_field_length_check(vehicle, weight_takeoff):

    aircraft = vehicle['aircraft']
    airport_departure = vehicle['airport_departure']

    takeoff_field_length_required = airport_departure['takeoff_field_length']
    # weight_takeoff = aircraft['maximum_takeoff_weight']

    flag = 0
    while flag == 0:

        takeoff_field_length_computed = balanced_field_length(
            vehicle, weight_takeoff)

        if takeoff_field_length_computed > takeoff_field_length_required:
            weight_takeoff = weight_takeoff - (10*GRAVITY)
        else:
            flag = 1
    return weight_takeoff


def second_segment_climb_check(vehicle, weight_takeoff):

    aircraft = vehicle['aircraft']
    engine = vehicle['engine']
    # weight_takeoff = aircraft['maximum_takeoff_weight']
    thrust_takeoff = engine['maximum_thrust']

    flag = 0
    while flag == 0:
        thrust_to_weight_takeoff_required = second_segment_climb(
            vehicle, weight_takeoff)
        thrust_to_weight_takeoff = thrust_takeoff/weight_takeoff

        if thrust_to_weight_takeoff < thrust_to_weight_takeoff_required:
            weight_takeoff = weight_takeoff-(10*GRAVITY)
        else:
            flag = 2
    return weight_takeoff


def landing_field_length_check(vehicle, maximum_takeoff_weight, weight_landing):

    aircraft = vehicle['aircraft']
    wing = vehicle['wing']
    airport_destination = vehicle['airport_destination']

    landing_field_length_required = airport_destination['landing_field_length']
    wing_surface = wing['area']

    flag = 0
    while flag == 0:
        # aircraft['maximum_landing_weight'] = weight_landing
        landing_field_length_computed = landing_field_length(
            vehicle, weight_landing)

        maximum_takeoff_mass = maximum_takeoff_weight/GRAVITY
        maximum_landing_mass = weight_landing/GRAVITY

        maximum_takeoff_mass_to_wing_surface_requirement = (
            (maximum_landing_mass/wing_surface)/(maximum_landing_mass/maximum_takeoff_mass))
        maximum_takeoff_mass_to_wing_surface = maximum_landing_mass/wing_surface

        if (landing_field_length_computed > landing_field_length_required or maximum_takeoff_mass_to_wing_surface > maximum_takeoff_mass_to_wing_surface_requirement):
            weight_landing = weight_landing-(10*GRAVITY)
        else:
            flag = 2

    return weight_landing


def landing_climb_check(vehicle, maximum_takeoff_weight, weight_landing):

    aircraft = vehicle['aircraft']
    engine = vehicle['engine']

    thrust_landing = engine['maximum_thrust'] * 0.98

    flag = 0
    while flag == 0:
        thrust_to_weight_landing_required = missed_approach_climb_AEO(
            vehicle, maximum_takeoff_weight, weight_landing)
        thrust_to_weight_landing = thrust_landing/weight_landing

        if thrust_to_weight_landing < thrust_to_weight_landing_required:
            weight_landing = weight_landing-(10*GRAVITY)
        else:
            flag = 2
    return weight_landing


def missed_approach_climb_check(vehicle, maximum_takeoff_weight, weight_landing):

    aircraft = vehicle['aircraft']
    engine = vehicle['engine']

    thrust_landing = engine['maximum_thrust'] * 0.98

    flag = 0
    while flag == 0:
        thrust_to_weight_landing_required = missed_approach_climb_OEI(
            vehicle, maximum_takeoff_weight, weight_landing)
        thrust_to_weight_landing = thrust_landing/weight_landing

        if thrust_to_weight_landing < thrust_to_weight_landing_required:
            weight_landing = weight_landing-(10*GRAVITY)

        else:
            flag = 2
    return weight_landing


def residual_rate_of_climb_check():

    return


def maximum_cruise_speed_check():

    return


def drag_divergence_check():

    return


def regulated_takeoff_weight(vehicle):

    aircraft = vehicle['aircraft']
    airport_departure = vehicle['airport_departure']

    weight_takeoff = aircraft['maximum_takeoff_weight']*GRAVITY

    takeoff_field_length_weight = takeoff_field_length_check(
        vehicle, weight_takeoff)

    second_segment_climb_weight = second_segment_climb_check(
        vehicle, weight_takeoff)

    maximum_takeoff_weight = min(
        takeoff_field_length_weight, second_segment_climb_weight)
    return maximum_takeoff_weight/GRAVITY  # [Kg]


def regulated_landing_weight(vehicle):

    aircraft = vehicle['aircraft']
    weight_landing = aircraft['maximum_landing_weight']*GRAVITY

    maximum_takeoff_weight = aircraft['maximum_takeoff_weight']*GRAVITY

    landing_field_length_weight = landing_field_length_check(
        vehicle, maximum_takeoff_weight, weight_landing)

    landing_climb = landing_climb_check(
        vehicle, maximum_takeoff_weight, weight_landing)

    missed_approach = missed_approach_climb_check(
        vehicle, maximum_takeoff_weight, weight_landing)

    maximum_landing_weight = min(
        landing_field_length_weight, landing_climb, missed_approach)
    return maximum_landing_weight/GRAVITY  # [Kg]
# =============================================================================
# MAIN
# =============================================================================


# =============================================================================
# TEST
# =============================================================================


# aircraft = vehicle['aircraft']
# weight_takeoff = aircraft['maximum_takeoff_weight']
# takeoff_field_length_weight = takeoff_field_length_check(vehicle, weight_takeoff)
# print('weight BFL requirement:', takeoff_field_length_weight/GRAVITY)

# # print(takeoff_field_length_weight/GRAVITY)
# second_segment_climb_weight =  second_segment_climb_check(vehicle, weight_takeoff)
# print('weight second segment requirement:', second_segment_climb_weight/GRAVITY)

# maximum_takeoff_weight = min(takeoff_field_length_weight, second_segment_climb_weight)
# print('========================================================================================')
# print('MTOW [kg]:', maximum_takeoff_weight/GRAVITY)
# print('========================================================================================')

# aircraft = vehicle['aircraft']
# weight_landing = aircraft['maximum_landing_weight']
# landing_field_length_weight = landing_field_length_check(vehicle, maximum_takeoff_weight, weight_landing)
# print('weight landing field requirement:', landing_field_length_weight/GRAVITY)

# landing_climb = landing_climb_check(vehicle, maximum_takeoff_weight, weight_landing)
# print('weight landing climb:', landing_climb/GRAVITY)


# missed_approach = missed_approach_climb_check(vehicle, maximum_takeoff_weight, weight_landing)
# print('weight missed approach:', missed_approach/GRAVITY)

# maximum_landing_weight = min(landing_field_length_weight, landing_climb, missed_approach)
# print('========================================================================================')
# print('MLW [kg]:', maximum_landing_weight/GRAVITY)
# print('========================================================================================')
