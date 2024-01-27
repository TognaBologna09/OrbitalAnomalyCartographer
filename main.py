
"""Welcome to the OrbitalAnomalyCartographer"""

# For essential math
import numpy as np
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
# Implement CelestialObject class
from cartographer_tools import ObjectManager as om

import tkinter as tk
import customtkinter as ctk
import CTkListbox as CTkL

class Window(ctk.CTkFrame):

    lines = []
    scats = []

    def __init__(self, master = None, resolution="1280x720"):
        style.use("dark_background")
        ctk.CTkFrame.__init__(self, master)
        self.master = master
        self.resolution = resolution
        self.init_window()
    
#region frontend facing GUI
                
    def init_tabs(self):
        self.tabview = ctk.CTkTabview(master = app, height = 690, width =220)
        self.tabview.place(x=1040,y=10)


    def init_tab_calc(self):


        tab_calculator = self.tabview.add("Calculator")

        tutorial = "Choose a value for the axis, and eccentricity.\n\nEnter a value for any of the \norbital angles from 0 to 2pi.\n\nThe other angles will \nautomatically generate."

        calc_tutorial_label = ctk.CTkTextbox(master=tab_calculator, width=185, state='disabled',height = 110)
        calc_tutorial_label.configure(state='normal')
        calc_tutorial_label.insert('end',tutorial)
        calc_tutorial_label.configure(state='disabled')
        calc_tutorial_label.place(x=10,y=10)

        calc_semimajorAxis_label = ctk.CTkLabel(master = tab_calculator, text ="Semimajor Axis")
        calc_semimajorAxis_var = ctk.CTkEntry(master = tab_calculator, width = 40)
        calc_semimajorAxis_label.place(x=10, y=130)
        calc_semimajorAxis_var.place(x=120,y=130)

        calc_eccentricity_label = ctk.CTkLabel(master = tab_calculator, text = "Eccentricity")
        calc_eccentricity_var = ctk.CTkEntry(master = tab_calculator, width = 40)
        calc_eccentricity_label.place(x=10, y=170)
        calc_eccentricity_var.place(x=120, y=170)

    def init_tab_objects(self):


        tab_objects = self.tabview.add("Objects")

        objects_name_label = ctk.CTkLabel(master = tab_objects, text = 'Name')
        objects_name_var = ctk.CTkEntry(master = tab_objects)
        objects_name_label.place(x=10, y=10)
        objects_name_var.place(x=50,y=10)

        objects_size_label = ctk.CTkLabel(master = tab_objects, text = 'Size')
        objects_size_var = ctk.CTkEntry(master = tab_objects, width = 40)
        objects_size_label.place(x=60, y=50)
        objects_size_var.place(x=10,y=50)

        objects_color_label = ctk.CTkLabel(master = tab_objects, text ="Color")
        objects_color_var = ctk.CTkComboBox(master = tab_objects, values=["Red", "Orange", "Yellow", "Green", "Blue", "Indigo", "Violet"])
        objects_color_label.place(x=120, y=90)
        objects_color_var.place(x=10, y=90)

        objects_semimajorAxis_label = ctk.CTkLabel(master = tab_objects, text ="Semimajor Axis      (0.0)")
        objects_semimajorAxis_var = ctk.CTkEntry(master = tab_objects, width = 40)
        objects_semimajorAxis_label.place(x=60, y=130)
        objects_semimajorAxis_var.place(x=10,y=130)

        objects_eccentricity_label = ctk.CTkLabel(master = tab_objects, text = "Eccentricity        [0.0, 1.0)")
        objects_eccentricity_var = ctk.CTkEntry(master = tab_objects, width = 40)
        objects_eccentricity_label.place(x=60, y=170)
        objects_eccentricity_var.place(x=10, y=170)

        objects_initAngle_label = ctk.CTkLabel(master = tab_objects, text = "Initial Angle        [0.0, 2pi]")
        objects_initAngle_var = ctk.CTkEntry(master = tab_objects, width = 40)
        objects_initAngle_label.place(x=60, y=210)
        objects_initAngle_var.place(x=10, y=210)

        objects_inclination_label = ctk.CTkLabel(master = tab_objects, text = "Inclination        [0.0, 2pi]")
        objects_inclination_var = ctk.CTkEntry(master = tab_objects, width = 40)
        objects_inclination_label.place(x=60, y=250)
        objects_inclination_var.place(x=10, y=250)

        objects_omega_label = ctk.CTkLabel(master = tab_objects, text = "Omega        [0.0, 2pi]")
        objects_omega_var = ctk.CTkEntry(master = tab_objects, width = 40)
        objects_omega_label.place(x=60, y=290)
        objects_omega_var.place(x=10, y=290)

        self.objects_listedObjects = CTkL.CTkListbox(master = tab_objects, width=160,height=180)
        self.objects_listedObjects.place(x=10, y=370)
    
        self.objects_Generate_button = ctk.CTkButton(master = tab_objects, text = "Generate Object", corner_radius=8, width = 180,
                                                command =lambda: [om.GenerateObject(objects_name_var.get(),
                                                                                    objects_size_var.get(),
                                                                                    objects_color_var.get(),
                                                                                    objects_semimajorAxis_var.get(),
                                                                                    objects_eccentricity_var.get(),
                                                                                    objects_initAngle_var.get(),
                                                                                    objects_inclination_var.get(),
                                                                                    objects_omega_var.get()),
                                                                                    self.Populate_Objects_List()]
                                                                                    )
                                                                                            
        self.objects_Generate_button.place(x=10,y=330)

        objects_Clear_button = ctk.CTkButton(master = tab_objects, text = "Clear Objects", corner_radius=8, width = 180, command = lambda: [om.ClearCelestialObjects(),self.Populate_Objects_List()])
        objects_Clear_button.place(x=10,y=605)
  
    def Populate_Objects_List(self):
        self.objects_listedObjects.delete("all")
        for i in range(0,len(om.celestial_objects)):
            self.objects_listedObjects.insert(i,om.celestial_objects[i].name)
        return 


    def init_tab_configure(self):


        tab_configure = self.tabview.add("Configure")

        configure_label_animation = ctk.CTkLabel(master = tab_configure, text = "Animation Controls")
        configure_label_animation.place(x=55,y=10)

        configure_button_frewind = ctk.CTkButton(master = tab_configure, text="<<",width=30,height=30)
        configure_button_frewind.place(x=10,y=50)
        configure_button_rewind = ctk.CTkButton(master = tab_configure, text="<",width=30,height=30)
        configure_button_rewind.place(x=50,y=50)
        configure_button_play = ctk.CTkButton(master = tab_configure, text=">=",width=30,height=30)
        configure_button_play.place(x=90,y=50)
        configure_button_forward = ctk.CTkButton(master = tab_configure, text =">",width=30,height=30)
        configure_button_forward.place(x=130,y=50)
        configure_button_forward = ctk.CTkButton(master = tab_configure, text =">>",width=30,height=30)
        configure_button_forward.place(x=170,y=50)

        configure_playbackSpeed_label = ctk.CTkLabel(master=tab_configure, text='Playback Speed')
        configure_playbackSpeed_label.place(x=50, y=90)
        configure_playbackSpeed_var = ctk.CTkEntry(master = tab_configure, width = 30)
        configure_playbackSpeed_var.place(x=10, y=90)

        configure_plot_button = ctk.CTkButton(master = tab_configure, text ="Plot Objects", width=180, 
                                              command=lambda: [self.init_plot_window(),
                                                                self.Generate_Scatter_Plots(),
                                                                self.Plot_Full_Orbits(),
                                                                self.Animate_Manual(0)
                                                                # ,self.init_anim_window(),
                                                                # self.Generate_Lines(),
                                                                # self.init_animation()
                                                                ])
        
        
        configure_plot_button.place(x=10, y=130)

        self.configure_slider = ctk.CTkSlider(master=tab_configure, 
                                            from_=-np.pi, 
                                            to=np.pi, 
                                            number_of_steps=1000,
                                            command=self.Animate_Manual,
                                            width = 180)
        self.configure_slider.place(x=10,y=170)


    def init_plot_window(self):
        
        
        self.frame_plotwindow = ctk.CTkFrame(self.master, width = 1000, height = 680)
        self.frame_plotwindow.place(x=20,y =20)
     
        self.fig = Figure(figsize=(12.05,8.1))

        self.canvas = FigureCanvasTkAgg(self.fig,
                                        master = self.frame_plotwindow)  # A tk.DrawingArea.

        self.button_quit = ctk.CTkButton(master = self.frame_plotwindow, 
                                        text="Quit",
                                        command=app.quit,
                                        width = 35,
                                        height = 35)
        self.button_quit.place(x=935, y = 22.5)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_plotwindow, pack_toolbar=False)
        self.toolbar.place(x=30,y=30)
        self.toolbar.update()

        self.canvas.get_tk_widget().place(x=20, y=20)    
        
        self.ax = self.fig.add_subplot(1,3,(1,3), projection='3d')
        self.ax.grid(True)
        self.ax.set_axis_off()
        self.ax.plot([0.1,0],[0,0],[0,0], label='x', color='b')
        self.ax.plot([0,0],[0.1,0],[0,0], label='y', color='g')
        self.ax.plot([0,0],[0,0],[0.1,0], label='z', color='r')
        
        
        plt.Axes.set_axis_off(self.ax)
        # self.Plot_Full_Orbits()
        self.Generate_Scatter_Plots()
       
    def init_anim_window(self):


        # self.frame_animwindow = ctk.CTkFrame(self.master, width=256,height =256)
        # self.frame_animwindow.place(x = 760,y=420)
    
        self.fig_anim = Figure(figsize=(3,3))
        self.canvas_anim = FigureCanvasTkAgg(self.fig_anim, master = None)

        self.canvas_anim.get_tk_widget().place(x=990,y=670)

        self.ax_anim = self.fig_anim.add_subplot(111)
        # self.ax_anim.grid(True)
        # self.ax_anim.set_axis_off()
        self.ax_anim.set_xlim(left=-2, right=2)
        self.ax_anim.set_ylim(bottom=-2,top=2)

        # plt.Axes.set_axis_off(self.ax_anim)

        
    def init_animation(self):
        self.ani = animation.FuncAnimation(self.fig_anim, self.Animate_Automatic, 1000, interval=500, blit=False)
    
        

