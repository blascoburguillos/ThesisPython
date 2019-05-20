#!/usr/bin/env python

import numpy as np
from gnssr.simulator.geometry.geometry import *
import gnssr.simulator.rcs.sea_rcs as sea_rcs

def radar_cross_section_military(r, t, sim_config):
    """
    Args:
        r (numpy.ndarray with size(3,)): Position on the local coordinates.
        sim_config: 
        sim_config: Instance of simulation_configuration class.
    Returns:
        numpy.ndarray with  size(1,).
    """

    #100x25m 
    v_x = 33 # m/s
    wake_x = 1.5e3 - v_x*t#m
    wake_y = 0.5e3 #m
    wake_x_size = 200 #m
    wake_y_size = wake_x_size*np.tan(20*np.pi/180)
    wake = np.logical_and.reduce((
            np.abs(r[0]-wake_x) < wake_x_size, 
            wake_y_size/wake_x_size*(r[0]-wake_x) - (r[1]-wake_y) >= 0, 
            wake_y_size/wake_x_size*(r[0]-wake_x) + (r[1]-wake_y) >= 0
            ))
    sea = sea_rcs.radar_cross_section(r, sim_config)
    #target = rcs_sea(r, sim_config, sim_config.u_10*2)
    np.place(sea, wake, 0)
    #np.place(target, np.logical_not(wake), 0)
    return sea #+ target

def radar_cross_section(r, t, sim_config):
    """
    Args:
        r (numpy.ndarray with size(3,)): Position on the local coordinates.
        sim_config: 
        sim_config: Instance of simulation_configuration class.
    Returns:
        numpy.ndarray with  size(1,).
    """

    #100x25m 
    v_x = 25 # m/s
    wake_x = 5e3 - v_x*t #m
    wake_y = 0.5e3 #m
    wake_x_size = 200 #m
    wake_y_size = wake_x_size*np.tan(19.5*np.pi/180)
    wake = np.logical_and.reduce((
            np.abs(r[0]-wake_x) < wake_x_size, 
            wake_y_size/wake_x_size*(r[0]-wake_x) - (r[1]-wake_y) >= 0, 
            wake_y_size/wake_x_size*(r[0]-wake_x) + (r[1]-wake_y) >= 0
            ))
    sea_matrix = np.copy(sea_rcs.radar_cross_section(r, sim_config))

    target_matrix = np.copy(sea_matrix)*1.41 # 1.5 dB increase
    np.place(sea_matrix, wake, 0)
    np.place(target_matrix, np.logical_not(wake), 0)
    return sea_matrix + target_matrix

    '''
    #Wind variation  
    import copy
    sim_config_2 = copy.deepcopy(sim_config)
    sim_config_2.u_10 = sim_config.u_10*2
    target_matrix = np.copy(sea_rcs.radar_cross_section(r, sim_config_2))
    #np.place(sea, wake, 0)
    np.place(sea_matrix, wake, 0)
    np.place(target_matrix, np.logical_not(wake), 0)
    return sea_matrix + target_matrix
    '''

    '''
    # Zero 
    sea = sea_rcs.radar_cross_section(r, sim_config)
    #target = rcs_sea(r, sim_config, sim_config.u_10*2)
    np.place(sea, wake, 0)
    #np.place(target, np.logical_not(wake), 0)
    return sea
    '''
