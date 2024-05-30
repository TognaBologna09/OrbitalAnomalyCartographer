
"""Welcome to the OrbitalAnomalyCartographer"""

# For essential math
import numpy as np

# Plotting
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib import style

# GUI libraries
import customtkinter as ctk
import tkinter as tk
import CTkListbox as CTkL

# Custom Libraries 
from cartographer_tools import object_manager as om 
from cartographer_tools import angle_calculator as ac 
from cartographer_tools import plot_manager as pm

from sql_utilities import mysql_celestial_ingester as mysql_c_i


class Window(ctk.CTkFrame):

    def __init__(self, master = None, resolution="1280x720"):
        style.use("dark_background")
        ctk.CTkFrame.__init__(self, master)
        self.master = master
        self.resolution = resolution
        self.init_window()

        # global list to store 
        # the selected object 
        # from tkinter gui
        self.selected_id = []

    
#region frontend facing GUI
                
    def init_tabs(self):
        self.tabview = ctk.CTkTabview(master = app, height = 690, width =250)
        self.tabview.place(x=1010,y=10)

    #region calculator tab
    def init_tab_calc(self):


        self.tab_calculator = self.tabview.add("Calculator")

        tutorial = """~~~~~~IMPORTANT~~~~~~ \n\nInput angles in units of degrees"""

        self.calc_tutorial_textbox = ctk.CTkTextbox(master = self.tab_calculator, width=205, state='disabled', height = 70, fg_color="gray14")
        self.calc_tutorial_textbox.configure(state="normal")
        self.calc_tutorial_textbox.insert('end', tutorial)
        self.calc_tutorial_textbox.configure(state="disabled")
        self.calc_tutorial_textbox.place(x=10,y=5)

        anomalies = "Eccentric Anomaly \n\nMean Anomaly"

        self.calc_anomalies_textbox = ctk.CTkTextbox(master=self.tab_calculator, width=145, state='disabled',height = 70, fg_color="gray17")
        self.calc_anomalies_textbox.configure(state='normal')
        self.calc_anomalies_textbox.insert('end', anomalies)
        self.calc_anomalies_textbox.configure(state='disabled')
        self.calc_anomalies_textbox.place(x=70,y=210)

 
        calc_parameters_label = ctk.CTkLabel(master = self.tab_calculator, text = "Orbital Angle Calculator", width = 205, fg_color="#1f538d", corner_radius = 10, height=30)
        calc_parameters_label.place(x=10, y=90)
        

        calc_eccentricity_label = ctk.CTkLabel(master = self.tab_calculator, text = "Eccentricity")
        calc_eccentricity_label_units = ctk.CTkLabel(master = self.tab_calculator, text = "[0.0, 1.0)")
        self.calc_eccentricity_var = ctk.DoubleVar(master = self.tab_calculator)
        self.calc_eccentricity_entry = ctk.CTkEntry(master = self.tab_calculator, textvariable=self.calc_eccentricity_var,width = 55)
        calc_eccentricity_label.place(x=70, y=130)
        calc_eccentricity_label_units.place(x=170,y=130)
        self.calc_eccentricity_entry.place(x=10, y=130)


        self.calc_angleParameters_var = ctk.DoubleVar(master = self.tab_calculator)
        self.calc_angleParameters_entry = ctk.CTkEntry(master = self.tab_calculator, textvariable=self.calc_angleParameters_var, width=55)
        self.calc_angleParameters_var.trace_add(mode='write', callback=self.calc_callback)
        self.calc_angleParameters_label = ctk.CTkComboBox(master = self.tab_calculator, values=["True Anomaly","Eccentric Anomaly","Mean Anomaly"], width = 150, fg_color="#1f538d", corner_radius = 10, height=30)
        self.calc_angleParameters_label.place(x=70, y=170)
        self.calc_angleParameters_entry.place(x=10,y=170)


        self.calc_angleParameters_var_two = ctk.DoubleVar(master = self.tab_calculator, value=0.0)
        self.calc_angleParameters_entry_two = ctk.CTkEntry(master = self.tab_calculator, textvariable=self.calc_angleParameters_var_two, state="disabled", width=55, fg_color="gray17", border_color="gray24")
        self.calc_angleParameters_entry_two.place(x=10,y=210)
 

        self.calc_angleParameters_var_three = ctk.DoubleVar(master = self.tab_calculator, value=0.0)
        self.calc_angleParameters_entry_three = ctk.CTkEntry(master = self.tab_calculator, textvariable=self.calc_angleParameters_var_three, state="disabled", width=55, fg_color="gray17", border_color="gray24")
        self.calc_angleParameters_entry_three.place(x=10,y=250)


    #endregion

    #region objects tab

    def init_tab_objects(self):

        
        self.tab_objects = self.tabview.add("Objects")

        objects_name_label = ctk.CTkLabel(master = self.tab_objects, text = 'Name')
        self.objects_name_var = ctk.StringVar(master = self.tab_objects)
        self.objects_name_entry = ctk.CTkEntry(master = self.tab_objects, textvariable = self.objects_name_var)
        objects_name_label.place(x=10, y=10)
        self.objects_name_entry.place(x=50,y=10)


        objects_color_label = ctk.CTkLabel(master = self.tab_objects, text ="Color - Size")
        self.objects_color_var = ctk.CTkComboBox(master = self.tab_objects, width= 85, values=["Red", 
                                                                                               "Orange", 
                                                                                               "Yellow", 
                                                                                               "Green", 
                                                                                               "Blue", 
                                                                                               "Indigo", 
                                                                                               "Violet", 
                                                                                               "White",
                                                                                               "Gray"])
        objects_color_label.place(x=100, y=50)
        self.objects_color_var.place(x=10, y=50)
        
        self.objects_size_var = ctk.DoubleVar(master = self.tab_objects)
        self.objects_size_entry = ctk.CTkEntry(master = self.tab_objects, textvariable=self.objects_size_var, width = 50)
        self.objects_size_entry.place(x=170, y=50)


        objects_semimajorAxis_label = ctk.CTkLabel(master = self.tab_objects, text ="Semimajor Axis")
        objects_semimajorAxis_label_units = ctk.CTkLabel(master = self.tab_objects, text="(0.0) AU")
        self.objects_semimajorAxis_var = ctk.DoubleVar(master = self.tab_objects)
        self.objects_semimajorAxis_entry = ctk.CTkEntry(master = self.tab_objects, textvariable=self.objects_semimajorAxis_var, width = 55)
        objects_semimajorAxis_label.place(x=70, y=90)
        objects_semimajorAxis_label_units.place(x=170,y=90)
        self.objects_semimajorAxis_entry.place(x=10,y=90)


        objects_eccentricity_label = ctk.CTkLabel(master = self.tab_objects, text = "Eccentricity")
        objects_eccentricity_label_units = ctk.CTkLabel(master = self.tab_objects, text = "[0.0, 1.0)")
        self.objects_eccentricity_var = ctk.DoubleVar(master = self.tab_objects)
        self.objects_eccentricity_entry = ctk.CTkEntry(master = self.tab_objects, textvariable=self.objects_eccentricity_var, width = 55)
        objects_eccentricity_label.place(x=70, y=130)
        objects_eccentricity_label_units.place(x=170, y =130)
        self.objects_eccentricity_entry.place(x=10, y=130)


        objects_initAngle_label = ctk.CTkLabel(master = self.tab_objects, text = "Initial Angle")
        objects_initAngle_label_units = ctk.CTkLabel(master = self.tab_objects, text = "[0.0, 360]\u00b0")
        self.objects_initAngle_var = ctk.DoubleVar(master = self.tab_objects)
        self.objects_initAngle_entry = ctk.CTkEntry(master = self.tab_objects, textvariable=self.objects_initAngle_var, width = 55)
        objects_initAngle_label.place(x=70, y=170)
        objects_initAngle_label_units.place(x=170,y=170)
        self.objects_initAngle_entry.place(x=10, y=170)


        objects_inclination_label = ctk.CTkLabel(master = self.tab_objects, text = "Inclination")
        objects_inclination_label_units = ctk.CTkLabel(master = self.tab_objects, text = "[0.0, 360]\u00b0")
        self.objects_inclination_var = ctk.DoubleVar(master = self.tab_objects)
        self.objects_inclination_entry = ctk.CTkEntry(master = self.tab_objects, textvariable=self.objects_inclination_var, width = 55)
        objects_inclination_label.place(x=70, y=210)
        objects_inclination_label_units.place(x=170,y=210)
        self.objects_inclination_entry.place(x=10, y=210)

        objects_omega_label = ctk.CTkLabel(master = self.tab_objects, text =  "Longitude A.N. ")
        objects_omega_label_units = ctk.CTkLabel(master = self.tab_objects, text = "[0.0, 360]\u00b0")
        self.objects_omega_var = ctk.DoubleVar(master = self.tab_objects)
        self.objects_omega_entry = ctk.CTkEntry(master = self.tab_objects, textvariable=self.objects_omega_var, width = 55)
        objects_omega_label.place(x=70, y=250)
        objects_omega_label_units.place(x=170,y=250)
        self.objects_omega_entry.place(x=10, y=250)

        self.objects_listedObjects = CTkL.CTkListbox(master = app, 
                                                    width=190, height=180, 
                                                    command= self.display_selected_object_values)
        self.objects_listedObjects.place(x=1025, y=385 )


        self.objects_generate_button = ctk.CTkButton(master = self.tab_objects, text = "Generate Object", corner_radius=8, width = 210,
                                                command =lambda: [pm.plot_manager.force_pause_2d(),
                                                                  self.selected_id.clear(),
                                                                om.generate_object(self.objects_name_var.get(),
                                                                                    self.objects_color_var.get(),
                                                                                    self.objects_size_var.get(),
                                                                                    self.objects_semimajorAxis_var.get(),
                                                                                    self.objects_eccentricity_var.get(),
                                                                                    self.objects_initAngle_var.get(),
                                                                                    self.objects_inclination_var.get(),
                                                                                    self.objects_omega_var.get()),
                                                                                    # pm.plot_manager.delete_animation_2d(),
                                                                                    # pm.plot_manager.delete_animation_3d(),
                                                                                    self.plot_sequence_2d(),
                                                                                    self.plot_sequence_3d(),
                                                                                    self.delete_visual_feedback(),
                                                                                    self.populate_objects_list()]
                                                                                    )
                                                                                            
        self.objects_generate_button.place(x=10,y=290)

        self.objects_delete_button = ctk.CTkButton(master = app, text = "Delete Object", corner_radius=8, width = 210, fg_color="gray10", state="DISABLED", 
                                                   command = lambda: [self.delete_selected_object(),
                                                                      self.plot_sequence_2d(),
                                                                      self.plot_sequence_3d(),
                                                                      self.populate_objects_list(), 
                                                                      self.delete_visual_feedback()])
        self.objects_delete_button.place(x=1025,y=615)

        self.objects_Clear_button = ctk.CTkButton(master = app, text = "Clear Objects", corner_radius=8, width = 210, command = lambda: [om.clear_celestial_objects(), self.delete_visual_feedback(), self.plot_sequence_2d(), self.plot_sequence_3d(), self.populate_objects_list()])
        self.objects_Clear_button.place(x=1025,y=655)

        self.objects_listedObjects.configure(height=6)
    
    #endregion
    
    # region frontend visual feedback methods
    
    def populate_objects_list(self):
        print("populating object list with values...")
        
        self.objects_listedObjects.delete("all")
        cobj = om.get_celestial_objects()

        if len(cobj) > 0:

            for i,x in enumerate((cobj)):
                print(f"adding {x.name} to the list")
                self.objects_listedObjects.insert(i, x.name) 
        
        return
    
    
    def display_selected_object_values(self, selected_option):
        
        cobj = om.get_celestial_objects()
        for x in (cobj) :

            if x.name == selected_option:
                print("selected_id is now "+ str(selected_option))
                self.selected_id = [x]
                pm.plot_manager.init_2d_plotting(pm.plot_manager.fig)
                self.delete_visual_feedback()
                # populate fields with object's parameters
                self.objects_name_var.set(x.name)
                self.objects_color_var.set(x.color)
                if (x.size == ""):
                    x.size = 0
                    self.objects_size_var.set(f'{x.size:.3}')
                else:
                    self.objects_size_var.set(f'{x.size:.3}')

                if (x.semimajor_axis == ""):
                    x.semimajor_axis = 0
                    self.objects_semimajorAxis_var.set(f'{x.semimajor_axis:.3}')
                else:
                    self.objects_semimajorAxis_var.set(f'{x.semimajor_axis:.3}')
                
                if(x.eccentricity == ""):
                    x.eccentricity = 0
                    self.objects_eccentricity_var.set(f'{x.eccentricity:.3}')
                    self.calc_eccentricity_var.set(f'{x.eccentricity:.3}')
                else:
                    self.objects_eccentricity_var.set(f'{x.eccentricity:.3}')
                    self.calc_eccentricity_var.set(f'{x.eccentricity:.3}')

                if (x.initial_angle == ""):
                    x.initial_angle = 0
                    self.objects_initAngle_var.set(f'{x.initial_angle:.3}')
                else:
                    self.objects_initAngle_var.set(f'{x.initial_angle:.3}')

                if (x.inclination == ""):
                    x.inclination = 0
                    self.objects_inclination_var.set(f'{x.inclination:.3}')
                else:
                    self.objects_inclination_var.set(f'{x.inclination:.3}')

                # psi = longitude of asc. node
                if (x.omega == ""):
                    x.omega = 0
                    self.objects_omega_var.set(f'{x.omega:.3}')
                else:
                    self.objects_omega_var.set(f'{x.omega:.3}')
                
                self.plot_sequence_2d()
        return
    
    def delete_selected_object(self):
        # Identify the object by name
        print("deleting " + self.selected_id[0].name)
        cobj = om.get_celestial_objects()

        if len(self.selected_id) == 0:
            
            return

        else:
            name_to_delete = self.selected_id[0].name
            for x in cobj:
                
                if x.name == name_to_delete:
                    print("removing item")
                    om.celestial_objects.remove(self.selected_id[0])
                    self.selected_id.remove(x)

    def delete_visual_feedback(self):
        if len(self.selected_id) == 0 :
            self.objects_delete_button.configure(state="DISABLED", fg_color = "gray10")
            
        else:
            self.objects_delete_button.configure(state="NORMAL", fg_color = "#3a7ebf")
            
    # contains plotting methods
        # toggle_pause_3d()
        # toggle_pause_2d()
        # animate_manual()
        # plot_sequence_3d()   
    def init_tab_configure(self):

        self.tab_configure = self.tabview.add("Configure")
        # self.tab_configure.bind("<Button-1>", self.plot_sequence)
        configure_add_solar_planets_button = ctk.CTkButton(master = self.tab_configure, text = "Add Solar Planets", width=210,
                                                           command=lambda: [mysql_c_i.generate_solar_planets(), self.populate_objects_list()])
        configure_add_solar_planets_button.place(x=10,y=10)

        configure_add_terrestrials_button = ctk.CTkButton(master = self.tab_configure, text = "Add Terrestrials", width=55,
                                                           command=lambda: [mysql_c_i.generate_terrestrial_planets(), self.populate_objects_list()])
        configure_add_terrestrials_button.place(x=10, y=50)

        configure_add_jovians_button = ctk.CTkButton(master = self.tab_configure, text = "Add Jovians", width=100,
                                                           command=lambda: [mysql_c_i.generate_jovian_planets(), self.populate_objects_list()])
        configure_add_jovians_button.place(x=120, y=50)


       

        # 2D animation button controls
        configure_label_animation_2d = ctk.CTkLabel(master = self.tab_configure, text = "2D Animation")
        configure_label_animation_2d.place(x=10,y=150)

        # configure_button_frewind_2d = ctk.CTkButton(master = self.tab_configure, text="<<",width=30,height=30, command=self.plot_sequence_2d)
        # configure_button_frewind_2d.place(x=10,y=190)
        # configure_button_rewind_2d = ctk.CTkButton(master = self.tab_configure, text="<",width=30,height=30, command=self.decrement_animation_2d_speed)
        # configure_button_rewind_2d.place(x=50,y=190)
        configure_button_play_2d = ctk.CTkButton(master = self.tab_configure, text=">=",width=30,height=30, command=pm.plot_manager.toggle_pause_2d)
        configure_button_play_2d.place(x=100,y=150)
        # configure_button_forward_2d = ctk.CTkButton(master = self.tab_configure, text =">",width=30,height=30, command=self.increment_animation_2d_speed)
        # configure_button_forward_2d.place(x=130,y=190)
        # configure_button_forward_2d = ctk.CTkButton(master = self.tab_configure, text =">>",width=30,height=30)
        # configure_button_forward_2d.place(x=170,y=190)
        # configure_playbackSpeed_label = ctk.CTkLabel(master=self.tab_configure, text='Playback Speed')
        # configure_playbackSpeed_label.place(x=50, y=130)
        # configure_playbackSpeed_var = ctk.CTkEntry(master = self.tab_configure, width = 30)
        # configure_playbackSpeed_var.place(x=10, y=130)

         # 3D animation button controls
        configure_label_animation_3d = ctk.CTkLabel(master = self.tab_configure, text = "3D Animation")
        configure_label_animation_3d.place(x=10,y=190)

        # configure_button_frewind_3d = ctk.CTkButton(master = self.tab_configure, text="<<",width=30,height=30)
        # configure_button_frewind_3d.place(x=10,y=120)
        # configure_button_rewind_3d = ctk.CTkButton(master = self.tab_configure, text="<",width=30,height=30, command=self.decrement_animation_3d_speed)
        # configure_button_rewind_3d.place(x=50,y=120)
        configure_button_play_3d = ctk.CTkButton(master = self.tab_configure, text=">=",width=30,height=30, command=pm.plot_manager.toggle_pause_3d)
        configure_button_play_3d.place(x=100,y=190)
        # configure_button_forward_3d = ctk.CTkButton(master = self.tab_configure, text =">",width=30,height=30, command=self.increment_animation_3d_speed)
        # configure_button_forward_3d.place(x=130,y=120)
        # configure_button_forward_3d = ctk.CTkButton(master = self.tab_configure, text =">>",width=30,height=30)
        # configure_button_forward_3d.place(x=170,y=120)

        self.configure_slider_label_upper = ctk.CTkLabel(master = self.tab_configure,
                                                text="-1000 Days")
        self.configure_slider_label_upper.place(x=10, y=255)
        self.configure_slider = ctk.CTkSlider(master=self.tab_configure, 
                                            from_=-1000, 
                                            to=1000, 
                                            number_of_steps=2000,
                                            command=pm.plot_manager.animate_manual_3d,
                                            height = 10,
                                            orientation="horizontal")
        self.configure_slider.place(x=10,y=235)
        # # self.configure_slider_label_middle = ctk.CTkLabel(master = self.tab_configure, text="0 Days")
        # # self.configure_slider_label_middle.place(x=50, y=125)
        self.configure_slider_label_lower = ctk.CTkLabel(master = self.tab_configure, text="+1000 Days")
        self.configure_slider_label_lower.place(x=140,y=255)
        
        # self.configure_listedObjects = CTkL.CTkListbox(master = app, width=190,height=180, command= self.display_selected_object_values)
        # self.configure_listedObjects.place(x=10, y=330)

        # self.configure_delete_button = ctk.CTkButton(master = app, text = "Delete Object", corner_radius=8, width = 210, fg_color="gray10", state="DISABLED", command = lambda: [self.delete_selected_object(), self.populate_objects_list(), self.delete_visual_feedback()])
        # self.configure_delete_button.place(x=10,y=565)

        # configure_Clear_button = ctk.CTkButton(master = app, text = "Clear Objects", corner_radius=8, width = 210, command = lambda: [om.clear_celestial_objects(), self.populate_objects_list(), self.delete_visual_feedback()])
        # configure_Clear_button.place(x=10,y=605)
        configure_plot_button = ctk.CTkButton(master = self.tab_configure, text ="Plot Objects", width=210, 
                                              command=lambda: [ self.plot_sequence_3d()])
        
        
        configure_plot_button.place(x=10, y=290)

    #region plots

    def init_3d_plot_window(self):
        
        
        self.frame_plotwindow = ctk.CTkFrame(self.master, width = 970, height = 680)
        self.frame_plotwindow.place(x=20,y =20)
        
        # 11.7, 8.1
        # self.fig = Figure(figsize=(11.7,8.1))

        self.canvas = FigureCanvasTkAgg(pm.plot_manager.fig,
                                        master = self.frame_plotwindow)  # A tk.DrawingArea.

        self.button_quit = ctk.CTkButton(master = self.frame_plotwindow, 
                                        text="Quit",
                                        command=app.quit,
                                        width = 35,
                                        height = 35)
        self.button_quit.place(x=905, y = 22.5)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_plotwindow, pack_toolbar=False)
        self.toolbar.place(x=30,y=30)
        self.toolbar.update()
        self.canvas.get_tk_widget().place(x=20, y=20)    
        
        pm.plot_manager.init_3d_plotting(pm.plot_manager.fig)

    #endregion


    def plot_sequence_3d(self):
        print("plot sequence: 3d")
        self.init_3d_plot_window()
        # pm.plot_manager.init_2d_plotting(pm.plot_manager.fig)
        pm.plot_manager.generate_scatter_plots_3d()
        # pm.plot_manager.generate_scatter_plots_2d(self.selected_id)
        pm.plot_manager.plot_full_orbits_3d(pm.plot_manager.fig)
        # pm.plot_manager.plot_full_orbit_2d(pm.plot_manager.fig, self.selected_id)
        pm.plot_manager.plot_sequence_animation_3d(pm.plot_manager.fig)
        pm.plot_manager.animate_manual_3d(0)
        return
    
    def plot_sequence_2d(self):
        pm.plot_manager.init_2d_plotting(pm.plot_manager.fig)
        pm.plot_manager.generate_scatter_plots_2d(self.selected_id)
        pm.plot_manager.plot_full_orbit_2d(pm.plot_manager.fig, self.selected_id)
        pm.plot_manager.plot_sequence_animation_2d(pm.plot_manager.fig, self.selected_id)
        return

    
    #region calc window backend


    def translate_anomalies(self):
        
        deg_to_rad = np.pi/180
        _e = self.calc_eccentricity_var.get()
        anomaly = self.calc_angleParameters_label.get()
        
        match anomaly:
            case "True Anomaly":
                print("case v")
                self.calc_anomalies_textbox.configure(state="normal")
                self.calc_anomalies_textbox.delete(1.0,'end')
                self.calc_anomalies_textbox.insert('end', "Eccentric Anomaly" + "\n\n")
                self.calc_anomalies_textbox.insert('end',"Mean Anomaly")
                self.calc_anomalies_textbox.configure(state="disabled")
                _v = float(self.calc_angleParameters_var.get()*deg_to_rad)
                _Ecc = 0    #float(self.calc_angleParameters_var_two.get())
                _m = 0      #float(self.calc_angleParameters_var_three.get())
                ac.set_anomalies(float(_e),[_v],[_Ecc],[_m],self.calc_angleParameters_label.get())
            case "Eccentric Anomaly":
                self.calc_anomalies_textbox.configure(state="normal")
                self.calc_anomalies_textbox.delete(1.0,'end')
                self.calc_anomalies_textbox.insert('end', "True Anomaly" + "\n\n")
                self.calc_anomalies_textbox.insert('end',"Mean Anomaly")
                self.calc_anomalies_textbox.configure(state="disabled")
                _Ecc = float(self.calc_angleParameters_var.get()*deg_to_rad)
                _v = 0      #self.calc_angleParameters_var_two.get()
                _m = 0      #self.calc_angleParameters_var_three.get()
                ac.set_anomalies(float(_e),[_v],[_Ecc],[_m],self.calc_angleParameters_label.get())
            case "Mean Anomaly":
                self.calc_anomalies_textbox.configure(state="normal")
                self.calc_anomalies_textbox.delete(1.0,'end')
                self.calc_anomalies_textbox.insert('end', "True Anomaly" + "\n\n")
                self.calc_anomalies_textbox.insert('end',"Eccentric Anomaly")
                self.calc_anomalies_textbox.configure(state="disabled")
                _m = float(self.calc_angleParameters_var.get()*deg_to_rad)
                _v = 0      #self.calc_angleParameters_var_two.get()
                _Ecc = 0    #self.calc_angleParameters_var_three.get()
                ac.set_anomalies(float(_e),[_v],[_Ecc],[_m],self.calc_angleParameters_label.get())

        # _e = self.calc_eccentricity_var.get()
        # if (self.calc_angleParameters_var.get() == ""):
        #     self.calc_v_var.set(0.0)
        # _v = self.calc_v_var.get()
        # _E_ = self.calc_E_var.get()
        # _m = self.calc_m_var.get()
        
        
    
    """
    For the calculator tab, when selecting an item from 
    the objects list, the semimajor axis and eccentricity 
    fill their variables.

    The user must choose the angle they have, and then the
    other two angle variables are calculated.
    """
    def display_angles(self):
        anomaly = self.calc_angleParameters_label.get()
        # anomaly = "True Anomaly"
        v_str = "True Anomaly"
        E_str = "Eccentric Anomaly"
        m_str = "Mean Anomaly"
        match anomaly:
            case "True Anomaly":
                print("displaying case v")
                self.calc_angleParameters_var_two.set('{:.2f}'.format(ac.calculated_angles[1]))
                self.calc_angleParameters_var_three.set('{:.2f}'.format(ac.calculated_angles[2]))

            case "Eccentric Anomaly":
                self.calc_angleParameters_var_two.set('{:.2f}'.format(ac.calculated_angles[0]))
                self.calc_angleParameters_var_three.set('{:.2f}'.format(ac.calculated_angles[2]))
                

            case "Mean Anomaly":
                self.calc_angleParameters_var_two.set('{:.2f}'.format(ac.calculated_angles[0]))
                self.calc_angleParameters_var_three.set('{:.2f}'.format(ac.calculated_angles[1]))


    def calc_callback(self, *args):
        self.translate_anomalies()
        self.display_angles() 
          
     
#endregion 

#region initialization 
    

    def init_window(self):
    
        self.init_3d_plot_window()
        pm.plot_manager.init_2d_plotting(pm.plot_manager.fig)
        self.init_tabs()
        self.init_tab_configure()
        self.init_tab_objects()
        self.init_tab_calc()
        self.populate_objects_list()
    
    
#endregion
style.use("dark_background")

app = ctk.CTk()
app.resizable(width=False, height=False)
app.geometry("1280x720")
app.title("Orbital Cartographer")

gui = Window(app)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


app.mainloop()
