 # Stability analysis for a varying courant number and fixed spatial resolution

# Read in required packages and scripts
from initialConditions import *
from advectionSchemes import *
from diagnostics import *
import numpy as np
import math

def main(xmin, xmax, nx, lower_c, upper_c, num_of_c):
    "Given an initial condition, and spatial grid conditions. Run each scheme"
    "for a even number of courant numbers between lower_c and upper_c"

    # Derived grid points
    dx = (xmax - xmin)/nx
    x = np.arange(xmin, xmax, dx)

    phiOld = cosBell(x, 0, 0.75) # Initial condition

    # Determine the range of nt values to test the desired courant numbers
    lower_nt = math.floor(nx / upper_c)
    upper_nt = math.ceil(nx / lower_c)
    step = int((upper_nt - lower_nt)/num_of_c) # Integer difference between each nt value
    nt_values = np.arange(lower_nt, upper_nt, step)

    error_Matrix = np.zeros((len(nt_values), 2)) # Matrix to store courant value and l2 error

    # Error calculation for FTBS scheme
    for j,nt in enumerate(nt_values):
        c = nx/nt # Calculate the courant number
        error_Matrix[j, 0] = c
        phiFTBS = FTBS(phiOld.copy(), c, nt) # Run the scheme for each (c, nt) pair
        phiAnalytic = cosBell((x - c*nt*dx)%(xmax - xmin), 0, 0.75) # Find analytic solution for (c, nt) pair
        error_Matrix[j, 1] = l2ErrorNorm(phiFTBS, phiAnalytic) # Store L2 errors
    plt.plot(error_Matrix[:, 0], error_Matrix[:, 1],'--g.', label = 'FTBS') # Plot results

    # Error calculation for FTCS scheme
    for j,nt in enumerate(nt_values):
        c = nx/nt
        error_Matrix[j, 0] = c
        phiFTCS = FTCS(phiOld.copy(), c, nt) # Run the scheme for each (c, nt) pair
        phiAnalytic = cosBell((x - c*nt*dx)%(xmax - xmin), 0, 0.75)
        error_Matrix[j, 1] = l2ErrorNorm(phiFTCS, phiAnalytic) # Store L2 errors
    plt.plot(error_Matrix[:, 0], error_Matrix[:, 1],'--r.', label = 'FTCS')

    # Error calculation for BTCS scheme
    for j,nt in enumerate(nt_values):
        c = nx/nt
        error_Matrix[j, 0] = c
        phiBTCS = BTCS(phiOld.copy(), c, nt) # Run the scheme for each (c, nt) pair
        phiAnalytic = cosBell((x - c*nt*dx)%(xmax - xmin), 0, 0.75)
        error_Matrix[j, 1] = l2ErrorNorm(phiBTCS, phiAnalytic) # Store L2 errors
    plt.plot(error_Matrix[:, 0], error_Matrix[:, 1],'--c.', label = 'BTCS')

    # Error calculation for CTCS scheme
    for j,nt in enumerate(nt_values):
        c = nx/nt
        error_Matrix[j, 0] = c
        phiCTCS = CTCS(phiOld.copy(), c, nt) # Run the scheme for each (c, nt) pair
        phiAnalytic = cosBell((x - c*nt*dx)%(xmax - xmin), 0, 0.75)
        error_Matrix[j, 1] = l2ErrorNorm(phiCTCS, phiAnalytic) # Store L2 errors
    plt.semilogy(error_Matrix[:, 0], error_Matrix[:, 1],'--m.', label = 'CTCS')

    # Error calculation for SL scheme
    nt_values = nt_values[nt_values <= 100] # Use less nt_values as SL scheme is slow
    error_Matrix = np.zeros((len(nt_values), 2))
    for j,nt in enumerate(nt_values):
        c = nx/nt
        error_Matrix[j, 0] = c
        phi_sem_lag = sem_lag(phiOld.copy(), c, nt, x, dx) # Run the scheme for each (c, nt) pair
        phiAnalytic = cosBell((x - c*nt*dx)%(xmax - xmin), 0, 0.75)
        error_Matrix[j, 1] = l2ErrorNorm(phi_sem_lag, phiAnalytic) # Store L2 errors
    plt.semilogy(error_Matrix[:, 0], error_Matrix[:, 1],'--y.', label = 'SL')

    #Plot Details
    plt.xlabel('log(c)')
    plt.ylabel('L2 Error (logarithmic)')
    plt.title('L2 Error as function of c')
    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=5)
    plt.savefig('plots/analysis/L2Error_vs_Courant_Number2', bbox_inches='tight')
    plt.close('all')

    return
