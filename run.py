"""Calculate the fields for all time, then animate them.

run.py takes command line input to set the modes of the simulation.
It then calculates both fields and animates them.

Attributes:
    Command Line Arguments - 

        $ python run.py amplitude,frequency amplitude_2,frequency_2

    The script takes a list of amplitudes (float) and frequencies (int)
    delimited by a space. If no args are given, the default 1,2 will be used.

    Any argument that does not follow this format will return a help message.
    Including $ python run.py help
    
Output:

    Creates a matplotlib.animation of the simulation

"""


from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sys
# local import
from maxwell_eq import *


def run(mode_list):
    """ Call simulate from maxwell_eq.py to set the Electric
    and Magnetic fields. Then, set up a plot which will list
    all of the amplitudes and frequencies specified in the 
    Command Line input. Finally, define the init and animate functions
    which FuncAnimation will use to animate the output

    Args:
        mode_list (list of tuples): Each tuple is of the form
                                    (frequency,amplitude). The mode list
                                    determines the initial conditions for
                                    the simulation. 
    Output: 
        generates an animation. Each frame of the animation represents a time
        n. Each frame plots Ex[:,n] and By[:,n] - the magnitudes as a function
        of position.
    """

    Ex, By = simulate(mode_list)

    fig, ax = plt.subplots()
    plt.xlabel("z axis")
    plt.ylabel("Magnitude")
    input_string = "Modes\n"
    for amp, freq in mode_list:
        input_string += f"amp: {amp}, freq: {freq}\n"
    plt.text(150,0.4*np.max(Ex[:,0]),input_string)
    fig.suptitle("E and B magnitudes vs z axis")

    x = np.linspace(0,zmax,zmax)
    line, = ax.plot(x, Ex[:,0], label = "Electric Field", color = "orange")
    bline, = ax.plot(x,By[:,0], label = "Magnetic Field", color = "blue")

    def init():  

        line.set_ydata(np.zeros(len(x)))
        bline.set_ydata(np.zeros(len(x)))
        return line,


    def animate(i):

        line.set_ydata(Ex[:,i])
        bline.set_ydata(By[:,i])
        return line,  bline


    ani = FuncAnimation(
        fig, animate, init_func=init,frames = np.arange(0,tmax,100), 
                                            interval=5, blit=True)

    plt.legend()
    plt.show()

def help_():

    print("\n\n\ntry: python run.py 1,2\n\nThe 1 represents "\
          "the amplitude of the initial Sine wave, the 2 represents "\
          "the number of peaks. \n\n\ntry: python run.py 1,1 3,4\n\n"\
          "The initial conditions will be a Sine wave of amplitude 1 "\
          "with 1 peak, plus a Sine wave of amplitude 3 with 4 peaks.\n\n\n")

    sys.exit()


if __name__ == '__main__':

    """Parse command line arguments
    then call run(). If CL args are 
    incorrectly formatted, call help_().
    """
    mode_list = []
    if len(sys.argv) == 1:
        mode_list = [(1,2)]
    elif sys.argv[1] == "help":
        help_()
    else:   
        for mode in sys.argv[1:]:
            try:
                amp_freq_tuple = mode.split(",")
                amp, freq = amp_freq_tuple
                mode_list.append(( float(amp), int(freq) ))

            except (IndexError, ValueError):
                help_()

    print(f"\nRunning simulation with initial conditions:")
    for amp, freq in mode_list:
        print(f"amplitude = {amp}, frequency = {freq}")

    run(mode_list)