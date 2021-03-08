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
from framework.Database.Aircrafts.baseline_aircraft_parameters import *
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation
from framework.Performance.Engine.engine_performance import turbofan
from scipy.integrate import ode
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================
global GRAVITY
GRAVITY = 9.81

def air_integration():
    return

def air2_integration():
    return

def thrust_equation_coefficients(V,T):
    A = T[0]
    B = (T[1] - T[0])/(V[1]-V[0])
    C = ((T[2]-T[1])/(V[2]-V[1])-(T[1]-T[0])/(V[1]-V[0]))/(V[2]-V[0])
    T0 = T[0] - B*V[0] + C*V[0]*V[1]
    T1 = B - C*(V[0]+V[1])
    T2 = C
    return T0, T1, T2

def takeoff_profile(takeoff_parameters,landing_parameters,aircraft_parameters,runaway_parameters,engine_parameters):

    aircraft = vehicle['aircraft']
    wing = vehicle['wing']
    _, _, _, _, _, rho_ISA, a = atmosphere_ISA_deviation(0, 0)

    # Initial calculations:
    V_rotation = takeoff_parameters['k1'] * np.sqrt((2*takeoff_parameters['takeoff_weight'])/(rho_ISA*wing['area']*aircraft['CL_maximum_takeoff']))
    V_2 = takeoff_parameters['k2'] * np.sqrt((2*takeoff_parameters['takeoff_weight'])/(rho_ISA*wing['area']*aircraft['CL_maximum_takeoff']))
    V_35 = V_2 + 10/1.9438
    V_vector = np.array([0, (V_2+20)/2, V_2+20])
    mach_vector = V_vector/a

    
    thrust_vector,_ = zip(aircraft['number_of_engines']*turbofan(0, mach_vector(i), 1, vehicle) for i in mach_vector)
    
    T0,T1,T2 = thrust_equation_coefficients(V_vector,thrust_vector)

    # Calculating the All Engines Operative takeoff

    # Runaway run

    # ----- Run until VR -----
    initial_block_distance = 0
    initial_block_velocity = 0
    initial_block_time = 0
    final_velocity = V_rotation
    i2 = 1
    error = 1e-6
    parameters_time_history = np.array([0, 0, 0, 0, 0, 0, 0, engine['RPM_ref_1'], engine['RPM_ref_2']])

    final_distance, final_velocity, final_block_time = takeoff_integration(initial_block_distance, initial_block_velocity, initial_block_time, takeoff_parameters, runaway_parameters, landing_parameters, vehicle, rho_ISA, final_velocity)
    
    # ----- Run until V35 -----
    initial_block_distance = final_distance
    initial_block_velocity = final_velocity
    initial_block_time = final_block_time
    final_velocity = V_35

    final_distance, final_velocity, final_block_time = takeoff_integration(initial_block_distance, initial_block_velocity, initial_block_time, takeoff_parameters, runaway_parameters, landing_parameters, vehicle, rho_ISA, final_velocity)

    # ----- Flare to 35 ft -----
    

    return 


def aircraft_noise(takeoff_parameters, landing_parameters,aircraft_parameters,aircraft_geometry,engine_parameters,runaway_parameters,noise_parameters,vehicle):
    
    # ---- Takeoff noise ----

    # Takeoff flight path:
    _,_,_,_,_ = takeoff_profile(takeoff_parameters,landing_parameters,aircraft_parameters,runaway_parameters,engine_parameters)

    # Noise calculation - EPNdB
    takeoff_noise = takeoff_EPNdB(time_history, throttle_position, takeoff_parameters,noise_parameters,aircraft_geometry,engine_parameters,vehicle)
    sideline_noise,_ = sideline_EPNdB(time_history,throttle_position,takeoff_parameters,noise_parameters,aircraft_geometry,engine_parameters,vehicle)

    # ---- Aproach and landing noise ----

    # Takeoff flight path:
    _ = approach_profile(takeoff_parameters,landing_parameters,aircraft_parameters,vehicle)

    # Noise calculation - EPNdB
    landing_noise = approach_EPNdB(_,landing_parameters,noise_parameters,aircraft_geometry,vehicle)

    return takeoff_noise, sideline_noise, landing_noise

