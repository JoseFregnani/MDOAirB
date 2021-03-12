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
from framework.Attributes.Airspeed.airspeed import V_cas_to_mach, mach_to_V_cas, crossover_altitude
from framework.Performance.Analysis.climb_to_altitude import rate_of_climb_calculation

import math
from scipy.integrate import ode
import matplotlib.pyplot as plt
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================
global GRAVITY
GRAVITY = 9.81
kt_to_ms = 0.514444
deg_to_rad = np.pi/180
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

def takeoff_profile(takeoff_parameters,landing_parameters,aircraft_parameters,runaway_parameters,engine_parameters,vehicle):

    aircraft = vehicle['aircraft']
    wing = vehicle['wing']
    engine = vehicle['engine']
    _, _, _, _, _, rho_ISA, a = atmosphere_ISA_deviation(0, 0)

    # Initial calculations:
    V_rotation = takeoff_parameters['k1'] * np.sqrt((2*takeoff_parameters['takeoff_weight'])/(rho_ISA*wing['area']*aircraft['CL_maximum_takeoff']))
    V_2 = takeoff_parameters['k2'] * np.sqrt((2*takeoff_parameters['takeoff_weight'])/(rho_ISA*wing['area']*aircraft['CL_maximum_takeoff']))
    V_35 = V_2 + 10/1.9438
    V_vector = np.array([0, (V_2+20)/2, V_2+20])
    mach_vector = V_vector/(a*kt_to_ms)

    
    # thrust_vector,_ = zip(aircraft['number_of_engines']*turbofan(0, mach_vector[i], 1, vehicle) for i in mach_vector)
    thrust_vector = []
    for i in mach_vector:
        thrust,_ , vehicle= turbofan(0, i, 1, vehicle)
        thrust = aircraft['number_of_engines']*thrust
        thrust_vector.append(thrust)
    
    T0,T1,T2 = thrust_equation_coefficients(V_vector,thrust_vector)

    engine['T0'] = T0
    engine['T1'] = T1
    engine['T2'] = T2

    # Calculating the All Engines Operative takeoff

    time_vector = []
    altitude_vector = []

    # Runaway run

    # ----- Run until VR -----
    initial_block_altitude = 0 
    initial_block_distance = 0
    initial_block_trajectory_angle = 0
    initial_block_time = 0
    initial_block_velocity = 0
    initial_block_horizontal_velocity = 0
    initial_block_vertical_velocity = 0
    initial_fan_rotation = engine['fan_rotation']
    initial_compressor_rotation = engine['compressor_rotation']

    stop_criteria = V_rotation
    i2 = 1
    error = 1e-6


    phase = 'ground'
    (final_block_altitude,
    final_block_distance,
    final_block_trajectory_angle,
    final_block_time,
    final_block_velocity,
    final_block_horizontal_velocity,
    final_block_vertical_velocity,
    final_fan_rotation,
    final_compressor_rotation,
    time_vec1,
    velocity_vec1,
    distance_vec1,
    velocity_horizontal_vec1,
    altitude_vec1,
    velocity_vertical_vec1,
    trajectory_angle_vec1,
    fan_rotation_vec1,
    compressor_rotation_vec1) = takeoff_integration(
        initial_block_altitude,
        initial_block_distance,
        initial_block_trajectory_angle,
        initial_block_time,
        initial_block_velocity,
        initial_block_horizontal_velocity,
        initial_block_vertical_velocity,
        initial_fan_rotation,
        initial_compressor_rotation,
        aircraft_parameters,
        takeoff_parameters,
        runaway_parameters,
        landing_parameters,
        vehicle,
        rho_ISA,
        stop_criteria,
        phase
        )

    # time_vec = time_vec.tolist()

    # time_vector.append(time_vec)
    # altitude_vector.append(altitude_vec)


    
    # ----- Run until V35 -----
    initial_block_altitude = 0 
    initial_block_distance = final_block_distance
    initial_block_trajectory_angle = 0
    initial_block_time = final_block_time
    initial_block_velocity = final_block_velocity
    initial_block_horizontal_velocity = 0
    initial_block_vertical_velocity = 0
    initial_fan_rotation = engine['fan_rotation']
    initial_compressor_rotation = engine['compressor_rotation']
    
    stop_criteria = V_35


    phase = 'ground'

    (final_block_altitude,
    final_block_distance,
    final_block_trajectory_angle,
    final_block_time,
    final_block_velocity,
    final_block_horizontal_velocity,
    final_block_vertical_velocity,
    final_fan_rotation,
    final_compressor_rotation,
    time_vec2,
    velocity_vec2,
    distance_vec2,
    velocity_horizontal_vec2,
    altitude_vec2,
    velocity_vertical_vec2,
    trajectory_angle_vec2,
    fan_rotation_vec2,
    compressor_rotation_vec2) = takeoff_integration(
        initial_block_altitude,
        initial_block_distance,
        initial_block_trajectory_angle,
        initial_block_time,
        initial_block_velocity,
        initial_block_horizontal_velocity,
        initial_block_vertical_velocity,
        initial_fan_rotation,
        initial_compressor_rotation,
        aircraft_parameters,
        takeoff_parameters,
        runaway_parameters,
        landing_parameters,
        vehicle,
        rho_ISA,
        stop_criteria,
        phase
        )


    # ----- Flare to 35 ft -----
    
    initial_block_altitude = 0 
    initial_block_distance = final_block_distance
    initial_block_trajectory_angle = 0
    initial_block_time = final_block_time
    initial_block_velocity = final_block_velocity
    initial_block_horizontal_velocity = 0
    initial_block_vertical_velocity = 0
    initial_fan_rotation = engine['fan_rotation']
    initial_compressor_rotation = engine['compressor_rotation']

    stop_criteria = 35

    phase = 'flare'

    (final_block_altitude,
    final_block_distance,
    final_block_trajectory_angle,
    final_block_time,
    final_block_velocity,
    final_block_horizontal_velocity,
    final_block_vertical_velocity,
    final_fan_rotation,
    final_compressor_rotation,
    time_vec3,
    velocity_vec3,
    distance_vec3,
    velocity_horizontal_vec3,
    altitude_vec3,
    velocity_vertical_vec3,
    trajectory_angle_vec3,
    fan_rotation_vec3,
    compressor_rotation_vec3) = takeoff_integration(
        initial_block_altitude,
        initial_block_distance,
        initial_block_trajectory_angle,
        initial_block_time,
        initial_block_velocity,
        initial_block_horizontal_velocity,
        initial_block_vertical_velocity,
        initial_fan_rotation,
        initial_compressor_rotation,
        aircraft_parameters,
        takeoff_parameters,
        runaway_parameters,
        landing_parameters,
        vehicle,
        rho_ISA,
        stop_criteria,
        phase
        )


    # ----- Flare to 2000 ft -----
    
    initial_block_altitude = final_block_altitude 
    initial_block_distance = final_block_distance
    initial_block_trajectory_angle = final_block_trajectory_angle
    initial_block_time = final_block_time
    initial_block_velocity = final_block_velocity
    initial_block_horizontal_velocity = final_block_horizontal_velocity
    initial_block_vertical_velocity = final_block_vertical_velocity
    initial_fan_rotation =final_fan_rotation
    initial_compressor_rotation = final_compressor_rotation

    stop_criteria = 2000

    phase = 'climb'

    (final_block_altitude,
    final_block_distance,
    final_block_trajectory_angle,
    final_block_time,
    final_block_velocity,
    final_block_horizontal_velocity,
    final_block_vertical_velocity,
    final_fan_rotation,
    final_compressor_rotation,
    time_vec4,
    velocity_vec4,
    distance_vec4,
    velocity_horizontal_vec4,
    altitude_vec4,
    velocity_vertical_vec4,
    trajectory_angle_vec4,
    fan_rotation_vec4,
    compressor_rotation_vec4) = takeoff_integration(
        initial_block_altitude,
        initial_block_distance,
        initial_block_trajectory_angle,
        initial_block_time,
        initial_block_velocity,
        initial_block_horizontal_velocity,
        initial_block_vertical_velocity,
        initial_fan_rotation,
        initial_compressor_rotation,
        aircraft_parameters,
        takeoff_parameters,
        runaway_parameters,
        landing_parameters,
        vehicle,
        rho_ISA,
        stop_criteria,
        phase
        )

    # time_vec1.reshape(-1)
    # time_vec2.reshape(-1)
    # time_vec3.reshape(-1)
    # time_vec4 = np.asarray(time_vec4)
    # time_vec4 

    time_vec = np.concatenate((time_vec1,time_vec2,time_vec3,time_vec4),axis=0)
    velocity_vec = np.concatenate((velocity_vec1,velocity_vec2,velocity_vec3,velocity_vec4),axis=0)
    distance_vec = np.concatenate((distance_vec1,distance_vec2,distance_vec3,distance_vec4),axis=0)
    velocity_horizontal_vec = np.concatenate((velocity_horizontal_vec1,velocity_horizontal_vec2,velocity_horizontal_vec3,velocity_horizontal_vec4),axis=0)
    altitude_vec = np.concatenate((altitude_vec1,altitude_vec2,altitude_vec3,altitude_vec4),axis=0)
    velocity_vertical_vec = np.concatenate((velocity_vertical_vec1,velocity_vertical_vec2,velocity_vertical_vec3,velocity_vertical_vec4),axis=0)
    trajectory_angle_vec = np.concatenate((trajectory_angle_vec1,trajectory_angle_vec2,trajectory_angle_vec3,trajectory_angle_vec4),axis=0)
    fan_rotation_vec = np.concatenate((fan_rotation_vec1,fan_rotation_vec2,fan_rotation_vec3,fan_rotation_vec4),axis=0)
    compressor_rotation_vec = np.concatenate((compressor_rotation_vec1,compressor_rotation_vec2,compressor_rotation_vec3,compressor_rotation_vec4),axis=0)

    return time_vec,velocity_vec,distance_vec,velocity_horizontal_vec,altitude_vec,velocity_vertical_vec,trajectory_angle_vec,fan_rotation_vec,compressor_rotation_vec