#region backend functions
        
    
    def Plot_Full_Orbits(self):
        if(len(om.celestial_objects))<1:
            plt.clf()

        else:
            for i in range(0, len(om.celestial_objects)):
                x,y,z = om.celestial_objects[i].rotate_radial(om.celestial_objects[i].theta)
                self.ax.plot(x,y,z, color = om.celestial_objects[i].color, linestyle='dashed')
                self.fig.canvas.draw_idle()


    def Generate_Scatter_Plots(self):
       
        self.scats.clear()

        for o in om.celestial_objects:
            self.scats.append(self.ax.scatter(o.x[0],o.y[0],o.z[0]))

    # def Animate_Manual(self, f):
    #     frame = float(f)

    #     self.Generate_Scatter_Plots()

    #     print(len(self.scats))
    #     self.ax.scatter([0],[0],[0], s=10,color='Yellow')

    #     if len(om.celestial_objects) > 0:

    #         for i in range(0,len(om.celestial_objects)):

    #             a, b, c = om.celestial_objects[i].rotate_radial_scalarAngle(frame + np.pi + om.celestial_objects[i].initial_angle)
                
    #             self.scats[i] = self.ax.scatter(a,b,c)
    #             print("offset it u whore")
    #             self.scats[i].set_data_3d
    #             print("nyeh")
    #             self.fig.canvas.draw_idle()
            
    def Animate_Manual(self, f):
        frame = float(f)

        # self.Generate_Scatter_Plots()

        # print(len(self.scats))
        # self.ax.scatter([0], [0], [0], s=10, color='Yellow')

        if len(om.celestial_objects) > 0:

            for i in range(0, len(om.celestial_objects)):

                a, b, c = om.celestial_objects[i].rotate_radial_scalarAngle(frame + om.celestial_objects[i].initial_angle)

                # Check if the scatter plot already exists
                if i < len(self.scats):
                    # Update the existing scatter plot's data
                    self.scats[i]._offsets3d=(a, b, c)
                    # scatter = self.ax.scatter(a, b, c)
                else:
                    # Create a new scatter plot if it doesn't exist
                    print("creating plot")
                    scatter = self.ax.scatter(a, b, c, s=om.celestial_objects[i].size, color=om.celestial_objects[i].color)
                    print(a,b,c)
                    self.scats.append(scatter)

        # print("offset it u whore")
        self.fig.canvas.draw_idle()

    theta_domain = np.linspace(0,2*np.pi,1000)

    def Generate_Lines(self):

        self.lines.clear()
        for o in om.celestial_objects:
            line = self.ax_anim.scatter(o.x,o.y, s=o.size, color = o.color)
            self.lines.append(line)
    
    def Animate_Automatic(self,f):
        
        trail_length = 5
        
        self.ax_anim.scatter([0],[0], marker = 'o',color='Yellow')

        # self.fig_anim.clf()
        # self.init_anim_window()
        if len(om.celestial_objects) > 0:

            for i in range(0,len(om.celestial_objects)):

                
                p = om.celestial_objects[i].semimajor_axis*(1-om.celestial_objects[i].eccentricity**2)

                rval = p / (1 + om.celestial_objects[i].eccentricity*np.cos(self.theta_domain+f*.01))

                x_data = np.zeros(trail_length)
                y_data = np.zeros(trail_length)

                for j in range(0,trail_length):
                    value = j/trail_length
                    x_radial = np.multiply(rval[f],np.cos(f*value*np.pi))
                    x_data[j] = x_radial
                    y_radial = np.multiply(rval[f],np.sin(f*value*np.pi))
                    y_data[j] = y_radial


                if len(self.lines) < 1:
                    pass

                elif f < trail_length:

                    self.lines[i].set_offsets((x_data,y_data))
                    
                    return
                    
                else:

                    self.lines[i].set_offsets((x_data,y_data))
                    
                    
                    return


            
