import mysql.connector as mysql
from cartographer_tools import object_manager as om
#region sql backend

def generate_solar_planets():
    
    cnx = mysql.connect(user='public', password='password',
                            host='localhost',
                            database='orbital_objects')
    with cnx.cursor() as cursor:

            cursor.execute("SELECT * FROM solar_planets")

            rows = cursor.fetchall()

            for rows in rows:
                if rows[0] == "Sun":
                    pass
                else:
                    # om.generate_object(name, 
                    #                   color, 
                    #                   size, 
                    #                   a, 
                    #                   e, 
                    #                   theta_o, 
                    #                   i, 
                    #                   omega)
                    om.generate_object(rows[0], 
                                       rows[1], 
                                       rows[7], 
                                       rows[2], 
                                       rows[3], 
                                       rows[4], 
                                       rows[5], 
                                       rows[6])

    cnx.close()
    return

def generate_terrestrial_planets():

    cnx = mysql.connect(user='public', password='password',
                            host='localhost',
                            database='orbital_objects')
    with cnx.cursor() as cursor:

            cursor.execute("SELECT * FROM solar_planets where semimajor_axis < 2")

            rows = cursor.fetchall()

            for rows in rows:
                if rows[0] == "Sun":
                    pass
                else:
                    om.generate_object(rows[0], rows[1], rows[7], rows[2], rows[3], rows[4], rows[5], rows[6])

    cnx.close()
    return

def generate_jovian_planets():

    cnx = mysql.connect(user='public', password='password',
                            host='localhost',
                            database='orbital_objects')
    with cnx.cursor() as cursor:

            cursor.execute("SELECT * FROM solar_planets WHERE semimajor_axis > 2 ")

            rows = cursor.fetchall()

            for rows in rows:

                om.generate_object(rows[0], rows[1], rows[7], rows[2], rows[3], rows[4], rows[5], rows[6])
    cnx.close()
    return

#endregion