def aircraft_noise(takeoff_parameters, landing_parameters,aircraft_parameters,aircraft_geometry,engine_parameters,runaway_parameters,noise_parameters,vehicle):
    
    # ---- Takeoff noise ----

    # Takeoff flight path:
    time_vec,velocity_vec,distance_vec,velocity_horizontal_vec,altitude_vec,velocity_vertical_vec,trajectory_angle_vec,fan_rotation_vec,compressor_rotation_vec = takeoff_profile(takeoff_parameters,landing_parameters,aircraft_parameters,runaway_parameters,engine_parameters,vehicle)

    # Noise calculation - EPNdB
    TO_noise = takeoff_EPNdB(time_vec,velocity_vec,distance_vec,velocity_horizontal_vec,altitude_vec,velocity_vertical_vec,trajectory_angle_vec,fan_rotation_vec,compressor_rotation_vec, throttle_position, takeoff_parameters,noise_parameters,aircraft_geometry,engine_parameters,vehicle)
    sideline_noise,_ = sideline_EPNdB(time_history,throttle_position,takeoff_parameters,noise_parameters,aircraft_geometry,engine_parameters,vehicle)

    # ---- Aproach and landing noise ----

    # Takeoff flight path:
    _ = approach_profile(takeoff_parameters,landing_parameters,aircraft_parameters,vehicle)

    # Noise calculation - EPNdB
    landing_noise = approach_EPNdB(_,landing_parameters,noise_parameters,aircraft_geometry,vehicle)

    return takeoff_noise, sideline_noise, landing_noise