#endregion 

#region initialization and null value generation
    

    def init_window(self):
        # self.scats = []
        self.init_plot_window()
        # self.init_anim_window()
        # self.init_animation()
        self.init_tabs()
        self.init_tab_configure()
        self.init_tab_objects()
        self.init_tab_calc()
        self.Populate_Objects_List()
    
    
#endregion
style.use("dark_background")

app = ctk.CTk()
app.resizable(width=False, height=False)
app.geometry("1280x720")

cobj = om.GetCelestialObjects()

gui = Window(app)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# # Begin Plot window

# frame_plotwindow = ctk.CTkFrame(master = app, width = 1000, height = 680)
# frame_plotwindow.place(x=20,y =20)

# fig = Figure(figsize=(12.05,8.1))
# canvas = FigureCanvasTkAgg(fig, master=frame_plotwindow)  # A tk.DrawingArea.

# ax = fig.add_subplot(1,3,(1,3), projection='3d')
# ax.grid(False)
# ax.set_axis_off()
# ax.plot([0.1,0],[0,0],[0,0], label='x', color='b')
# ax.plot([0,0],[0.1,0],[0,0], label='y', color='g')
# ax.plot([0,0],[0,0],[0.1,0], label='z', color='r')
# plt.Axes.set_axis_off(ax)

