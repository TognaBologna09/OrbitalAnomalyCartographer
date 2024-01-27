import numpy as np
import math as m

class Vector3:

    posx = 0
    posy = 0
    posz = 0
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def SetVector3Array(self, ux,uy,uz):
        self.x = ux
        self.y = uy
        self.z = uz

    def SetVector3(self, nx, ny, nz):
        self.posx = nx
        self.posy = ny
        self.posz = nz

class CelestialObject(Vector3):
    
    psi = 0

    theta = np.linspace(0,2*np.pi,1000)

    r = np.ones(len(theta))
    rx = np.zeros(len(theta))
    ry = np.zeros(len(theta))
    rz = np.zeros(len(theta))

    rx2D = np.zeros(len(theta))
    ry2D = np.zeros(len(theta))
    rz2D = np.zeros(len(theta))

    def __init__(self, name, size, color, semimajor_axis, eccentricity, initial_angle, inclination, omega):
        self.name =  name
        self.size = size
        self.color = color
        self.semimajor_axis = float(semimajor_axis)
        self.eccentricity = float(eccentricity)
        self.initial_angle = float(initial_angle)
        self.inclination = float(inclination)
        self.omega = float(omega)

        rx,ry,rz = self.radial_to_cart_array()
        self.rx2D, self.ry2D, self.rz2D = rx,ry,rz
        
        rx,ry,rz = self.rotate_radial(self.theta)
        self.SetVector3Array(rx,ry,rz)


    def increment_theta_animation(self):
            rx,ry,rz = self.radial_to_cart()
            rx,ry,rz = self.rotate_radial(self.v)
            self.SetVector3(rx,ry,rz)

    def radial(self):
        p = self.semimajor_axis*(1-self.eccentricity**2)
        
        for i in range(0,len(self.theta)):
            iterator = i+int(m.floor(self.initial_angle*1000))
            if iterator > len(self.theta):
                iterator = iterator - len(self.theta)
            angle = self.theta[iterator]
           
            self.r[i] = p / (1 + self.eccentricity*np.cos(angle))
           

        return self.r

    def radial_to_cart_array(self):
        p = self.semimajor_axis*(1-self.eccentricity**2)
        z_radial = np.zeros(len(self.theta))
        for i in range(0,len(self.theta)):  # populate r array for breaking into cartesian components

            # iterator = i+m.floor(self.initial_angle*1000)
            # if iterator > len(self.theta):
            #     iterator = iterator - len(self.theta)
            
            # angle = self.theta[iterator]
            angle = self.theta[i]
            self.r[i] = (
                    p 
                    / 
                    (1 + self.eccentricity*np.cos(angle))
                        )

        x_radial = np.multiply(self.r,np.cos(self.theta))
        y_radial = np.multiply(self.r,np.sin(self.theta))
        
        return (x_radial,y_radial,z_radial)

    def radial_to_cart(self, angle):
        p = self.semimajor_axis*(1-self.eccentricity**2)

        rval = (
            p
            / 
            (1 + self.eccentricity*np.cos(angle))
                )

        x_radial = np.multiply(rval,np.cos(angle))
        y_radial = np.multiply(rval,np.sin(angle))
        
        z_radial = 0

        return (x_radial,y_radial,z_radial)
    
    # phi:omega, theta:inclination, psi = 0 (the other two variables define all the orbital elements)
    def euler_to_quaternion(self):
 
        qw = m.cos(self.omega/2) * m.cos(self.inclination/2) * m.cos(self.psi/2) + m.sin(self.omega/2) * m.sin(self.inclination/2) * m.sin(self.psi/2)
        qx = m.sin(self.omega/2) * m.cos(self.inclination/2) * m.cos(self.psi/2) - m.cos(self.omega/2) * m.sin(self.inclination/2) * m.sin(self.psi/2)
        qy = m.cos(self.omega/2) * m.sin(self.inclination/2) * m.cos(self.psi/2) + m.sin(self.omega/2) * m.cos(self.inclination/2) * m.sin(self.psi/2)
        qz = m.cos(self.omega/2) * m.cos(self.inclination/2) * m.sin(self.psi/2) - m.sin(self.omega/2) * m.sin(self.inclination/2) * m.cos(self.psi/2)
 
        return [qw, qx, qy, qz]
    
    def q_conjugate(self, q):
        w, x, y, z = q
        return (w, -x, -y, -z)

    def q_mult(self, q1,q2):
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2
        w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
        x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
        y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
        z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
        return w, x, y, z

    def qv_mult(self, q1, v1):
        q2 = (0.0,) + v1
        return self.q_mult(self.q_mult(q1,q2), self.q_conjugate(q1))[1:]
    
    def rotate_radial(self,angle):
        q = self.euler_to_quaternion()
        u_quat = []
        
        ux,uy,uz = self.radial_to_cart_array()
        u = []
        for i in range(0,len(angle)):  
            u.append((ux[i], uy[i], uz[i]))
            u_quat.append(self.qv_mult(q,u[i]))
            u_quatx, u_quaty, u_quatz = zip(*u_quat)
        return u_quatx, u_quaty, u_quatz
    
    def rotate_radial_scalarAngle(self, angle):
        q = self.euler_to_quaternion()
        u_quat = []
        
        ux,uy,uz = self.radial_to_cart(angle)
        u = []
        u.append((ux, uy, uz))
        u_quat.append(self.qv_mult(q,u[0]))
        u_quatx, u_quaty, u_quatz = zip(*u_quat)
        return u_quatx, u_quaty, u_quatz
    
    def orbit_vector_scalar(self, angle):
        a,b,c = self.rotate_radial_scalarAngle(angle)
        self.posx, self.posy, self.posz = a,b,c
        return self.posx,self.posy,self.posz

test1 = CelestialObject("earf",1,'blue', 1, 0.05, 0, 1.0, 0)
# value = np.zeros(1)
# for i in range(0,10):
#     test1.increment_theta()

    
# x,y,z = test1.radial_to_cart()
# test1.SetVector3Array(x,y,z)
# print(test1.x[:10])

# print(x,y,z)
# u = []
# q = test1.euler_to_quaternion()
# for i in range(0,len(test1.theta)):  
#     u.append((x[i], y[i], z[i]))
#     print(test1.qv_mult(q,u[i]))


celestial_objects = [test1]

def GenerateObject(name, size, color, a, e, v, i, w):
    celestial_objects.append(CelestialObject(name, size, color, a, e, v, i, w))
    return

def GetCelestialObjects():
    return celestial_objects

def ClearCelestialObjects():
    celestial_objects.clear()
    return


# SetOrbits()

# print(zip(*celestial_objects_r_vectors))