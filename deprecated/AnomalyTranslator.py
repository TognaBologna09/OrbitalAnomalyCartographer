# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 04:19:45 2021

@author: awgiu
"""
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

import numpy as np

plt.style.use('ggplot')
# Anomaly Translator
#
# Homework 7 for ASTR 450
# Anthony Giuffre

### METHODS ###

##-purpose-##
# this script is meant to translate between the three orbital anomalies, given
# any one of the three. 
#
# There are three possible cases:
#   i.)     given v, find E,m
#   ii.)    given E, find v,m
#   iii.)   given m, find v,E
#
#   *The third case is the trickiest to implement, since it involves the 
#   transcendental equation to solve for E given a constant m. 
#
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

# radial equation for an elliptic orbit
def radial(a,e,v):  # a function taking scalar a, e, with an array of v to solve for r
    p = a*(1-e**2)
    r = np.ones(len(v))
    for angle in range(0,len(v)):
        r[angle] = p / (1 + e*np.cos(v[angle]))
    
    x_radial = np.multiply(r,np.cos(v))
    y_radial = np.multiply(r,np.sin(v))
    
    return r

# the equation for r given E
def radial_ecc(a,e,E):  # this function takes scalar a, e, and an array of E
    r = np.ones(len(E))
    for angle in range(0,len(E)):
        r[angle] = 1 - e*np.cos(E[angle])
    
    return r

# the eccentric circle in cartesian coordinates
def ecc_circle_cart(a,e,v): # this function takes scalar a, e, and an array of v
    x = np.linspace(-2*a,a,len(v))      # x basis with length of input array
    y = np.linspace(-2*a,a,len(v))      # y basis 
                            
    X,Y = np.meshgrid(x,y)              # creating a mesh
    
    F = (X+e)**2 + (Y)**2 - 1           # equation of the eccentric circle, with center 
                                        # at the center of the radial equation's ellipse
    F_a = np.array(F)                       # numpy array
    F_a = F_a.reshape((len(x),len(y)))      # reshape the array
                            
    fig = plt.figure(figsize=(12,6))    # figure
    h = plt.contour(X,Y,F_a)            # plot
    plt.show()



# Writing a set of two functions to solve the transcendental equation for E given m

from scipy.optimize import root

# function of the solution to the transcendental equation given an angle M
def M_to_E(x,e,m):
    eq = (x - e*np.sin(x) - m)
    return eq

# function to find the root of the solution to the transcendental equation
def E_transcendental(e,M):
    ecc_anom = np.ones(len(M))
    for angle in range(0,len(M)):
        ecc_anom[angle] = root(M_to_E,0, args = (e,M[angle])).x[0]
        
    return ecc_anom

def EccentricInputCollection():
    try:
        n00 = input('\nWhat is the eccentricity of the orbit? \t(in decimals) : ')
        e = float(n00)
       
        if e >= 1:
            
            raise ValueError('Value is too eccentric! The orbit is hyperbolic and will not properly plot. \n...\nPlease input a new value between [0,1)')
        elif e<0 :
            raise ValueError('Value must be non-negative. \n...')
        
    except ValueError:
        print('\nPlease input a new value between [0,1)')
        EccentricInputCollection()
            
    return e

### The Three Routines ###

def v_AnomalyTranslator(e,v):  
    " function takes two float inputs for the eccentricity e "
    " and true anomaly v. It returns the other two anomalies "
    " in the form (v,E,m)"
    
    "How to use the outputs of the function:        "
    "E_AnomalyTranslator()[0] returns v             "
    "E_AnomalyTranslator()[1] returns E             "
    "E_AnomalyTranslator()[2] returns m             "
    "E_AnomalyTranslator()[3] returns (v,E,m)       "
    
    angle_v = float(v)
    angle_E = float(E_ecc_anom(e,[angle_v]))
    angle_m = float(M_kep_eq(e,[angle_E]))
            
    
    a = [angle_v, float("{:.5f}".format(angle_E)),float("{:.5f}".format(angle_m)) ]
    b = 'The array (v, E, m) given v = '+str(angle_v)+' is... \n['+str(a[0])+', '+str(a[1])+', '+str(a[2])+']'
    c = [angle_v, float("{:.5f}".format(angle_E)),float("{:.5f}".format(angle_m)), b]
    return c
 
def E_AnomalyTranslator(e,E): 
    " This function takes two float inputs for the "
    " eccentricity e and eccentric anomaly E, and returns"
    " the other two anomalies (v,E,m)"
    
    "How to use the outputs of the function:        "
    "E_AnomalyTranslator()[0] returns v             "
    "E_AnomalyTranslator()[1] returns E             "
    "E_AnomalyTranslator()[2] returns m             "
    "E_AnomalyTranslator()[3] returns (v,E,m)       "
    angle_E = float(E)
    angle_v = float(E_to_v(e,[angle_E]))
    angle_m = float(M_kep_eq(e,[angle_E]))
            
    
    a = [float("{:.5f}".format(angle_v)), angle_E, float("{:.5f}".format(angle_m))]
    b = 'The array (v, E, m) given E = '+str(E)+' is... \n['+str(a[0])+', '+str(a[1])+', '+str(a[2])+']'
    c = [float("{:.5f}".format(angle_v)), angle_E, float("{:.5f}".format(angle_m)), b]
    return c

def m_AnomalyTranslator(e,m):
    " This function takes two float inputs for the "
    " eccentricity e and mean anomaly m, and returns "
    " the other two anomalies (v,E,m)"
    
    "How to use the outputs of the function:        "
    "m_AnomalyTranslator()[0] returns v             "
    "m_AnomalyTranslator()[1] returns E             "
    "m_AnomalyTranslator()[2] returns m             "
    "m_AnomalyTranslator()[3] returns (v,E,m)       "
    angle_m = float(m)
    angle_E = float(E_transcendental(e,[angle_m]))  # m-->E equation from routine 3
    angle_v = float(E_to_v(e,[angle_E]))
    
    a = [float("{:.5f}".format(angle_v)), float("{:.5f}".format(angle_E)), angle_m]
    b = 'The array (v, E, m) given m = '+str(m)+' is... \n['+str(a[0])+', '+str(a[1])+', '+str(a[2])+']'
    c = [float("{:.5f}".format(angle_v)), float("{:.5f}".format(angle_E)), angle_m, b]    
    return c 


### A way to graphically represent these functions ###
       
def Anomaly_Cartographer():
    "This function uses the semi-major axis, eccentricity, and an array of    " 
    "mean anomalies to graphically represent all three anomalies. The function"
    "will prompt the user to input a value for v in decimals which will draw  "
    "a line to a position along the respective curve marking the angle of the "
    "true, eccentric, and mean anomalies.                                     "

    "Equations used in the function:    "
    "radial(a,e,v)                      "
    "E_ecc_anom(e,v)                    "
    "M_kep_eq(e,E)                      "

## Creating variables for use with functions ##
    v = np.linspace(0,2*np.pi,2000)
    

    while True:
        
## Asking for user input variable a for the semi-major axis ##-----------------
        n000= input('\nWhat is the value for the semi-major axis? : ')
        a = float(n000)
        
## Creating the shape for the eccentric circle given the orbital elements ##
    
        x = np.linspace(-2*a,a,len(v))    # cartesian x, and y arrays of length
        y = np.linspace(-2*a,a,len(v))    # equal to the input angle array
    
        X,Y = np.meshgrid(x,y)   # using meshgrid-->contour plot
    

## Asking for user input variable e for the eccentricity ##--------------------
        
        e = EccentricInputCollection()
        
       
        F_eccentric = (X+e)**2 + (Y)**2 - 1     # contour equation of ellipse equal 0
        F_E = np.array(F_eccentric)
        F_E = F_E.reshape( (len(x),len(y)) )
  
## Creating the shape for the elliptical orbit given the radial equation ##----
   
        r = radial(a,e,v)   # array of r using the radial equation 
                                
        # E = E_ecc_anom(e,v) # array of E using the eccentric anomaly equation (v-->E)
        
        # M = M_kep_eq(e,E)   # array of M using the kepler equation (E-->m)
            
## Variables to establish cartesian origins and symmetries ##------------------

        center_ellipse_x = -a*e     # center of ellipse, x coord
        p_focus_ellipse_x  = 0      # focus of ellipse, x coord
        center_ellipse_y = 0        # center of ellipse, y coord
        
        x_radial = np.multiply(r,np.cos(v)) # cartesian x,y of radial eqn
        y_radial = np.multiply(r,np.sin(v))

        # x_ecc = np.multiply(1,np.cos(E))-a*e    # cartesian x,y of ecc. circle
        # y_ecc = np.multiply(1,np.sin(E))        # with center at (-ae,0)   
        
        # x_m = np.multiply(1, np.cos(M))-a*e     # cartesian x,y using the
        # y_m = np.multiply(1, np.sin(M))         # mean anomaly, center (-ae,0)
        
        # x_ecc_rad_vector = x_radial
        # y_ecc_rad_vector = y_ecc - y_radial
        
    
## Choosing an angle to mark on the graph ##-----------------------------------
    
        # #true_anom_test = input('Input a value for the true anomaly in decimals \nto mark the position of the orbit.  : ') 
        # true_anom_test = input('Input a value for the true anomaly in decimals \nto mark the position of the orbit. : ')
        
        # # M_choice = float(mean_anom_test)
        # # E_choice = m_AnomalyTranslator(e,[M_choice])[1]  # m-->E equation from routine 3
        # # v_choice = m_AnomalyTranslator(e,[_choice])[0]  # E-->v equation from routine 3
        # v_choice = float(true_anom_test)         # storing the value
        # E_choice = float(E_ecc_anom(e,[v_choice]))   # v-->E
        # M_choice = float(M_kep_eq(e,[E_choice]))    # E-->m
        
        "A plot"
        # a figure for graphing
        fig = plt.figure(figsize=(9, 9))
        ax = plt.axes()
        
        "Plotting the radial equation"
        # the ellipse is plotted using radial equation in cartesian form 
        ax.plot(x_radial,y_radial, label='Ellipse',color='blue')   
        
        
        "Plotting the eccentric circle"
        # the eccentric circle is plotted using a contour plot
        ecc_cir = ax.contour(a*X,a*Y,F_eccentric,[0],colors ='orange')
        
        #-------------------------------------------------------------------------#
        y='y'
        n='n'
        
        print('\n... notice ... possible input angles from [0, 2pi]\n')
        n0 = input('What angle do you have? \t(v/E/m) : ')
        
        v = 'v'
        E = 'E'
        m = 'm'
        if n0 == v:
            print('... ... ...')
            n0a = input('What is the value of the true anomaly? (as a decimal in rad) : ')
            
            angle_v = float(n0a)
            print(v_AnomalyTranslator(e,angle_v)[3])
            
            v_choice = angle_v
            E_choice = v_AnomalyTranslator(e,angle_v)[1]
            M_choice = v_AnomalyTranslator(e,angle_v)[2]

            "Plotting a line for the eccentric anomaly"
            # and a line is drawn using the E_angle from v using the converter, and distance formula
            ecc_cir_vector = ax.plot([np.multiply(a,a*np.cos(E_choice))-a*e,center_ellipse_x],[np.multiply(a,np.sin(E_choice)),0], color= 'darkorange', label='Eccentric Anomaly r Vector')
            # ecc_cir_vector = plt.plot([ a*cos(E), -2ae ],[a*sin(E), 0])
            
            "Plotting a line for the mean anomaly"
            # and a line is drawn out using the mean anomaly
            m_vector = ax.plot([np.multiply(a, np.cos(M_choice))-a*e,center_ellipse_x],[np.multiply(a, np.sin(M_choice)),center_ellipse_y], color ='red', label='Mean Anomaly r Vector')
            
            "Plotting the line connecting the radial equation to the eccentric circle"
            # a final line to connect the ellipse to the eccentric circle
            ecc_rad_vector = ax.plot([np.multiply(radial(a,e,[v_choice])[0],np.cos(v_choice)), np.multiply(radial(a,e,[v_choice])[0], np.cos(v_choice))],[a*np.sin(E_choice), np.multiply(radial(a,e,[v_choice])[0], np.sin(v_choice))], color = 'purple', label='Line connecting Ell.->Ecc.')
        
            "Plotting a line for the true anomaly"
            # and a line is drawn using the angle of choice using the distance formula
            rad_ell_vector = ax.plot( [p_focus_ellipse_x, np.multiply(radial(a,e,[v_choice])[0],np.cos(v_choice) )],[center_ellipse_y,np.multiply(radial(a,e,[v_choice])[0],np.sin(v_choice)) ], color= 'royalblue', label='True Anomaly r Vector')
            
            # setting limits, title, gridlines
            plt.title('graph of elliptical orbit and eccentric circle, \n(a,e,v): ('+str(a)+','+str(e)+','+str(v_choice)+')')
            plt.xlim(-2*a,1*a)
            plt.ylim(-2*a,1.5*a)
            
            plt.legend(loc= 'lower right')
            plt.show()
            
            v_E_M = '(v,E,m)'+' : '+'('+str(v_choice)+', '+str(float("{:.4f}".format(E_choice)))+', '+str(float("{:.4f}".format(M_choice)))+')'
            return v_E_M
                            
            n0b = input('Do you want to test new parameters? (y/n) : ')
            if n0b==y:
               print('\n... ... ...') 
            elif n0b==n:
                break
        
        elif n0 == E:
            print ('... ... ...')
            n0b = input('What is the value of the eccentric anomaly? (as a decimal in rad) : ')
            
            angle_E = float(n0b)
            print(E_AnomalyTranslator(e,angle_E)[3])
            
            v_choice = E_AnomalyTranslator(e,angle_E)[0]
            E_choice = angle_E
            M_choice = E_AnomalyTranslator(e,angle_E)[2]

            "Plotting a line for the eccentric anomaly"
            # and a line is drawn using the E_angle from v using the converter, and distance formula
            ecc_cir_vector = ax.plot([np.multiply(a,a*np.cos(E_choice))-a*e,center_ellipse_x],[np.multiply(a,np.sin(E_choice)),0], color= 'darkorange', label='Eccentric Anomaly r Vector')
            # ecc_cir_vector = plt.plot([ a*cos(E), -2ae ],[a*sin(E), 0])
            
            "Plotting a line for the mean anomaly"
            # and a line is drawn out using the mean anomaly
            m_vector = ax.plot([np.multiply(a, np.cos(M_choice))-a*e,center_ellipse_x],[np.multiply(a, np.sin(M_choice)),center_ellipse_y], color ='red', label='Mean Anomaly r Vector')
            
            "Plotting the line connecting the radial equation to the eccentric circle"
            # a final line to connect the ellipse to the eccentric circle
            ecc_rad_vector = ax.plot([np.multiply(radial(a,e,[v_choice])[0],np.cos(v_choice)), np.multiply(radial(a,e,[v_choice])[0], np.cos(v_choice))],[a*np.sin(E_choice), np.multiply(radial(a,e,[v_choice])[0], np.sin(v_choice))], color = 'purple', label='Line connecting Ell.->Ecc.')
        
            "Plotting a line for the true anomaly"
            # and a line is drawn using the angle of choice using the distance formula
            rad_ell_vector = ax.plot( [p_focus_ellipse_x, np.multiply(radial(a,e,[v_choice])[0],np.cos(v_choice) )],[center_ellipse_y,np.multiply(radial(a,e,[v_choice])[0],np.sin(v_choice)) ], color= 'royalblue', label='True Anomaly r Vector')
            
            # setting limits, title, gridlines
            plt.title('graph of elliptical orbit and eccentric circle, \n(a,e,E): ('+str(a)+','+str(e)+','+str(E_choice)+')')
            plt.xlim(-2*a,1*a)
            plt.ylim(-2*a,1.5*a)
               
            plt.legend(loc= 'lower right')
            plt.show()
            
            v_E_M = '(v,E,m)'+' : '+'('+str(v_choice)+', '+str(float("{:.4f}".format(E_choice)))+', '+str(float("{:.4f}".format(M_choice)))+')'
            return v_E_M
            
            n0b = input('Do you want to test new parameters? (y/n) : ')
            if n0b==y:
               print('\n... ... ...') 
            elif n0b==n:
                break
        
        elif n0 == m:
            print('... ... ...')
            n0c = input('What is the value of the mean anomaly? (as a decimal in rad) : ')
            
            angle_m = float(n0c)
            print(m_AnomalyTranslator(e,angle_m)[3])
            
            v_choice = m_AnomalyTranslator(e,angle_m)[0]
            E_choice = m_AnomalyTranslator(e,angle_m)[1]
            M_choice = angle_m

            "Plotting a line for the eccentric anomaly"
            # and a line is drawn using the E_angle from v using the converter, and distance formula
            ecc_cir_vector = ax.plot([np.multiply(a,a*np.cos(E_choice))-a*e,center_ellipse_x],[np.multiply(a,np.sin(E_choice)),0], color= 'darkorange', label='Eccentric Anomaly r Vector')
            # ecc_cir_vector = plt.plot([ a*cos(E), -2ae ],[a*sin(E), 0])
            
            "Plotting a line for the mean anomaly"
            # and a line is drawn out using the mean anomaly
            m_vector = ax.plot([np.multiply(a, np.cos(M_choice))-a*e,center_ellipse_x],[np.multiply(a, np.sin(M_choice)),center_ellipse_y], color ='red', label='Mean Anomaly r Vector')
            
            "Plotting the line connecting the radial equation to the eccentric circle"
            # a final line to connect the ellipse to the eccentric circle
            ecc_rad_vector = ax.plot([np.multiply(radial(a,e,[v_choice])[0],np.cos(v_choice)), np.multiply(radial(a,e,[v_choice])[0], np.cos(v_choice))],[a*np.sin(E_choice), np.multiply(radial(a,e,[v_choice])[0], np.sin(v_choice))], color = 'purple', label='Line connecting Ell.->Ecc.')
        
            "Plotting a line for the true anomaly"
            # and a line is drawn using the angle of choice using the distance formula
            rad_ell_vector = ax.plot( [p_focus_ellipse_x, np.multiply(radial(a,e,[v_choice])[0],np.cos(v_choice) )],[center_ellipse_y,np.multiply(radial(a,e,[v_choice])[0],np.sin(v_choice)) ], color= 'royalblue', label='True Anomaly r Vector')
            
            # setting limits, title, gridlines
            plt.title('graph of elliptical orbit and eccentric circle, \n(a,e,m): ('+str(a)+','+str(e)+','+str(M_choice)+')')
            plt.xlim(-2*a,1*a)
            plt.ylim(-2*a,1.5*a)
            
            plt.legend(loc= 'lower right')
            plt.show()
            
            v_E_M = '(v,E,m)'+' : '+'('+str(v_choice)+', '+str(float("{:.4f}".format(E_choice)))+', '+str(float("{:.4f}".format(M_choice)))+')'
            return v_E_M
            
            n0b = input('Do you want to test new parameters? (y/n) : ')
            if n0b==y:
               print('\n... ... ...\n') 
            elif n0b==n:
                break
        
            else:
                print('character not recognized')
       
### r1,r2.Using Equations ###----------------------------------------------------
# (writing variables)

a=1
u=1
P = 2*np.pi*(a**3/u)**(1/2)

ecc      = 0.8
theta    = np.arange(0,2*np.pi,np.pi/1000)

Ecc_angles = E_ecc_anom(ecc,theta)          # v-->E

M_angles = M_kep_eq(ecc,Ecc_angles)         # E-->M


### Plotting the three anomalies ###-------------------------------------------

def AnomalyPlots():
    while True:
        print('For extra credit!')
        n1 = input('Would you like to see a plot of the three anomalies? (y/n) : ')
        y='y'
        n='n'
        if n1 == y:
            
            fig = plt.figure(figsize=(12,6))
    
            plt.title('True Anomaly, Eccentric Anomaly, Mean Anomaly')
            plt.ylabel('Angle of \nanomaly', rotation = 0)
            plt.xlabel('Angle from 0 to 2pi')
            plt.xlim(-0.05,2*np.pi+0.05)
            
            plt.plot(theta,theta,'b', label='v')
            plt.plot(theta,Ecc_angles,'g', label='E')
            plt.plot(theta,M_angles,'r', label='M')
            
            
            dl = 0.2
            lw = 3
            
            plt.plot( np.zeros( len(theta) ), np.linspace(-dl, dl, len(theta) ), color = 'black', linewidth = lw, label='theta = 0')
            plt.plot( np.multiply(np.pi, np.ones( len(theta) )), np.linspace(np.pi-dl,np.pi+dl, len(theta) ), color = 'black', linestyle='solid', linewidth = lw, label='theta = pi')
            plt.plot( np.multiply(2*np.pi, np.ones( len(theta) )), np.linspace(2*np.pi - dl, 2*np.pi + dl, len(theta)) ,color = 'black', linestyle='solid', linewidth = lw,label='theta = 2pi') 
            
            
            plt.legend(loc='upper left')
    
            #####
            n2 = input('Would you like to see a graph of M-v? (y/n) : ')
            if n2 == y:
                fig = plt.figure(figsize=(12,6))
            
                plt.title('M-v')
                plt.xlabel('0 to 2pi')
                plt.ylabel('M-v')
            
                plt.plot(theta,M_angles-theta,color='red', label='M-v')
                plt.plot(theta, np.zeros(len(theta)), color='black', label='y = 0')
                plt.legend()
                print('\nThese graphs represent the angles where v=E=M,\nand the inequal relationships between the angles.')
                break
            elif n2 == n:
                print('... ... ...')
                break
            else:
                print('character not recognized')
        elif n1 == n:
            print('... ... ...\nGoodbye!')
            break
        else:
            print('character not recognized')
        break 


### Testing Functions of routine 1 ###-----------------------------------------
# 
# Conditions to test:
# --boundaries
# v,E,M = 0 when  v = 0
# v,E,M = pi when v = pi
# -- eccentricity for circle
# v = E = M for e = 0
# -- for an ellipse 
#   for 0 < e < 1...
# v >= E >= M for [0,pi] 
# v <= E <= M for [pi,2pi]

# --testing the prewritten functions
# print('\nTesting functions from routine 1: \n')
# print('\tIf v = 0, then E,m should equal 0. \n ::: v-E = 0 --> ' + str(theta[0]-Ecc_angles[0]) )
# print('\tIf v = pi, then E,m should equal pi. \n ::: v(pi)-E = 0 --> ' +str( round(theta[int(len(theta)/2)]-Ecc_angles[int(len(theta)/2)] )) )

# print('\n\tFrom [0,pi], v >= E >= M.')
# print('\n\tFrom [pi,2pi], v <= E <= M.')
# print('\nThese relationships are also visible with the graph of the three anomalies')

### Begin: Routine 3 ###

# take a test value...
# M = np.pi/2

# this angle m is a constant for the transcendental equation  
# intersect = M_angles - np.pi/2
# and this array ('intersect') can be shown on a graph to represent the solution
# for i in range(0,len(intersect)):
#     val = intersect[i]**2           # squared normalization --> making values positive
#     if val <= 10**(-4):             # if the value is small,
#         print(M_angles[i])          # show the M_angle that satisfies


" Writing User-end Console programs "###---------------------------------------

"       Anomaly Translator      "
"   uses functions:             "
"                               "
"       --v_AnomalyTranslator   "
"           -E_ecc_anom         " # v-->E
"           -M_kep_eq           " # E-->m
"                               "
"       --E_AnomalyTranslator   "
"           -E_to_v             " # E-->v
"           -M_kep_eq           " # E-->m
"                               "
"       --m_AnomalyTranslator   "
"           -M_to_E             " # m-->E
"           -E_transcendental   " # m-->E
"           -E_to_v             " # E-->v
    
def AnomalyTranslator():
    print('\nWelcome to the Anomaly Translator: Follow the prompts to translate orbital angles!')
    print('\nYou will be asked to input two values in order to accurately translate angles.')
    print('\nThe first value is the eccentricity, and the second value is your angle of choice\nexpressed as a decimal in units of radians. ')
    y='y'
    n='n'
    
    while True:

        e = EccentricInputCollection()
        # n00 = input('\nWhat is the eccentricity of the orbit? \t(in decimals) : ')
        # e = float(n00)
        
        print('\n... notice ... possible input angles from [0, 2pi]\n')
        n0 = input('What angle do you have? \t(v/E/m) : ')
        
        v = 'v'
        E = 'E'
        m = 'm'
        if n0 == v:
            print('... ... ...')
            n0a = input('What is the value of the true anomaly? (as a decimal in rad) : ')
            
            angle_v = float(n0a)
            print(v_AnomalyTranslator(e,angle_v)[3])
            
            n0b = input('Do you want to test new parameters? (y/n) : ')
            if n0b==y:
               print('\n... ... ...') 
            elif n0b==n:
                break
        
        elif n0 == E:
            print ('... ... ...')
            n0b = input('What is the value of the eccentric anomaly? (as a decimal in rad) : ')
            
            angle_E = float(n0b)
            print(E_AnomalyTranslator(e,angle_E)[3])
            
            n0b = input('Do you want to test new parameters? (y/n) : ')
            if n0b==y:
               print('\n... ... ...') 
            elif n0b==n:
                break
        
        elif n0 == m:
            print('... ... ...')
            n0c = input('What is the value of the mean anomaly? (as a decimal in rad) : ')
            
            angle_m = float(n0c)
            print(m_AnomalyTranslator(e,angle_m)[3])
            
            n0b = input('Do you want to test new parameters? (y/n) : ')
            if n0b==y:
               print('\n... ... ...\n') 
            elif n0b==n:
                break
        print('\n... ... ...\nDone.\n')
        break
    
    else:
        print('character not recognized')


"       Anomaly Cartographer    "
"   uses functions:             "
"                               "
"       --v_AnomalyTranslator   "
"           -E_ecc_anom         " # v-->E
"           -M_kep_eq           " # E-->m
"                               "
"       --E_AnomalyTranslator   "
"           -E_to_v             " # E-->v
"           -M_kep_eq           " # E-->m
"                               "
"       --m_AnomalyTranslator   "
"           -M_to_E             " # m-->E
"           -E_transcendental   " # m-->E
"           -E_to_v             " # E-->v
"                               "
"       --radial_eq             " # ellipse equation

def AnomalyCartographer():
        
    while True:
        print('\nWelcome to the Anomaly Cartographer: Follow the prompts to graph an orbit!')
        n2 = input('Do you wish to continue and use the Cartographer? (y/n) : ')
        y='y'
        n='n'
        
        theta = np.linspace(0,2*np.pi,2000)
        
        if n2 ==n:
            print('Goodbye!')
            break
        elif n2 ==y:
            while True:
                    
                map = Anomaly_Cartographer()
                print(map)

                n2b = input('Do you want to see another graph? (y/n) : ')
                if n2b ==n:
                    print('Goodbye!')
                    
                    break
                elif n2b ==y:
                    print('\n... ... ...\n')
            break
            
        else:
            print('character not recognized')
        
#AnomalyTranslator()
AnomalyCartographer()
#AnomalyPlots()




