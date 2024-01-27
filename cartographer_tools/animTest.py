# import matplotlib.pyplot as plt
# import numpy as np

# import tkinter
# import customtkinter as ctk

# from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
#                                                NavigationToolbar2Tk)
# import matplotlib.animation as animation

# import ObjectManager as om

# test1=om.GenerateObject("earf",1,"b",1,0.05,0,0,0)

# # app = ctk.CTk()
# # app.resizable(width=False, height=False)
# # app.geometry("1280x720")

# def update(frame, orbits, lines):
#     for line, o in zip (lines, orbits):
#         for i in range(0, len(orbits)):
#             line.set_data_3d(orbits[i].x[:frame],orbits[i].y[:frame],orbits[i].z[:frame])
#     return lines

# orbitals = om.celestial_objects

# # Attaching 3D axis to the figure
# fig = plt.figure()
# ax = fig.add_subplot(projection="3d")

# # frame_plotwindow = ctk.CTkFrame(master = app, width = 1000, height = 680)
# # frame_plotwindow.place(x=20,y =20)
# # canvas = FigureCanvasTkAgg(fig, master=frame_plotwindow)  # A tk.DrawingArea.

# # Create lines initially without data
# lines = [ax.plot([], [], [])[0] for _ in orbitals]

# # Creating the Animation object
# ani = animation.FuncAnimation(
#     fig, update, 1000, fargs=(orbitals, lines), interval=10, blit=True)

# plt.show()

# app.mainloop()

# #################################################################
# # import tkinter as tk
# # from matplotlib.figure import Figure
# # from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# # from matplotlib.animation import FuncAnimation

# # # Function to update the plot during animation
# # def update_plot(frame):
# #     # Your update logic goes here
# #     # For example, plot some data based on the frame number
# #     x = range(10)
# #     y = [i * frame for i in x]
# #     line.set_data(x, y)
# #     return line,

# # # Create the Tkinter window
# # root = tk.Tk()
# # root.title("Matplotlib Animation in Tkinter")

# # # Create a Matplotlib figure and axis
# # fig, ax = Figure(), Figure().add_subplot(111)

# # # Plot initial data
# # line, = ax.plot([], [], label='Animated Line')
# # ax.legend()

# # # Create a Tkinter canvas for the Matplotlib figure
# # canvas = FigureCanvasTkAgg(fig, master=root)
# # canvas_widget = canvas.get_tk_widget()
# # canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# # # Create the animation
# # animation = FuncAnimation(fig, update_plot, frames=range(1, 10), interval=500, blit=True)

# # # Start the Tkinter event loop
# # root.mainloop()
# ##########################################################3
import tkinter

import numpy as np

# # # # Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

root = tkinter.Tk()
root.wm_title("Embedding in Tk")

fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
ax = fig.add_subplot(projection="3d")
line, = ax.plot(t, 2 * np.sin(2 * np.pi * t), 2*np.cos(2*np.pi*t))
# ax.set_xlabel("time [s]")
# ax.set_ylabel("f(t)")

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

# pack_toolbar=False will make it easier to use a layout manager later on.
toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

canvas.mpl_connect(
    "key_press_event", lambda event: print(f"you pressed {event.key}"))
canvas.mpl_connect("key_press_event", key_press_handler)

button_quit = tkinter.Button(master=root, text="Quit", command=root.destroy)


def update_frequency(new_val):
    # retrieve frequency
    f = float(new_val)
    ax.cla()
    # update data
    y = 2 * np.sin(2 * np.pi * f * t)
    z = 2 * np.cos(2*np.pi * f * t)
    ax.scatter(t, y, z)
    
    # required to update canvas and attached toolbar!
    canvas.draw()


slider_update = tkinter.Scale(root, from_=1, to=30, orient=tkinter.HORIZONTAL,
                              command=update_frequency, label="Frequency [Hz]")

# Packing order is important. Widgets are processed sequentially and if there
# is no space left, because the window is too small, they are not displayed.
# The canvas is rather flexible in its size, so we pack it last which makes
# sure the UI controls are displayed as long as possible.
button_quit.pack(side=tkinter.BOTTOM)
slider_update.pack(side=tkinter.BOTTOM)
toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

tkinter.mainloop()

# Imports

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#---------End of imports



# from tkinter import Frame,Label,Entry,Button


# class Window(Frame):

#     def __init__(self, master = None):
#         Frame.__init__(self, master)
#         self.master = master
#         self.init_window()


#     def Clear(self):      
#         print("clear")
#         self.textAmplitude.insert(0, "1.0")
#         self.textSpeed.insert(0, "1.0")       


#     def Plot(self):
#         self.v = float(self.textSpeed.get())
#         self.A = float(self.textAmplitude.get())


#     def animate(self,i):
#         self.line.set_ydata(self.A*np.sin(self.x+self.v*i))  # update the data
#         return self.line,


#     def init_window(self):



#         self.master.title("Use Of FuncAnimation in tkinter based GUI")
#         self.pack(fill='both', expand=1)     

#         #Create the controls, note use of grid

#         self.labelSpeed = Label(self,text="Speed (km/Hr)",width=12)
#         self.labelSpeed.grid(row=0,column=1)
#         self.labelAmplitude = Label(self,text="Amplitude",width=12)
#         self.labelAmplitude.grid(row=0,column=2)

#         self.textSpeed = Entry(self,width=12)
#         self.textSpeed.grid(row=1,column=1)
#         self.textAmplitude = Entry(self,width=12)
#         self.textAmplitude.grid(row=1,column=2)

#         self.textAmplitude.insert(0, "1.0")
#         self.textSpeed.insert(0, "1.0")
#         self.v = 1.0
#         self.A = 1.0


#         self.buttonPlot = Button(self,text="Plot",command=self.Plot,width=12)        
#         self.buttonPlot.grid(row=2,column=1)

#         self.buttonClear = Button(self,text="Clear",command=self.Clear,width=12)
#         self.buttonClear.grid(row=2,column=2)


#         self.buttonClear.bind(lambda e:self.Clear)



#         tk.Label(self,text="SHM Simulation").grid(column=0, row=3)

#         self.fig = plt.Figure()

#         self.x = 20*np.arange(0, 2*np.pi, 0.01)        # x-array


#         self.ax = self.fig.add_subplot(111)
#         self.line, = self.ax.plot(self.x, np.sin(self.x))        


#         self.canvas = FigureCanvasTkAgg(self.fig, master=self)
#         self.canvas.get_tk_widget().grid(column=0,row=4)


#         self.ani = animation.FuncAnimation(self.fig, self.animate, np.arange(1, 200), interval=25, blit=False)




# root = tk.Tk()
# root.geometry("700x400")
# app = Window(root)
# tk.mainloop()