# plots = []

# def PlotFullOrbits():
#     if(len(om.celestial_objects))<1:
#         plt.clf()
        
#     else:
#         for i in range(0, len(om.celestial_objects)):
#             x,y,z = om.celestial_objects[i].rotate_radial(om.celestial_objects[i].theta)
#             # print(x[750:],y[750:])
#             ax.plot(x,y,z, color = om.celestial_objects[i].color)
#             fig.canvas.draw_idle()

# def PlotOrbitalPosition():
#     if(len(om.celestial_objects))<1:
#         plt.clf()
        
#     else:
#         for i in range(0,len(om.celestial_objects)):
            
#             plots.append(ax.plot(om.celestial_objects[i].x[0],om.celestial_objects[i].y[0],om.celestial_objects[i].z[0], lw = om.celestial_objects[i].size, color = om.celestial_objects[i].color, marker = 'o'))
#             # print(scatPlots[i])
#             canvas.draw()


# # scats = [ax.scatter([],[],[], marker = 'o', lw=_.size)[0] for _ in om.celestial_objects]
# scats = []
# def GenerateScatterPlots():
#     scats.clear()
#     for o in om.celestial_objects:
#         scats.append(ax.scatter(o.x[0],o.y[0],o.z[0]))
#         # scats.append(ax.scatter(o.posx,o.posy,o.posz, s=o.size,color=o.color))
# GenerateScatterPlots()

# def Animate_manual(f):
#     for i in range(0,len(om.celestial_objects)):
#         # print(frame, o.x[frame],o.y[frame],o.z[frame])
#         # om.celestial_objects[i].increment_theta()
#         a,b,c = om.celestial_objects[i].rotate_radial_scalarAngle(f)
#         om.celestial_objects[i].SetVector3(a,b,c)
#         scats[i]._offsets3d = (om.celestial_objects[i].orbit_vector_scalar(f))
#         # print(o.posx,o.posy,o.posz)
#         # print(om.celestial_objects[i].x[frame],om.celestial_objects[i].y[frame],om.celestial_objects[i].z[frame])
#         canvas.draw()

