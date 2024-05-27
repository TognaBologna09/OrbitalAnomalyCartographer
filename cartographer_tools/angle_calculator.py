import numpy as np
from scipy.optimize import root


# Setting, Getting the three angles
calculated_angles = np.zeros(3)

def get_true_anomaly():
    return calculated_angles[0]

def get_eccentric_anomaly():
    return calculated_angles[1]

def get_mean_anomaly():
    return calculated_angles[2]

"""This method takes scalar inputs using
the ctk.CTkEntry variables to set values 
for the three anomalies.
"""
def set_anomalies(e,v,E,m,id):
    
    match id:
        case "True Anomaly":
            # routine 1
            # v is the original angle to transform
            _E = E_ecc_anom(e, v)
            _m = M_kep_eq(e,_E)
            
            set_global_angles(v,_E,_m)
        case "Eccentric Anomaly":
            # print("routine 2")
            # routine 2
            # E is the original angle to transform
            _v = E_to_v(e,E)
            _m = M_kep_eq(e,E)
           
            set_global_angles(_v,E,_m)

        case "Mean Anomaly":
            # print("routine 3")
            # routine 3
            # M is the original angle to transform
            _E = E_transcendental(e,m)
            _v = E_to_v(e,_E)
            
            set_global_angles(_v,_E,m)


            

def set_global_angles(v,E,m):
    rad_to_deg = 180/np.pi
    calculated_angles[0]=v[0]*rad_to_deg
    calculated_angles[1]=E[0]*rad_to_deg
    calculated_angles[2]=m[0]*rad_to_deg


##-routine 1-##
# take v
# transform to E    ...     v --> E
# transform to m    ...     E --> m
#
##-routine 2-##
# take E
# transform to m    ...     E --> m         
# transform to v    ...     E --> v
#
##-routine 3-##
# take m            
# transform to E    ...     m --> E *
# transform to v    ...     E --> v


### Equations to apply ###--------------------------------------------------

# writing the more straightforward equations first...

# v --> E
def E_ecc_anom(e,v):    # func computes eccentric anomaly given e (eccentricity)
                        # a scalar input, and v (true anomaly) an array input
    
    e_anom = np.ones(len(v))        # create the info array
    
    if e > 1:               # if the orbit is hyperbolic, return zeros
        e_anom = np.zeros(len(v))   
    
    else:                   # if the orbit is parabolic, or elliptical
        for angle in range(0,len(v)):   # iterate over the angles of true anomaly given,
            e_anom[angle] =  2*np.arctan( (np.sqrt((1-e)/(1+e)) * np.tan(v[angle]/2)) )
                                        # store the value for E given the angle v,
                                        # append the info array with the value for E
            
            # since this is an arctan function, we do not want the negative 
            # solutions to keep the domain from 0, 2pi.
            
            
            if e_anom[angle]<0:                         # To change the domain from (-pi,pi) --> (0,2pi),
                                                        # add 2pi to all the negative elements
                e_anom[angle]=e_anom[angle]+2*np.pi

    return e_anom       # return the eccentric anomalies for given array of v

# E --> m
def M_kep_eq(e,E):      # func computes mean anomaly given e (ecc.) a scalar,
                        # and E (ecc. anomaly) an array 
    
    M = np.ones(len(E))             # create the info array
    if e > 1:               # if the orbit is hyperbolic, return zeros
        M = np.zeros(len(E))
    else:
        for angle in range(0,len(E)):   # for the angles of ecc. anomaly given,
            M[angle] = E[angle] - e*np.sin(E[angle])
            if M[angle] <= 10**-10:     # append the info array with the kepler equation
                M[angle] = 0
    return M            # return the mean anomalies for given array of E

# E --> v
def E_to_v(e,E):
    v_anom = np.ones(len(E))
    
    if e > 1:               # if the orbit is hyperbolic, return zeros
        v_anom = np.zeros(len(E))
    else:                   # else for parabolic, elliptical, return angles of v
        for angle in range(0,len(v_anom)):
            v_anom[angle] = 2*np.arctan( (np.sqrt((1+e)/(1-e))*np.tan(E[angle]/2)) )
             
            if v_anom[angle]<0:                         # To change the domain from (-pi,pi) --> (0,2pi),
                                                        # add 2pi to all the negative elements
                v_anom[angle]=v_anom[angle]+2*np.pi
    
    return v_anom

# m --> E
def M_to_E(x,e,m):
    eq = (x - e*np.sin(x) - m)
    return eq

# function to find the root of the solution to the transcendental equation
def E_transcendental(e,M):
    ecc_anom = np.ones(len(M))
    for angle in range(0,len(M)):
        ecc_anom[angle] = root(M_to_E,0, args = (e,M[angle])).x[0]
        
    return ecc_anom