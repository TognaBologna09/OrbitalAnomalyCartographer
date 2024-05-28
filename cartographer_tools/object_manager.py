import numpy as np
import math as m

from celestial_classes import celestial_object as co 

celestial_objects = []      # Declare global object list

def generate_object(name, color, size, a, e, v, i, w):
    #any(x.name == "t2" for x in l)
    if any(x.name == name for x in celestial_objects):
        for x in celestial_objects:
            if any(x.name == name for x in celestial_objects):
                celestial_objects.remove(x)
        celestial_objects.append(co.CelestialObject(name, color, size, a, e, v, i, w))
        
        pass
    else:
        celestial_objects.append(co.CelestialObject(name, color, size, a, e, v, i, w))
        
    return

def get_celestial_objects():
    return celestial_objects

def clear_celestial_objects():
    celestial_objects.clear()
    return

#endregion


   