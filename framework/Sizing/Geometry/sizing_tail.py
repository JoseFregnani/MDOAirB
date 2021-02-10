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
import numpy as np

from framework.Sizing.Geometry.sizing_vertical_tail import sizing_vertical_tail
from framework.Sizing.Geometry.sizing_horizontal_tail import sizing_horizontal_tail
from framework.Weights.center_of_gravity_position import center_of_gravity
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================
global deg_to_rad
deg_to_rad = np.pi/180

def sizing_tail(vehicle, mach, altitude):

    # np.save('vehicle_test.npy', vehicle) 
    wing = vehicle['wing']
    aircraft = vehicle['aircraft']
    horizontal_tail = vehicle['horizontal_tail']
    vertical_tail = vehicle['vertical_tail']
    fuselage = vehicle['fuselage']
    relaxation = 0.7
    kink_distance = (wing['span']/2)*wing['semi_span_kink'] 

    horizontal_tail['aerodynamic_center_ref'] = 0.25
    vertical_tail['aerodynamic_center_ref'] = 0.25
    

    # Calc of cg here
    vehicle = center_of_gravity(vehicle)

    delta_horizontal_tail = 10000
    delta_vertical_tail = 10000
    margin = aircraft['static_margin']*wing['mean_aerodynamic_chord']
    # aircraft['after_center_of_gravity_xposition'] = 15.29

    while (delta_horizontal_tail > 0.025) or (delta_vertical_tail > 0.025):
        airfoil_aerodynamic_center_reference = 0.25

        aircraft['neutral_point_xposition'] = wing['leading_edge_xposition'] + wing['mean_aerodynamic_chord_yposition']  * \
            np.tan(wing['sweep_leading_edge']*deg_to_rad) + \
            airfoil_aerodynamic_center_reference*wing['mean_aerodynamic_chord'] 
        # print('x_le: ',wing['leading_edge_xposition'] )
        # print('xneutral point: ',aircraft['neutral_point_xposition'] )
        distance_xnp_xcg = aircraft['neutral_point_xposition'] - aircraft['after_center_of_gravity_xposition']
        # print('xcg: ',aircraft['after_center_of_gravity_xposition'])
        # print('distance xnp xcg:',distance_xnp_xcg )
        delta_distance = distance_xnp_xcg - margin
        wing_leading_edge_xposition_new = wing['leading_edge_xposition'] - delta_distance
        wing['leading_edge_xposition'] = wing_leading_edge_xposition_new

        # Iteration cycle for vertical tail
        vertical_tail['aerodynamic_center_xposition'] = 0.95*fuselage['length'] - vertical_tail['center_chord'] + vertical_tail['mean_aerodynamic_chord_yposition'] * \
            np.tan(vertical_tail['sweep_leading_edge']*deg_to_rad) + \
            vertical_tail['aerodynamic_center_ref']*vertical_tail['mean_aerodynamic_chord']

        
        # print('ac_xpos',vertical_tail['aerodynamic_center_xposition'])
        # print('xcg_aft',aircraft['after_center_of_gravity_xposition'])
        distance_vtxac_xcg = vertical_tail['aerodynamic_center_xposition'] - \
            aircraft['after_center_of_gravity_xposition']
        
        # print('lv',distance_vtxac_xcg)


        vertical_tail_area_new = (
            wing['area']*vertical_tail['volume']*wing['span'])/distance_vtxac_xcg

        # print('VVH:',vertical_tail['volume'])

        # print('vt_area_new:',vertical_tail_area_new)

        delta_vertical_tail = np.abs(
            vertical_tail['area'] - vertical_tail_area_new)

        # print('delta ht:', delta_vertical_tail)

        # print('vt_area_new:',vertical_tail_area_new)

        vertical_tail['area'] = relaxation*vertical_tail_area_new + \
            (1-relaxation)*vertical_tail['area']
        # print('vt_area',vertical_tail['area'])

        vehicle = sizing_vertical_tail(
            vehicle,
            mach+0.05,
            altitude)

        # Iteration cycle for horizontal tail
        if horizontal_tail['position']  == 1:
            horizontal_tail['aerodynamic_center_xposition'] = 0.95*fuselage['length'] - horizontal_tail['center_chord'] + horizontal_tail['mean_aerodynamic_chord_yposition'] * \
                np.tan(horizontal_tail['sweep_leading_edge']*deg_to_rad) + \
                horizontal_tail['aerodynamic_center_ref'] * \
                horizontal_tail['mean_aerodynamic_chord']
        else:
            horizontal_tail['aerodynamic_center_xposition'] = 0.95*fuselage['length'] - vertical_tail['center_chord'] + vertical_tail['span'] * \
                np.tan(vertical_tail['sweep_leading_edge']*deg_to_rad) + \
                horizontal_tail['aerodynamic_center_ref'] * \
                horizontal_tail['mean_aerodynamic_chord'] + horizontal_tail['mean_aerodynamic_chord_yposition'] * \
                np.tan(horizontal_tail['sweep_leading_edge']*deg_to_rad)

        distance_htxac_xcg = horizontal_tail['aerodynamic_center_xposition'] - \
            aircraft['after_center_of_gravity_xposition']

        horizontal_tail_area_new = (
            horizontal_tail['volume']*wing['area']*wing['mean_aerodynamic_chord'])/distance_htxac_xcg

        delta_horizontal_tail = np.abs(
            horizontal_tail['area'] - horizontal_tail_area_new)
        # print('delta ht:', delta_horizontal_tail)

        horizontal_tail['area'] = relaxation*horizontal_tail_area_new + \
            (1-relaxation)*horizontal_tail['area']

        vehicle = sizing_horizontal_tail(vehicle, mach, altitude)
        
        vehicle = center_of_gravity(vehicle)
        

    return vehicle

# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
# vehicle = np.load('vehicle_test.npy',allow_pickle='TRUE').item()
# # print(vehicle['wing']) # displays "world"
# aircraft = vehicle['aircraft']
# horizontal_tail = vehicle['horizontal_tail']
# vertical_tail = vehicle['vertical_tail']
# engine = vehicle['engine']
# fuselage = vehicle['fuselage']
# # print(aircraft)
# # print('---------------------------------------------------------')
# mach = 0.8
# altitude = 41000
# vehicle = sizing_tail(vehicle, mach, altitude)
# aircraft = vehicle['aircraft']
# horizontal_tail = vehicle['horizontal_tail']
# vertical_tail = vehicle['vertical_tail']

# print(vertical_tail)