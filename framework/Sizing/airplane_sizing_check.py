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
from framework.Sizing.Geometry.wing_structural_layout_fuel_storage import wing_structural_layout
from framework.Sizing.Geometry.fuselage_sizing import fuselage_cross_section
from framework.Sizing.Geometry.wetted_area import wetted_area
from framework.Aerodynamics.aerodynamic_coefficients_ANN import aerodynamic_coefficients_ANN
from framework.Performance.Mission.mission_01 import mission
from framework.Performance.Engine.engine_performance import turbofan
from framework.Sizing.Geometry.sizing_landing_gear import sizing_landing_gear
from framework.Sizing.performance_constraints import *

# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================
global GRAVITY, m2_to_ft2, lb_to_kg, friction_coefficient
GRAVITY = 9.80665
m2_to_ft2 = 10.7639
lb_to_kg = 0.453592
friction_coefficient = 0.003


def airplane_sizing(x, vehicle):

    # Load nested dictionary vehicle
    aircraft = vehicle['aircraft']
    wing = vehicle['wing']
    winglet = vehicle['winglet']
    horizontal_tail = vehicle['horizontal_tail']
    vertical_tail = vehicle['vertical_tail']
    fuselage = vehicle['fuselage']
    engine = vehicle['engine']
    pylon = vehicle['pylon']
    nose_landing_gear = vehicle['nose_langing_gear']
    main_landing_gear = vehicle['main_langing_gear']
    performance = vehicle['performance']
    operations = vehicle['operations']
    airport_departure = vehicle['airport_departure']
    airport_destination = vehicle['airport_destination']

    # Upload dictionary variables with optimization variables input vector x
    wing['area'] = x[0]
    wing['aspect_ratio'] = x[1]
    wing['taper_ratio'] = x[2]
    wing['sweep_c_4'] = x[3]
    wing['twist'] = x[4]
    wing['semi_span_kink'] = x[5]
    aircraft['passenger_capacity'] = x[11]
    fuselage['seat_abreast_number'] = x[12]
    performance['range'] = x[13]
    aircraft['winglet_presence'] = x[17]
    aircraft['slat_presence'] = x[18]
    horizontal_tail['position'] = x[19]

    engine['bypass'] = x[6]
    engine['fan_diameter'] = x[7]
    engine['compressor_pressure_ratio'] = x[8]
    engine['turbine_inlet_temperature'] = x[9]
    engine['fan_pressure_ratio'] = x[10]
    engine['design_point_pressure'] = x[14]
    engine['design_point_mach'] = x[15]
    engine['position'] = x[16]

    # Aerodynamics
    Cl_max = 1.9
    wing['tip_incidence'] = wing['root_incidence'] + wing['twist']

    # Operations
    aircraft['payload_weight'] = aircraft['passenger_capacity']*operations['passenger_mass']  # [kg]
    proceed = 0

    # Airframe parameters
    wing['trunnion_xposition'] = 0.75
    wing['span'] = np.sqrt(
        wing['aspect_ratio']*wing['area'])
    CL_max = 0.9*Cl_max*np.cos(wing['sweep_c_4']*np.pi/180)
    CL_max_clean = CL_max

    # Engine paramters
    if engine['position'] == 0:
        aircraft['number_of_engines'] = 2
        engines_under_wing = 0
    elif engine['position'] == 1:
        aircraft['number_of_engines'] = 2
        engines_under_wing = 2

    if wing['position'] == 2 or engine['position'] == 2:
        horizontal_tail['position'] == 2

    classification = 0
    for i in range(1,fuselage['pax_transitions']-1):
        track = aircraft['passenger_capacity'] - \
            fuselage['transition_points'][i-1]
        if track < 0:
            classification = i
            break

    if classification == 0:
        classification = fuselage['pax_transitions']

    if classification == 1:
        fuselage['container_type'] = 'None'
    elif classification == 2:
        fuselage['container_type'] = 'LD3-45W'
    elif classification == 3:
        fuselage['container_type'] = 'LD3-45'

    vehicle = fuselage_cross_section(vehicle)

    # wetted area calculation

    wing['mean_thickness'] = np.mean(wing['thickness_ratio'])

    (vehicle,
        xutip,
        yutip,
        xltip,
        yltip,
        xukink,
        yukink,
        xlkink,
        ylkink,
        xuroot,
        yuroot,
        xlroot,
        ylroot) = wetted_area(vehicle)

    (vehicle) = wing_structural_layout(
        vehicle,
        xutip,
        yutip,
        yltip,
        xukink,
        xlkink,
        yukink,
        ylkink,
        xuroot,
        xlroot,
        yuroot,
        ylroot)

    # Estimation of MTOW [kg] by Class I methodology
    aircraft_wetted_area_ft2 = aircraft['wetted_area'] * m2_to_ft2
    aux1 = (np.log10(aircraft_wetted_area_ft2) - 0.0199)/0.7531
    wt0_initial = 10**aux1  # [kg]
    aircraft['maximum_takeoff_weight'] = wt0_initial*lb_to_kg  # [kg]
    fuselage['diameter'] = np.sqrt(fuselage['width']*fuselage['height'])
    wing['leading_edge_xposition'] = 0.45*fuselage['length']
    fuselage['cabine_length'] = fuselage['length'] - \
        (fuselage['tail_length']+fuselage['cockpit_length'])

    engine['diameter'] = engine['fan_diameter']*1.1
    # engine['maximum_thrust'] = 0.3264*aircraft['maximum_takeoff_weight']+ 2134.8
    engine['maximum_thrust'], _= turbofan(
        0, 0, 1, vehicle)

    engine_static_trhust = engine['maximum_thrust']*0.95

    # Calculo deo CD0 da asa e do fator k do arrasto induzido
    CL_1 = 0.4
    # Input for neural network: 0 for CL | 1 for alpha
    switch_neural_network = 0
    alpha_deg = 0
    h = 100
    mach = 0.15
    CD_1, _ = aerodynamic_coefficients_ANN(
        vehicle, h, mach, CL_1, alpha_deg, switch_neural_network)

    CL_2 = 0.5
    CD_2, _ = aerodynamic_coefficients_ANN(
        vehicle, h, mach, CL_2, alpha_deg, switch_neural_network)

    K_coefficient = (CD_1 - CD_2)/(CL_1**2 - CL_2**2)
    wing_CD0 = CD_1 - K_coefficient*(CL_1**2)

    h = 0
    CL = 0.45
    # CLalpha derivative estimation
    switch_neural_network = 1
    alpha_deg_1 = 1
    _, CL_out_1 = aerodynamic_coefficients_ANN(
        vehicle, h, mach, CL, alpha_deg_1, switch_neural_network)

    alpha_deg_2 = 2
    _, CL_out_2 = aerodynamic_coefficients_ANN(
        vehicle, h, mach, CL, alpha_deg_2, switch_neural_network)

    CL_alpha_deg = (CL_out_2 - CL_out_1)/(alpha_deg_2 - alpha_deg_1)
    CL_alpha_rad = CL_alpha_deg/(np.pi/180)

    # Divergence mach check
    mach = 0.7
    CL_1 = 0.4
    alga_deg = 1
    CD_max = -1000
    CD_min = 1000

    while mach <= operations['mach_maximum_operating']:
        mach = mach + 0.01
        switch_neural_network = 0
        CD_wing, _ = aerodynamic_coefficients_ANN(
            vehicle,h, mach, CL_1, alpha_deg, switch_neural_network)
        CD_ubrige = friction_coefficient * \
            (aircraft['wetted_area'] - wing['wetted_area']) / \
            wing['area']
        CD_total = CD_wing + CD_ubrige
        CD_max = max(CD_max, CD_total)
        CD_min = min(CD_min, CD_total)

    delta_CD = CD_max - CD_min

    if aircraft['slat_presence'] == 1:
        aircraft['CL_maximum_takeoff'] = CL_max_clean + 0.6
        aircraft['CL_maximum_landing'] = CL_max_clean + 1.2
    else:
        aircraft['CL_maximum_takeoff'] = CL_max_clean + 0.4
        aircraft['CL_maximum_landing'] = CL_max_clean + 1.0

    nose_landing_gear['xpostion'] = fuselage['cockpit_length'] - 0.4
    MTOW_count = 0
    delta_MTOW = 1E6
    max_MTOW_count = 25
    status = 0

    MTOW = aircraft['maximum_takeoff_weight']

    while (delta_MTOW > 100) and (MTOW_count < max_MTOW_count):


        vehicle, MTOW_calculated, fuel_mass,landing_weight = mission(vehicle)
        delta_MTOW = np.abs(MTOW_calculated - aircraft['maximum_takeoff_weight'])
        aircraft['maximum_takeoff_weight'] = 0.20*aircraft['maximum_takeoff_weight'] + 0.8*MTOW_calculated  # This calculation was performed inside mission function. Is that correct?
        wing['fuel_capacity'] = fuel_mass
        engine['maximum_thrust'] = (0.3264*aircraft['maximum_takeoff_weight'] + 2134.8)*0.95
        MTOW_count = MTOW_count + 1

    if MTOW_count > max_MTOW_count:
        print('MTOW calculation not converged')
        flag_requirements = 1
        DOC = 100
        delta_fuel = -10000
        takeoff_noise = 400
        status = 1
    else:
        
        aircraft['zCG'] = -0.80
        vehicle = sizing_landing_gear(vehicle)
        # fuel deficit 
        delta_fuel = wing['fuel_capacity'] - 1.005*fuel_mass
    
        if delta_fuel < 0:
            flag_fuel = 1
        else:
            flag_fuel = 0

    # Design envelope check

    maximum_takeoff_weight = aircraft['maximum_takeoff_weight']
    maximum_landing_weight = landing_weight

    engine['maximum_thrust'] = (aircraft['number_of_engines']*engine['maximum_thrust']*lb_to_kg)*GRAVITY
    regulated_takeoff_weight_required = regulated_takeoff_weight(vehicle)
    regulated_landing_weight_required = regulated_landing_weight(vehicle)
    # thrust_to_weight_ratio = (aircraft['number_of_engines']*engine['maximum_thrust']*lb_to_kg)/maximum_takeoff_weight
    # takeoff_to_weight_second_segment_required = second_segment_climb(vehicle, maximum_takeoff_weight*GRAVITY)

    if (maximum_takeoff_weight*10*GRAVITY) > regulated_takeoff_weight_required:
        flag_takeoff = 1
    else:
        flag_takeoff = 0
    
    if (maximum_landing_weight*10*GRAVITY) > regulated_landing_weight_required:
        flag_landing = 1
    else: 
        flag_landing = 0


    flags = [flag_takeoff, flag_landing, flag_fuel]

    if max(flags) > 0:
        status = 1
    else:
        status = 0

    return status, vehicle
# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================


# x = [100, 12, 0.38, 22.6, -2.5, 0.34, 5.0, 1.36, 28.5,
#      1450, 1.46, 78, 2, 1600, 33000, 0.82, 1, 0, 1, 1]

# x = [85, 8.3, 0.32, 21.9, -3.1, 0.35, 5.5, 1.35, 26.2,
#      1444, 1.46, 100, 6, 1600, 41000, 0.78, 1, 1, 1, 1]


# status = airplane_sizing(x, vehicle)