# # def Animate_play_auto(frame):
# #     for j in range(0,len(om.celestial_objects)):
# #         # print(frame, o.x[frame],o.y[frame],o.z[frame])
# #         # om.celestial_objects[i].increment_theta()
# #         a,b,c = om.celestial_objects[j].rotate_radial_scalarAngle(om.celestial_objects[j].theta[i])
# #         om.celestial_objects[j].SetVector3(a,b,c)
# #         scats[j]._offsets3d = (om.celestial_objects[j].orbit_vector_scalar(om.celestial_objects[j].theta[i]))
# #         # print(o.posx,o.posy,o.posz)
# #         # print(om.celestial_objects[i].x[frame],om.celestial_objects[i].y[frame],om.celestial_objects[i].z[frame])
# #         canvas.draw()

# def DrawCanvas():
#     ax.cla()
#     canvas.draw()

# toolbar = NavigationToolbar2Tk(canvas, frame_plotwindow, pack_toolbar=False)
# toolbar.place(x=30,y=30)
# toolbar.update()

# canvas.get_tk_widget().place(x=20, y=20)    


# # ani = animation.FuncAnimation(fig, func=Animate, fargs=(om.celestial_objects,lines), frames=1000, interval =10, blit=True)
# # plt.show()

# button_quit = ctk.CTkButton(master=frame_plotwindow, text="Quit", command=app.quit, width = 35, height = 35)
# button_quit.place(x=935, y = 22.5)

# ## Tab features
# # [Configure] [Objects] [Calculator]
# tabview = ctk.CTkTabview(master = app, height = 690, width =220)
# tabview.place(x=1040,y=10)

# # Begin [Configure], width is 220
# tab_configure = tabview.add("Configure")

# configure_label_animation = ctk.CTkLabel(master = tab_configure, text = "Animation Controls")
# configure_label_animation.place(x=55,y=10)

# configure_button_frewind = ctk.CTkButton(master = tab_configure, text="<<",width=30,height=30)
# configure_button_frewind.place(x=10,y=50)
# configure_button_rewind = ctk.CTkButton(master = tab_configure, text="<",width=30,height=30)
# configure_button_rewind.place(x=50,y=50)
# configure_button_play = ctk.CTkButton(master = tab_configure, text=">=",width=30,height=30)
# configure_button_play.place(x=90,y=50)
# configure_button_forward = ctk.CTkButton(master = tab_configure, text =">",width=30,height=30)
# configure_button_forward.place(x=130,y=50)
# configure_button_forward = ctk.CTkButton(master = tab_configure, text =">>",width=30,height=30)
# configure_button_forward.place(x=170,y=50)

# configure_playbackSpeed_label = ctk.CTkLabel(master=tab_configure, text='Playback Speed')
# configure_playbackSpeed_label.place(x=50, y=90)
# configure_playbackSpeed_var = ctk.CTkEntry(master = tab_configure, width = 30)
# configure_playbackSpeed_var.place(x=10, y=90)

# configure_plot_button = ctk.CTkButton(master = tab_configure, text ="Plot Objects", width=180, command=lambda: [PlotFullOrbits()])
# configure_plot_button.place(x=10, y=130)

# configure_slider = ctk.CTkSlider(master=tab_configure, from_=0, to=4*np.pi, number_of_steps=1000,
#                               command=Animate_manual, width = 180)
# configure_slider.place(x=10,y=170)

# # Begin [Objects], width is 220
# tab_objects = tabview.add("Objects")

# objects_name_label = ctk.CTkLabel(master = tab_objects, text = 'Name')
# objects_name_var = ctk.CTkEntry(master = tab_objects)
# objects_name_label.place(x=10, y=10)
# objects_name_var.place(x=50,y=10)

# objects_size_label = ctk.CTkLabel(master = tab_objects, text = 'Size')
# objects_size_var = ctk.CTkEntry(master = tab_objects, width = 40)
# objects_size_label.place(x=60, y=50)
# objects_size_var.place(x=10,y=50)

# objects_color_label = ctk.CTkLabel(master = tab_objects, text ="Color")
# objects_color_var = ctk.CTkComboBox(master = tab_objects, values=["Red", "Orange", "Yellow", "Green", "Blue", "Indigo", "Violet"])
# objects_color_label.place(x=120, y=90)
# objects_color_var.place(x=10, y=90)