def takeoff_noise(time_vec,velocity_vec,distance_vec,velocity_horizontal_vec,altitude_vec,velocity_vertical_vec,trajectory_angle_vec,fan_rotation_vec,compressor_rotation_vec, throttle_position, takeoff_parameters,noise_parameters,aircraft_geometry,engine_parameters,vehicle):

    XA = noise_parameters['takeoff_longitudinal_distance_mic']
    dlat = noise_parameters['takeoff_lateral_distance_mic'] 
    for i in range(1,len(time_vec)):
        H1 = altitude_vec[i]
        XB = distance_vec[i]
        gamma = trajectory_angle_vec[i]
        L1 = np.abs(XB-XA)
        R = np.sqrt(H1**2 + L1**2 + dlat**2)
        termo1 = np.sqrt(((H1 - L1*np.tan(np.abs(gamma*deg_to_rad)))**2 + dlat**2)/(R**2))
        if XB > XA:
            theta = np.arcsin(termo1)/deg_to_rad
        elif XB == XA:
            theta = 90
        else:
            theta = 180-(np.arcsin(termo1)/deg_to_rad)
        
        vairp = velocity_vec[i]
        N1 = fan_rotation_vec[i]
        N2 = compressor_rotation_vec[i]

        fi = np.arctan(H1/dlat)/deg_to_rad
        if vairp == 0:
            vairp = 0.1
        
        FPhase = 1
        if H1 >= 100
            aircraft_geometry['main_landing_gear_position'] = 2
            aircraft_geometry['main_landing_gear_position'] = 2
        else:
            aircraft_geometry['main_landing_gear_position'] = 1
            aircraft_geometry['main_landing_gear_position'] = 1

        saidatemp =     


    return frequencies, SPL, time

