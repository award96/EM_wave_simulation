"""Framework for simulating an Electromagnetic Wave using Maxwell's Equations

maxwell_eq.py takes a list of normal modes (frequencies that fit exactly
in the bounds of our simulation) and returns the Electric Field and 
Magnetic Field amplitudes for every point on the z-axis for 
each step in time. The simulation is that of an infinite plane wave.

Note on Geometric Meaning:
    An electromagnetic wave (light wave) travelling in the z-direction
    will have an Electric Field pointing in the x-direction and a 
    Magnetic Field pointing in the y-direction.

Attributes:
    The ratios of the various constants keeps the simulation stable in two ways.
    First - none of the floats in update_fields() are too large or too small for python's
            64 bit representation to accurately represent.
    Second - the simulation does not evolve too quickly.

    mu (float): The constant mu in Maxwell's Equations

    epsil (float): The constant epsil in Maxwell's Equations, together with 
                    mu these set the "speed of light" for our simulation
        
    fact (float): The stability factor for the algorithm.
                  Maxwell's equations are partial differential equations.
                  This means they represent how variables change as a result
                  of other variables changing (after a time delta t, the change
                  in x will be delta x).
                  fact = delta t / 2 * delta z , if it is big that means we are
                  evolving the simulation rapidly through time, if it is small that
                  means we are evolving the simulation slowly through time.
                  It must satisfy the Courant Stability condition if we are to have
                  a stable simulation

    zmax (int): The size of the simulated space, or the number of indices in the spatial array.

    tmax (int): The length of the simulation, or the number of indices in the time array.

Returns:

    Ex (numpy array): The Electric field
    By (numpy array): The Magnetic field

    Ex and By are two numpy arrays which contain the Electric field and Magnetic field magnitudes
    at each spatial index: 0 -> i -> zmax , for every time index 0 -> n -> tmax
    Ex[i,:] is the Electric field at point i for every timestep
    Ex[:,n] is the Electric field at every point for the n'th timestep

"""


import numpy as np

mu = 1
epsil = 0.5
fact = 0.005
zmax = 201
tmax = zmax * 10**3 # makes for a smoother animation loop


def simulate(mode_list):
    """ For every mode in the mode list, add them together
    and simulate how the electric and magnetic fields evolve with time

    Args:
        mode_list (list of tuples):
        The first element of each tuple is that mode's amplitude
        (relative strength), the second element is the frequency 
        of that mode (how many peaks it has between 0 and zmax)

    Returns:
        Ex, By : two arrays of size (zmax, tmax). The electric field, and
        magnetic field amplitude at every point in space for each 
        step in time.
    """
    # Electric field and Magnetic field
    Ex = np.zeros((zmax,tmax),float)
    By = np.zeros((zmax,tmax),float)
    # Set up the initial conditions 
    # and let the differential equations evolve the system
    initial_conditions(Ex,By, mode_list)
    update_fields(Ex,By)
    return Ex, By

def initial_conditions(Ex,By, mode_list):
    """ Sets the Ex and By arrays for time = 0
    Args:
        Ex: array of size (zmax,tmax)
        By: array of size (zmax,tmax)
    """
    k = np.linspace(0,zmax,zmax)
    Ex[:zmax,0] = fourier_func(k, mode_list)
    By[:zmax,0] = fourier_func(k, mode_list) * np.sqrt(mu * epsil)

def update_fields(Ex, By):
    """ The algorithm operates by updating the electric field
    on even time steps and updating the magnetic field on odd time steps

    This reflects how Electric and Magnetic fields respond to eachother in real
    life and is required for stability of the algorithm

    Args:
        Ex: array of size (zmax,tmax)
        By: array of size (zmax,tmax)
    """

    for n in range(tmax-1):
        
        if n%2 == 0:
            # derived from Maxwells Eqtns
            Ex[1:-1,n+1] = Ex[1:-1,n] - \
                          (fact/(mu*epsil))*(By[2:,n] - By[0:-2,n]  )
            
            Ex[0,n+1]    = Ex[0,n]    - \
                          (fact/(mu*epsil))*(By[1,n]      - By[-1,n])
            
            Ex[-1,n+1]   = Ex[-1,n]   - \
                          (fact/(mu*epsil))*(By[0,n]  - By[-2,n])
            
            # B field stays the same
            By[:,n+1] = By[:,n]
        
        else:
            # derived from Maxwells Eqtns
            By[1:-1,n+1] = By[1:-1,n] -  fact * (Ex[2:,n] - Ex[0:-2,n]  )
            By[0,n+1]    = By[0,n]    -  fact * (Ex[1,n]      - Ex[-1,n])
            By[-1,n+1]   = By[-1,n]   -  fact * (Ex[0,n]      - Ex[-2,n])
            # E field stays the same
            Ex[:,n+1] = Ex[:,n]

def sin_func(amp,freq,k):
    # return the sin function for all values in 
    # list k
    return amp * np.sin(freq * np.pi * k / zmax)

def fourier_func(k, mode_list):
    # return sum of multiple sin functions
    # for all values in list k
    
    sum_ = 0
    for amp, freq in mode_list:
        sum_ += sin_func(amp, freq, k)
    return sum_


    


            