# objects_semimajorAxis_label = ctk.CTkLabel(master = tab_objects, text ="Semimajor Axis      (0.0)")
# objects_semimajorAxis_var = ctk.CTkEntry(master = tab_objects, width = 40)
# objects_semimajorAxis_label.place(x=60, y=130)
# objects_semimajorAxis_var.place(x=10,y=130)

# objects_eccentricity_label = ctk.CTkLabel(master = tab_objects, text = "Eccentricity        [0.0, 1.0)")
# objects_eccentricity_var = ctk.CTkEntry(master = tab_objects, width = 40)
# objects_eccentricity_label.place(x=60, y=170)
# objects_eccentricity_var.place(x=10, y=170)

# objects_initAngle_label = ctk.CTkLabel(master = tab_objects, text = "Initial Angle        [0.0, 2pi]")
# objects_initAngle_var = ctk.CTkEntry(master = tab_objects, width = 40)
# objects_initAngle_label.place(x=60, y=210)
# objects_initAngle_var.place(x=10, y=210)

# objects_inclination_label = ctk.CTkLabel(master = tab_objects, text = "Inclination        [0.0, 2pi]")
# objects_inclination_var = ctk.CTkEntry(master = tab_objects, width = 40)
# objects_inclination_label.place(x=60, y=250)
# objects_inclination_var.place(x=10, y=250)

# objects_omega_label = ctk.CTkLabel(master = tab_objects, text = "Omega        [0.0, 2pi]")
# objects_omega_var = ctk.CTkEntry(master = tab_objects, width = 40)
# objects_omega_label.place(x=60, y=290)
# objects_omega_var.place(x=10, y=290)

# objects_listedObjects = CTkL.CTkListbox(master = tab_objects, width=160,height=180)
# objects_listedObjects.place(x=10, y=390)

# objects_Generate_button = ctk.CTkButton(master = tab_objects, text = "Generate Object", corner_radius=8, width = 180,
#                                          command =lambda: [om.GenerateObject(objects_name_var.get(),
#                                                                                         objects_size_var.get(),
#                                                                                         objects_color_var.get(),
#                                                                                         objects_semimajorAxis_var.get(),
#                                                                                         objects_eccentricity_var.get(),
#                                                                                         objects_initAngle_var.get(),
#                                                                                         objects_inclination_var.get(),
#                                                                                         objects_omega_var.get()),
#                                                                                         PopulateObjectsList(om.GetCelestialObjects())]
#                                                                                         )
                                                                                    
# objects_Generate_button.place(x=10,y=340)

# objects_Clear_button = ctk.CTkButton(master = tab_objects, text = "Clear Objects", corner_radius=8, width = 180, command = lambda: [om.ClearCelestialObjects(),PopulateObjectsList(om.GetCelestialObjects())])
# objects_Clear_button.place(x=10,y=590)

# def PopulateObjectsList(list):
#     objects_listedObjects.delete("all")
#     for i in range(0,len(list)):
#         objects_listedObjects.insert(i,list[i].name)
#     return

# # Begin [Calculator]
# tab_calculator = tabview.add("Calculator")

# tutorial = "Choose a value for the axis, and eccentricity.\n\nEnter a value for any of the \norbital angles from 0 to 2pi.\n\nThe other angles will \nautomatically generate."

# calc_tutorial_label = ctk.CTkTextbox(master=tab_calculator, width=185, state='disabled',height = 110)
# calc_tutorial_label.configure(state='normal')
# calc_tutorial_label.insert('end',tutorial)
# calc_tutorial_label.configure(state='disabled')
# calc_tutorial_label.place(x=10,y=10)

# calc_semimajorAxis_label = ctk.CTkLabel(master = tab_calculator, text ="Semimajor Axis")
# calc_semimajorAxis_var = ctk.CTkEntry(master = tab_calculator, width = 40)
# calc_semimajorAxis_label.place(x=10, y=130)
# calc_semimajorAxis_var.place(x=120,y=130)

# calc_eccentricity_label = ctk.CTkLabel(master = tab_calculator, text = "Eccentricity")
# calc_eccentricity_var = ctk.CTkEntry(master = tab_calculator, width = 40)
# calc_eccentricity_label.place(x=10, y=170)
# calc_eccentricity_var.place(x=120, y=170)

app.mainloop()

# canvas.mpl_connect(
#     "key_press_event", lambda event: print(f"you pressed {event.key}"))
# canvas.mpl_connect("key_press_event", key_press_handler)