def noise_calculation(vehicle):
    GRAVITY = 9.81

    aircraft = vehicle['aircraft']
    airport_departure = vehicle['airport_departure']
    maximum_takeoff_weight = aircraft['maximum_takeoff_weight']*GRAVITY
    maximum_landing_weight = aircraft['maximum_landing_weight']*GRAVITY

    takeoff_parameters = {}

    takeoff_parameters['takeoff_weight'] = maximum_takeoff_weight  # [N]
    takeoff_parameters['lambda'] = 0
    takeoff_parameters['k1'] = 1.1
    takeoff_parameters['k2'] = 1.2
    takeoff_parameters['time_1'] = 3.0  # [s]
    takeoff_parameters['obstacle_altitude'] = 35  # [ft]
    takeoff_parameters['time_step'] = 0.5  # [s]
    takeoff_parameters['time_2'] = 3.0  # [s]
    takeoff_parameters['trajectory_max_distance'] = 10000  # [m]

    landing_parameters = {}
    landing_parameters['gamma'] = -3
    landing_parameters['CL_3P'] = 0.3
    landing_parameters['CD_3P'] = 0.08
    landing_parameters['mu_roll'] = 0.03
    landing_parameters['mu_brake'] = 0.3
    landing_parameters['transition_time'] = 1.0
    landing_parameters['load_factor_flare'] = 1.1

    aircraft_parameters = {}
    aircraft_parameters['CL_3P'] = 0.3
    aircraft_parameters['CL_air'] = 1.65
    aircraft_parameters['CD_3P'] = 0.08
    aircraft_parameters['CD_air_LG_down'] = 0.111
    aircraft_parameters['CD_air_LG_up'] = 0.081

    aircraft_geometry = {}
    aircraft_geometry['fuselage_surface'] = 21.1
    aircraft_geometry['fuselage_length'] = 22.28
    aircraft_geometry['flap_deflection_TO'] = 10
    aircraft_geometry['flap_deflection_LD'] = 35 
    aircraft_geometry['main_landing_gear_number'] = 2
    aircraft_geometry['nose_landig_gear_number'] = 1

    aircraft_geometry['main_landing_gear_length'] = 1.88 
    aircraft_geometry['nose_landing_gear_length'] = 1.21
    aircraft_geometry['main_landing_gear_wheels'] = 2
    aircraft_geometry['nose_landing_gear_wheels'] = 2
    aircraft_geometry['wing_flap_type1_position'] = 1 
    aircraft_geometry['wing_flap_type2_position'] = 0
    aircraft_geometry['slats_position'] = 1
    aircraft_geometry['slots_number'] = 2
    aircraft_geometry['main_landing_gear_position'] = 1 
    aircraft_geometry['main_landing_gear_position'] = 1
    aircraft_geometry['altitude_retracted'] = 0
    aircraft_geometry['delta_ISA_retracted'] = 0

    engine_parameters = {}
    engine_parameters['throttle_position'] = 1
    engine['RPM_ref_1'] = 4952
    engine['RPM_ref_1'] = 14950

    runaway_parameters = {}
    runaway_parameters['mu_roll'] = 0.03
    runaway_parameterss['mu_brake'] = 0.3

    noise_parameters = {}
    noise_parameters['relative_humidity'] = 70
    noise_parameters['landing_lateral_distance_mic'] = 1
    noise_parameters['sideline_lateral_distance_mic'] = 450
    noise_parameters['takeoff_lateral_distance_mic'] = 1
    noise_parameters['landing_longitudinal_distance_mic'] = 2000
    noise_parameters['sideline_longitudinal_distance_mic'] = 0
    noise_parameters['takeoff_longitudinal_distance_mic'] = 6500

    takeoff_noise, sideline_noise, landing_noise = aircraft_noise(takeoff_parameters, landing_parameters,aircraft_parameters,aircraft_geometry,engine_parameters,runaway_parameters,noise_parameters,vehicle)

    takeoff_noise = 0
    sideline_noise = 0
    landing_noise = 0

    return takeoff_noise, sideline_noise, landing_noise


