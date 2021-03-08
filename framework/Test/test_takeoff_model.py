import numpy as np
from scipy.integrate import ode
def takeoff_int(state,time,velocity, rho,g,m,Sref):
    position = state[0]
    mu = 0.03
    

    T0 = 9.3527
    T1 = -0.1170
    T2 = -0.0173

    K = 0.0929
    K1 = -0.0088
    CLa = 3.9591
    CL0 = 0.3234
    CD0 = 0.0937
    Sref = 0.325
    alpha_dec = 0


    T = (T0 + T1*velocity + T2*velocity**2)*1

    CL = CL0 + alpha_dec*CLa

    CD = CD0 + K1*CL + K*CL**2
    L = (rho*velocity**2 )/2 * Sref*CL
    D = (rho*velocity**2)/2 * Sref * CD
    N = max(0,(m*g - L))
    Fat = N*mu

    x_dot = m*velocity/(T-D-Fat)

    dout = np.asarray([x_dot])
    dout = dout.reshape(1, )

    return dout
rho = 1.1
g = 9.81
Ks = 1.1
m = 2.522
Sref = 0.325
CLmax = 1.56

velocity = Ks*np.sqrt((2*g*m)/(rho*Sref*CLmax))
state = [0]

time = np.arange(0, 10., .001)
solution = odeint(takeoff_int,state,time,(velocity,rho,g,m,Sref))

print(solution)




