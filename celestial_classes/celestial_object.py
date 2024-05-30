import numpy as np
import math as m

class Vector3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def set_vector3_array(self, ux,uy,uz):
        self.x = ux
        self.y = uy
        self.z = uz

class CelestialObject(Vector3):
    
 
    theta = np.linspace(0,2*np.pi,2000)

    r = np.ones(len(theta))
    
    degree_per_day = 0 
    period = 0

    # psi is longitude of asc. node, labeled psi for quaternion equation
    def __init__(self, name, color, size, semimajor_axis, eccentricity, initial_angle, inclination, omega):
        self.name =  name
        self.color = color
        self.size = size
        self.semimajor_axis = float(semimajor_axis)
        self.eccentricity = float(eccentricity)
        self.initial_angle = float(initial_angle)*np.pi/180
        self.inclination = float(inclination)*np.pi/180
        self.omega = float(omega)*np.pi/180

        rx,ry,rz = self.rotate_radial(self.theta)
        self.set_vector3_array(rx,ry,rz)

        self.kepler()
        self.set_deg_per_day()
        
    
    def kepler(self):
        """ Kepler's 3rd Law: P^2 = a^3"""
        period = np.sqrt(np.power(self.semimajor_axis,3))
        self.period = period
        return 
    

    def set_deg_per_day(self):
        """ Assuming a constant velocity in the orbit,
        this sets the attribute for degrees per day
        using the objects keplerian period and angle
        in degrees.
        """
        value = np.divide(360,365*self.period)
        self.degree_per_day = value
        return 
    

    def radial(self):
        """The radial equation: 
        It plots ellipses, and returns an array of positions 
        in polar coordinates. 
        """
        p = self.semimajor_axis*(1-self.eccentricity**2)
        
        for i in range(0,len(self.theta)):
            iterator = i+int(np.floor(self.initial_angle*1000))
            if iterator > len(self.theta):
                iterator = iterator - len(self.theta)
            angle = self.theta[iterator]
           
            self.r[i] = p / (1 + self.eccentricity*np.cos(angle))
           

        return self.r
    
    
    def radial_scalarAngle(self, angle):
        """ The radial equation:
        The radial equation: Returns a scalar value r 
        in polar coordinates, and takes an input  
        angle in radians.
        """
        p = self.semimajor_axis*(1-self.eccentricity**2)

        rval = (
            p
            / 
            (1 + self.eccentricity*np.cos(angle))
                )
           

        return rval
    

    def radial_to_cart_array(self, angle):
        """ The radial equation:
        The radial equation converted to an array of positions
        in cartesian coordinates (xyz) 
        """
        p = self.semimajor_axis*(1-self.eccentricity**2)
        z_radial = np.zeros(len(angle))
        for i in range(0,len(angle)):  # populate r array for breaking into cartesian components

            self.r[i] = (
                    p 
                    / 
                    (1 + self.eccentricity*np.cos(angle[i]))
                    )

        x_radial = np.multiply(self.r,np.cos(angle))
        y_radial = np.multiply(self.r,np.sin(angle))
        
        return (x_radial,y_radial,z_radial)
    

    def rotate_radial(self,angle):
        """ The radial equation:
        Returns the radial equation as arrays xyz
        with an input array of angles from 0 to 2pi.
        """
        q = self.euler_to_quaternion(0,self.inclination,self.omega)
        u_quat = []
        
        ux,uy,uz = self.radial_to_cart_array(angle)
        u = []
        for i in range(0,len(angle)):  
            u.append((ux[i], uy[i], uz[i]))
            u_quat.append(self.qv_mult(q,u[i]))
            u_quatx, u_quaty, u_quatz = zip(*u_quat)
        return u_quatx, u_quaty, u_quatz

    def euler_to_quaternion(self, phi, theta, psi):
        # phi = 0, theta:inclination, psi = longitude of ascending node 
        qw = np.cos(phi/2) * np.cos(theta/2) * np.cos(psi/2) + np.sin(phi/2) * np.sin(theta/2) * np.sin(psi/2)
        qx = np.sin(phi/2) * np.cos(theta/2) * np.cos(psi/2) - np.cos(phi/2) * np.sin(theta/2) * np.sin(psi/2)
        qy = np.cos(phi/2) * np.sin(theta/2) * np.cos(psi/2) + np.sin(phi/2) * np.cos(theta/2) * np.sin(psi/2)
        qz = np.cos(phi/2) * np.cos(theta/2) * np.sin(psi/2) - np.sin(phi/2) * np.sin(theta/2) * np.cos(psi/2)
 
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
    