def takeoff_EPNdB(time_vec,velocity_vec,distance_vec,velocity_horizontal_vec,altitude_vec,velocity_vertical_vec,trajectory_angle_vec,fan_rotation_vec,compressor_rotation_vec, throttle_position, takeoff_parameters,noise_parameters,aircraft_geometry,engine_parameters,vehicle):

    frequencies, SPL, time = takeoff_noise(time_vec,velocity_vec,distance_vec,velocity_horizontal_vec,altitude_vec,velocity_vertical_vec,trajectory_angle_vec,fan_rotation_vec,compressor_rotation_vec, throttle_position, takeoff_parameters,noise_parameters,aircraft_geometry,engine_parameters,vehicle)


    
    return
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
    engine['fan_rotation'] = 4952
    engine['compressor_rotation'] = 14950

    runaway_parameters = {}
    runaway_parameters['mu_roll'] = 0.03
    runaway_parameters['mu_brake'] = 0.3

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




def takeoff_integration(
    initial_block_altitude,
    initial_block_distance,
    initial_block_trajectory_angle,
    initial_block_time,
    initial_block_velocity,
    initial_block_horizontal_velocity,
    initial_block_vertical_velocity,
    initial_fan_rotation,
    initial_compressor_rotation,
    aircraft_parameters,
    takeoff_parameters,
    runaway_parameters,
    landing_parameters,
    vehicle,
    rho_ISA,
    stop_criteria,
    phase
    ):

    if phase == 'ground':
        t0 = initial_block_time
        z0 = [initial_block_distance, initial_block_velocity]
        solver = ode(ground)
        solver.set_integrator('vode', nsteps=1000)
        solver.set_f_params(takeoff_parameters,runaway_parameters,landing_parameters,rho_ISA,vehicle)
        solver.set_initial_value(z0, t0)
        t1 = initial_block_time + 50
        # N = 50
        t = np.linspace(t0, t1,1000)
        N = len(t)
        sol = np.empty((N,2))
        sol_var = np.empty((N,6))
        sol[0] = z0
        times = np.empty((N, 1))


    if phase == 'flare':
        t0 = initial_block_time
        z0 = [initial_block_distance, initial_block_velocity, initial_block_altitude, initial_block_vertical_velocity, initial_block_trajectory_angle]
        solver = ode(flare)
        solver.set_integrator('vode', nsteps=1000)
        solver.set_f_params(aircraft_parameters, takeoff_parameters,runaway_parameters,landing_parameters,rho_ISA,vehicle)
        solver.set_initial_value(z0, t0)
        t1 = initial_block_time + 50
        # N = 50
        t = np.linspace(t0, t1,1000)
        N = len(t)
        sol = np.empty((N,5))
        sol_var = np.empty((N,3))
        sol[0] = z0
        times = np.empty((N, 1))


    # if phase == 'climb':

    #     climb_V_cas = np.sqrt(initial_block_horizontal_velocity**2 + initial_block_vertical_velocity**2)/kt_to_ms
    #     _, _, _, _, _, rho_ISA, a = atmosphere_ISA_deviation(initial_block_altitude, 0)
    #     mach_climb = climb_V_cas/(a)

    #     t0 = initial_block_time
    #     z0 = [initial_block_distance, initial_block_altitude]
    #     solver = ode(climb)
    #     solver.set_integrator('vode', nsteps=1000)
    #     solver.set_f_params(climb_V_cas, mach_climb, 0,
    #                     stop_criteria, vehicle)
    #     solver.set_initial_value(z0, t0)
    #     t1 = initial_block_time + 50
    #     # N = 50
    #     t = np.linspace(t0, t1,1000)
    #     N = len(t)
    #     sol = np.empty((N,2))
    #     sol_var = np.empty((N,6))
    #     sol[0] = z0
    #     times = np.empty((N, 1))



    # Repeatedly call the `integrate` method to advance the
    # solution to time t[k], and save the solution in sol[k].
    k = 1

    if phase == 'ground':
        while solver.successful() and solver.y[1] <= stop_criteria:
            solver.integrate(t[k])
            sol[k] = solver.y
            times[k] = solver.t
            
            _, _, _, _, _, rho_ISA, a = atmosphere_ISA_deviation(0, 0)
            mach = solver.y[1]/(a)
            thrust_force, fuel_flow, vehicle = turbofan(
                0, mach, 1, vehicle)

            engine = vehicle['engine']

            sol_var[k,0] = sol[k,1]
            sol_var[k,1] = 0
            sol_var[k,2] = 0
            sol_var[k,3] = 0
            sol_var[k,4] = engine['fan_rotation']
            sol_var[k,5] = engine['compressor_rotation']

            k += 1

            # print(sol_var[k])
            

        time_vec = times[1:k]
        velocity_vec = sol[1:k, 1]
        distance_vec = sol[1:k, 0]
        velocity_horizontal_vec = sol_var[1:k,0]
        altitude_vec = sol_var[1:k,1]
        velocity_vertical_vec = sol_var[1:k,2]
        trajectory_angle_vec = sol_var[1:k,3]
        fan_rotation_vec = sol_var[1:k,4]
        compressor_rotation_vec = sol_var[1:k,5]


        final_block_time = time_vec[-1]
        final_block_velocity = velocity_vec[-1]
        final_block_distance = distance_vec[-1]
        final_block_horizontal_velocity = velocity_vec[-1]
        final_block_altitude = altitude_vec[-1]
        final_block_vertical_velocity =  velocity_vertical_vec[-1]
        final_block_trajectory_angle = trajectory_angle_vec[-1]
        final_fan_rotation = fan_rotation_vec[-1]
        final_compressor_rotation = compressor_rotation_vec[-1]

        # plt.plot(time, compressor_rotation)
        # plt.show()
    
    elif phase == 'flare':
        while solver.successful() and solver.y[2] <= stop_criteria:
            solver.integrate(t[k])
            sol[k] = solver.y
            times[k] = solver.t

            _, _, _, _, _, rho_ISA, a = atmosphere_ISA_deviation(0, 0)
            mach = solver.y[1]/(a*kt_to_ms)
            thrust_force, fuel_flow, vehicle = turbofan(
                0, mach, 1, vehicle)
            engine = vehicle['engine']

            sol_var[k,0] = np.sqrt(sol[k,1]**2 + sol[k,3]**2)
            sol_var[k,1] = engine['fan_rotation']
            sol_var[k,2] = engine['compressor_rotation']

            k += 1

        time_vec = times[1:k]
        velocity_vec = sol_var[1:k,0]
        distance_vec = sol[1:k, 0]
        velocity_horizontal_vec = sol[1:k, 1]
        altitude_vec = sol[1:k, 2]
        velocity_vertical_vec = sol[1:k, 3]
        trajectory_angle_vec = sol[1:k, 4]
        fan_rotation_vec = sol_var[1:k,1]
        compressor_rotation_vec = sol_var[1:k,2]


        final_block_time = time_vec[-1]
        final_block_velocity = velocity_vec[-1]
        final_block_distance = distance_vec[-1]
        final_block_horizontal_velocity = velocity_vec[-1]
        final_block_altitude = altitude_vec[-1]
        final_block_vertical_velocity =  velocity_vertical_vec[-1]
        final_block_trajectory_angle = trajectory_angle_vec[-1]
        final_fan_rotation = fan_rotation_vec[-1]
        final_compressor_rotation = compressor_rotation_vec[-1]


    elif phase == 'climb':

        if math.floor(initial_block_time) == math.ceil(initial_block_time + takeoff_parameters['time_step']):
            time = math.floor(initial_block_time) + takeoff_parameters['time_step']
        else:
            time = math.ceil(initial_block_time)

        V_35 = np.sqrt(initial_block_horizontal_velocity**2 + initial_block_vertical_velocity**2)
        _, _, _, _, _, rho_ISA, a = atmosphere_ISA_deviation(initial_block_altitude, 0)
        mach =V_35/(a*kt_to_ms)

        thrust_force, fuel_flow, vehicle = turbofan(
            initial_block_altitude, mach, 1, vehicle)
        
        engine = vehicle['engine']

        total_thrust_force = thrust_force*aircraft['number_of_engines']

        if initial_block_altitude <= 100:
            gamma = np.arctan(total_thrust_force/((aircraft['maximum_takeoff_weight']*GRAVITY) - (aircraft_parameters['CD_air_LG_down']/aircraft_parameters['CL_air'])))
        else:
            gamma = np.arctan(total_thrust_force/((aircraft['maximum_takeoff_weight']*GRAVITY) - (aircraft_parameters['CD_air_LG_up']/aircraft_parameters['CL_air'])))
        
        rate_of_climb = V_35*np.sin(gamma)
        delta_altitude = rate_of_climb*takeoff_parameters['time_step']
        delta_distance = V_35*takeoff_parameters['time_step']*np.cos(gamma)
        

        time_vec = [time]
        velocity_vec = [V_35]
        distance_vec = [float(initial_block_distance+delta_distance)]
        velocity_horizontal_vec = [float(V_35*np.cos(gamma))]
        altitude_vec = [float(initial_block_altitude+delta_altitude)]
        velocity_vertical_vec = [float(rate_of_climb)]
        trajectory_angle_vec = [float(gamma*(180/np.pi))]
        fan_rotation_vec = [float(engine['fan_rotation'])]
        compressor_rotation_vec = [float(engine['compressor_rotation'])]
 
        iteration = 0
        for i in range(1,1000):

            time = time + takeoff_parameters['time_step']
            distance = distance_vec[-1]
            altitude = altitude_vec[-1]

            iteration = iteration + 1

            _, _, _, _, _, _, a = atmosphere_ISA_deviation(altitude, 0)

            mach = velocity_vec[-1]/(a*kt_to_ms)
            thrust_force, fuel_flow, vehicle = turbofan(
            altitude, mach, 1, vehicle)

            engine = vehicle['engine']

            total_thrust_force = thrust_force*aircraft['number_of_engines']
            
            N1 = engine['fan_rotation']
            N2 = engine['compressor_rotation']


            if initial_block_altitude <= 100:
                gamma = np.arctan(total_thrust_force/((aircraft['maximum_takeoff_weight']*GRAVITY) - (aircraft_parameters['CD_air_LG_down']/aircraft_parameters['CL_air'])))
            else:
                gamma = np.arctan(total_thrust_force/((aircraft['maximum_takeoff_weight']*GRAVITY) - (aircraft_parameters['CD_air_LG_up']/aircraft_parameters['CL_air'])))
            rate_of_climb = V_35*np.sin(gamma)
            
            delta_altitude = rate_of_climb*takeoff_parameters['time_step']
            delta_distance = V_35*takeoff_parameters['time_step']*np.cos(gamma)

            time_vec.append(time)
            velocity_vec.append(V_35)
            distance_vec.append(float(distance+delta_distance))
            velocity_horizontal_vec.append(float(V_35*np.cos(gamma)))
            altitude_vec.append(float(altitude+delta_altitude))
            velocity_vertical_vec.append(float(rate_of_climb))
            trajectory_angle_vec.append(float(gamma*(180/np.pi)))
            fan_rotation_vec.append(float(N1))
            compressor_rotation_vec.append(float(N2))

            if distance_vec[-1] >= 10000:
                break
        
        time_vec = np.asarray([time_vec]).T
        # velocity_vec = np.asarray([velocity_vec]).T
        # distance_vec = np.asarray([distance_vec]).T
        # velocity_horizontal_vec = np.asarray([velocity_horizontal_vec]).T
        # altitude_vec = np.asarray([altitude_vec]).T
        # velocity_vertical_vec = np.asarray([velocity_vertical_vec]).T
        # trajectory_angle_vec = np.asarray([trajectory_angle_vec]).T
        # fan_rotation_vec = np.asarray([fan_rotation_vec]).T
        # compressor_rotation_vec = np.asarray([compressor_rotation_vec]).T

        final_block_time = time_vec[-1]
        final_block_velocity = velocity_vec[-1]
        final_block_distance = distance_vec[-1]
        final_block_horizontal_velocity = velocity_vec[-1]
        final_block_altitude = altitude_vec[-1]
        final_block_vertical_velocity =  velocity_vertical_vec[-1]
        final_block_trajectory_angle = trajectory_angle_vec[-1]
        final_fan_rotation = fan_rotation_vec[-1]
        final_compressor_rotation = compressor_rotation_vec[-1]





    return (final_block_altitude,
    final_block_distance,
    final_block_trajectory_angle,
    final_block_time,
    final_block_velocity,
    final_block_horizontal_velocity,
    final_block_vertical_velocity,
    final_fan_rotation,
    final_compressor_rotation,
    time_vec,
    velocity_vec,
    distance_vec,
    velocity_horizontal_vec,
    altitude_vec,
    velocity_vertical_vec,
    trajectory_angle_vec,
    fan_rotation_vec,
    compressor_rotation_vec)
    