def takeoff_integration(initial_block_distance, initial_block_velocity, initial_block_time, takeoff_parameters, runaway_parameters, landing_parameters, vehicle, rho_ISA, final_speed):
    t0 = initial_block_time
    z0 = [initial_block_distance, initial_block_velocity]
    solver = ode(ground_integration)
    solver.set_integrator('vode', nsteps=1000)
    solver.set_f_params(takeoff_parameters,runaway_parameters,landing_parameters,rho_ISA,vehicle)
    solver.set_initial_value(z0, t0)

    t0 = 0
    t1 = 50
    # N = 50
    t = np.linspace(t0, t1)
    N = len(t)
    sol = np.empty((N,2))
    sol[0] = z0
    times = np.empty((N, 1))
    # Repeatedly call the `integrate` method to advance the
    # solution to time t[k], and save the solution in sol[k].
    k = 1
    while solver.successful() and solver.y[1] <= final_speed:
        solver.integrate(t[k])
        sol[k] = solver.y
        times[k] = solver.t
        k += 1
    distance = sol[0:k, 0]
    velocity = sol[0:k, 1]
    time = times[0:k]

    
    final_distance = distance[-1]
    final_velocity = velocity[-1] 
    final_block_time = time[-1]

    return final_distance, final_velocity, final_block_time

def ground_integration(time,state,takeoff_parameters,runaway_parameters,landing_parameters,rho_ISA,vehicle):
    wing = vehicle['wing']

    distance = state[0]
    velocity = state[1]

    constant = np.cos(takeoff_parameters['lambda']) + runaway_parameters['mu_roll']*np.sin(takeoff_parameters['lambda'])
    K0 = T0*constant - runaway_parameters['mu_roll']*takeoff_parameters['takeoff_weight']
    K1 = T1*constant
    K2 = T2*constant + 0.5*rho_ISA*wing['area']*(runaway_parameters['mu_roll']*landing_parameters['CL_3P'] - landing_parameters['CD_3P'])
    
    # Cálculo das derivadas
    x_dot = velocity
    V_dot = (GRAVITY/takeoff_parameters['takeoff_weight']) * (K0 + K1*velocity + K2*velocity*velocity)
    

    dout = np.asarray([x_dot, V_dot])
    dout = dout.reshape(2, )
    return dout

def flare_integration(time,state,takeoff_parameters,runaway_parameters,landing_parameters,rho_ISA,vehicle):
    wing = vehicle['wing']

    distance = state[0]
    velocity_horizontal = state[1]
    altitude = state[2]
    velocity_vertical = state[3]
    trajectory_angle = state[4]

    V_resultant = velocity_vertical**2 + velocity_horizontal**2
    gamma = trajectory_angle
    altitude = altitude

    _, _, _, _, _, _, a = atmosphere_ISA_deviation(altitude, 0)

    mach = np.sqrt(V_resultant/a)
    throttle_position = 1.0
    thrust_force, fuel_flow = turbofan(
        altitude, mach, throttle_position, vehicle)  # force [N], fuel flow [kg/hr]
    
    total_thrust_force = thrust_force*aircraft['number_of_engines']*

    drag = 0.5*rho_ISA*V_resultant*wing['area']*landing_parameters['CD_3P']
    lift = 0.5*rho_ISA*V_resultant*wing['area']*landing_parameters['CL_3P']

    velocity_horizontal = np.sqrt(V_resultant)*np.cos(gamma)
    parameter2_dot = GRAVITY/aircraft['maximum_takeoff_weight'] * (total_thrust_force - drag - aircraft['maximum_takeoff_weight']*np.sin(gamma))*np.cos(gamma) - GRAVITY*(1.3 - np.cos(gamma))*np.sin(gamma)
    velocity_vertical = np.sqrt(V_resultant)*np.sin(gamma)
    parameter4_dot = GRAVITY*(1.3-np.cos(gamma))*np.cos(gamma) + (GRAVITY/aircraft['maximum_takeoff_weight'])*(total_thrust_force - drag - aircraft['maximum_takeoff_weight']*np.sin(gamma))*np.sin(gamma)
    gamma_dot = (GRAVITY/np.sqrt(V_resultant))*1.3 - np.cos(gamma)


    dout = np.asarray([velocity_horizontal, parameter2_dot, velocity_vertical,  parameter4_dot, gamma_dot])
    dout = dout.reshape(5, )
    return dout
# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
