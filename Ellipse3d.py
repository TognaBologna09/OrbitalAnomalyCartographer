# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 01:15:21 2021

@author: awgiu
"""
# Purpose of this script is to explain how to rotate ellipses
# in 3 dimensions using the orbital element angles for 3d
# https://www.meccanismocomplesso.org/en/3d-rotations-and-euler-angles-in-python/
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d 

import math as m

# argument of pericenter w
def Rx(theta):
  return np.matrix([[ 1, 0           , 0           ],
                   [ 0, np.cos(theta),-np.sin(theta)],
                   [ 0, np.sin(theta), np.cos(theta)]])
# Ry(i)
def Ry(theta):
  return np.matrix([[ np.cos(theta), 0, np.sin(theta)],
                   [ 0           , 1, 0           ],
                   [-np.sin(theta), 0, np.cos(theta)]])
# Rz(omega)
def Rz(theta):
  return np.matrix([[ np.cos(theta), -np.sin(theta), 0 ],
                   [ np.sin(theta), np.cos(theta) , 0 ],
                   [ 0           , 0            , 1 ]])
# R
def R(theta):
    return np.matrix([[np.cos(theta), -np.sin(theta)],
                      [np.sin(theta), np.cos(theta)]])

### ALTERNATIVE TO EULER ANGLES IS HAMILTONIAN QUATERNIONS ###
# https://www.meccanismocomplesso.org/en/hamiltons-quaternions-and-3d-rotation-with-python/

# phi --> i
# theta --> omega
# psi --> w

def euler_to_quaternion(phi, theta, psi):
 
        qw = m.cos(phi/2) * m.cos(theta/2) * m.cos(psi/2) + m.sin(phi/2) * m.sin(theta/2) * m.sin(psi/2)
        qx = m.sin(phi/2) * m.cos(theta/2) * m.cos(psi/2) - m.cos(phi/2) * m.sin(theta/2) * m.sin(psi/2)
        qy = m.cos(phi/2) * m.sin(theta/2) * m.cos(psi/2) + m.sin(phi/2) * m.cos(theta/2) * m.sin(psi/2)
        qz = m.cos(phi/2) * m.cos(theta/2) * m.sin(psi/2) - m.sin(phi/2) * m.sin(theta/2) * m.cos(psi/2)
 
        return [qw, qx, qy, qz]
    
def q_conjugate(q):
    w, x, y, z = q
    return (w, -x, -y, -z)

def q_mult(q1,q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return w, x, y, z

def qv_mult(q1, v1):
    q2 = (0.0,) +v1
    return q_mult(q_mult(q1,q2), q_conjugate(q1))[1:]

def radial(a,e):
    theta = np.linspace(0,2*np.pi,100)
    p = a*(1-e**2)
    r = p/(1 + e*np.cos(theta))
    return r

inc= np.pi/8
w = 0
omega = 0
 
i_range = np.linspace(-np.pi/2,np.pi/2,24)
omega_range = np.linspace(0,2*np.pi,24)
w_range = np.linspace(0,2*np.pi,24)

q = euler_to_quaternion(w,inc,omega)

vector = (1,0,0)

vector2 = qv_mult(q,vector)
print(vector2)

theta = np.linspace(0,2*np.pi,100)

e = 0.68
a = 1

r = radial(a,e)

x = r*np.cos(theta)
y = r*np.sin(theta)
z = np.zeros(len(theta))

u = []
for i in range(0,len(x)):    
    u.append( (x[i], y[i], z[i]))
ux, uy, uz = zip(*u)

fig = plt.figure(figsize=plt.figaspect(1)*1.5)
ax = plt.axes(projection='3d')

for i in range(0,len([inc])):
    q = euler_to_quaternion(inc,omega,w)
    u_quat = []
    for i in range(0,len(x)):
        u_quat.append(qv_mult(q,u[i]))
        u_quatx, u_quaty, u_quatz = zip(*u_quat)
        
    ax.set_title('Rotated Orbit w/ RGB Cartesian Reference')
    
    ax.plot([1,0],[0,0],[0,0], label='x', color='b')
    ax.plot([0,0],[1,0],[0,0], label='y', color='g')
    ax.plot([0,0],[0,0],[1,0], label='z', color='r')

    ax.plot(ux,uy,uz, color='black', label = 'Flat orbit')
    ax.plot(u_quatx,u_quaty,u_quatz,color='orange', label = 'Rotated orbit')
    
    ax.legend(loc = 'upper right')
    
    plt.show()