def ground(time,state,takeoff_parameters,runaway_parameters,landing_parameters,rho_ISA,vehicle):
    wing = vehicle['wing']
    engine = vehicle['engine']

    distance = state[0]
    velocity = state[1]

    constant = np.cos(takeoff_parameters['lambda']) + runaway_parameters['mu_roll']*np.sin(takeoff_parameters['lambda'])
    K0 = engine['T0']*constant - runaway_parameters['mu_roll']*takeoff_parameters['takeoff_weight']
    K1 = engine['T1']*constant
    K2 = engine['T2']*constant + 0.5*rho_ISA*wing['area']*(runaway_parameters['mu_roll']*landing_parameters['CL_3P'] - landing_parameters['CD_3P'])
    
    # Cálculo das derivadas
    x_dot = velocity
    V_dot = (GRAVITY/takeoff_parameters['takeoff_weight']) * (K0 + K1*velocity + K2*velocity*velocity)
    

    dout = np.asarray([x_dot, V_dot])
    dout = dout.reshape(2, )
    return dout

def flare(time,state,aircraft_parameters,takeoff_parameters,runaway_parameters,landing_parameters,rho_ISA,vehicle):
    wing = vehicle['wing']

    distance = state[0]
    velocity_horizontal = state[1]
    altitude = state[2]
    velocity_vertical = state[3]
    trajectory_angle = state[4]

    V_resultant = np.sqrt(velocity_vertical**2 + velocity_horizontal**2)
    gamma = trajectory_angle

    _, _, _, _, _, rho_ISA, a = atmosphere_ISA_deviation(altitude, 0)

    mach = V_resultant/(a*kt_to_ms)
    throttle_position = 1.0
    thrust_force, fuel_flow, vehicle = turbofan(
        altitude, mach, throttle_position, vehicle)  # force [N], fuel flow [kg/hr]
    
    total_thrust_force = thrust_force*aircraft['number_of_engines']

    drag = 0.5*rho_ISA*(V_resultant**2)*wing['area']*aircraft_parameters['CD_air_LG_down']
    lift = 0.5*rho_ISA*(V_resultant**2)*wing['area']*aircraft_parameters['CL_air']

    velocity_horizontal = V_resultant*np.cos(gamma)
    parameter2_dot = GRAVITY/(aircraft['maximum_takeoff_weight']*GRAVITY) * (total_thrust_force - drag - aircraft['maximum_takeoff_weight']*np.sin(gamma))*np.cos(gamma) - GRAVITY*(1.3 - np.cos(gamma))*np.sin(gamma)
    velocity_vertical = V_resultant*np.sin(gamma)
    parameter4_dot = GRAVITY*(1.3-np.cos(gamma))*np.cos(gamma) + (GRAVITY/aircraft['maximum_takeoff_weight'])*(total_thrust_force - drag - aircraft['maximum_takeoff_weight']*np.sin(gamma))*np.sin(gamma)
    gamma_dot = (GRAVITY/V_resultant)*(1.3 - np.cos(gamma))


    dout = np.asarray([velocity_horizontal, parameter2_dot, velocity_vertical,  parameter4_dot, gamma_dot])
    dout = dout.reshape(5, )
    return dout

