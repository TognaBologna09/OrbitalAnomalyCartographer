from celestial_classes import celestial_object as co 

celestial_objects = []      # global object list

def generate_object(name, color, size, a, e, v, i, w):
    
    if any(x.name == name for x in celestial_objects):

        for y in celestial_objects:
            print("name to remove: " + name + ", current name is " + y.name)
            if (y.name == name):
                print("removing " + y.name + " from the list, and overwriting")
                celestial_objects.remove(y)
                break

        celestial_objects.append(co.CelestialObject(name, color, size, a, e, v, i, w))
        
        
    else:
        celestial_objects.append(co.CelestialObject(name, color, size, a, e, v, i, w))
    return

def get_celestial_objects():
    return celestial_objects

def clear_celestial_objects():
    celestial_objects.clear()
    return

#endregion


   