def climb(time, state, climb_V_cas, mach_climb, delta_ISA, final_block_altitude, vehicle):
    aircraft = vehicle['aircraft']

    distance = state[0]
    altitude = state[1]

    mass = aircraft['maximum_takeoff_weight']

    if altitude > final_block_altitude:
        return
        
    _, _, _, _, _, rho_ISA, _ = atmosphere_ISA_deviation(altitude, delta_ISA)
    throttle_position = 1.0

    if climb_V_cas > 0:
        mach = V_cas_to_mach(climb_V_cas, altitude, delta_ISA)
    else:
        mach = mach_climb

    thrust_force, fuel_flow , vehicle = turbofan(
        altitude, mach, throttle_position, vehicle)  # force [N], fuel flow [kg/hr]
    thrust_to_weight = aircraft['number_of_engines'] * \
        thrust_force/(mass*GRAVITY)
    rate_of_climb, V_tas, climb_path_angle = rate_of_climb_calculation(
        thrust_to_weight, altitude, delta_ISA, mach, mass, vehicle)
    # if rate_of_climb < 300:
    #     print('rate of climb violated!')

    V_tas = V_tas*kt_to_ms

    rate_of_climb = rate_of_climb*0.0166667

    x_dot = (V_tas*101.269)*np.cos(climb_path_angle)  # ft/min
    h_dot = rate_of_climb  # ft/min
    # W_dot = -2*fuel_flow*kghr_to_kgmin  # kg/min
    time_dot = h_dot*0.0166667
    # dout = np.asarray([x_dot, h_dot, W_dot])
    dout = np.asarray([x_dot, h_dot])
    dout = dout.reshape(2, )

    return dout
# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================

wing['area'] = 72
aircraft['maximum_takeoff_weight'] = 25579
aircraft['CL_maximum_landing'] = 2.8517
aircraft['CL_maximum_takeoff'] = 2.2517

engine['fan_pressure_ratio'] = 1.6
engine['compressor_pressure_ratio'] = 27
engine['bypass'] = 4
engine['fan_diameter'] = 1
engine['turbine_inlet_temperature'] = 1410

noise_calculation(vehicle)