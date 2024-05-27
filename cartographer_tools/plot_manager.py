# For essential math
import numpy as np

# Plotting
import matplotlib.pyplot as plt

import matplotlib.animation as animation


# custom libraries
from cartographer_tools import object_manager as om
from cartographer_tools import angle_calculator as ac

class PlotManager:
    # define global variables
    lines_true = []
    lines_ecc = []
    lines_mean = []
    scatter_plots_3d = []
    scatter_plots_2d = []

    def init_3d_plotting(self, plot_figure):
        self.ax = plot_figure.add_subplot(111, projection='3d')
        self.ax.grid(True)
        self.ax.set_axis_off()

        # cartesian references

        self.ax.plot([0.1,0],[0,0],[0,0], label='x', color='b')
        self.ax.plot([0,0],[0.1,0],[0,0], label='y', color='g')
        self.ax.plot([0,0],[0,0],[0.1,0], label='z', color='r')
        
        num = 0.1
        for x in om.celestial_objects:
            num = max(x.semimajor_axis, num)

        self.ax.set_xlim3d(-num/2,num/2)
        self.ax.set_ylim3d(-num/2,num/2)
        self.ax.set_zlim3d(-num/4,num/4)
        
        plt.Axes.set_axis_off(self.ax)

    def init_2d_plotting(self, plot_figure):
        self.ax2 = plot_figure.add_subplot(224, projection='rectilinear')
        self.ax2.clear()
        self.ax2.set_axis_off()       
        self.ax2.plot(0,0, label='origin')
        self.ax2.axis('equal')

    def clear_2d_plot_window(self):
        self.ax2.clear()
        self.ax2.set_axis_off()       
        self.ax2.plot(0,0, label='origin')

    def plot_full_orbits_3d(self, plot_figure):
        if(len(om.celestial_objects))<1:
            plt.clf()

        else:
            
            for i in range(0, len(om.celestial_objects)):
                x,y,z = om.celestial_objects[i].rotate_radial(om.celestial_objects[i].theta)
                self.ax.plot(x,y,z, color = om.celestial_objects[i].color, linestyle='dashed', linewidth=min(om.celestial_objects[i].size/1.5, 1))
                
                plot_figure.canvas.draw_idle()

    def plot_full_orbit_2d(self, plot_figure, selected_id: list):
        
        if len(selected_id) == 0:
            self.ax2.cla()
        
        else:
            for o in selected_id:
                # self.ax2.cla()
                x_2d,y_2d,z_2d = o.radial_to_cart_array()
                self.ax2.plot(x_2d,y_2d, color = o.color, linestyle='dashed', linewidth=min(o.size/1.5, 1))

                plot_figure.canvas.draw_idle()

    def generate_scatter_plots_3d(self):
       
        self.scatter_plots_3d.clear()

        for o in om.celestial_objects:
            # print(f"Object {o}: size = {o.size}")
            scatter = self.ax.scatter(o.x[0],o.y[0],o.z[0], color=o.color)
            self.scatter_plots_3d.append(scatter)

    def generate_scatter_plots_2d(self, selected_id: list):

        self.scatter_plots_2d.clear()
        self.lines_true.clear()
        self.lines_ecc.clear()
        self.lines_mean.clear()
        
        self.ax2.cla()
        self.ax2.tick_params(left = False, right = False, labelleft = False, 
                labelbottom = False, bottom = False) 
       
        for o in selected_id:    
            
            scatter = self.ax2.scatter(o.x[0],o.y[0])
            self.scatter_plots_2d.append(scatter)

            line_true = self.ax2.plot(0,0, color= 'turquoise', label='True Anomaly')[0]
            self.lines_true.append(line_true)
            # line_ecc = self.ax2.plot(0,0, color = 'purple', label='Line connecting Ell.->Ecc.')[0]
            # self.lines_ecc.append(line_ecc)
            line_mean = self.ax2.plot(0,0, color ='magenta', label='Mean Anomaly')[0]
            self.lines_mean.append(line_mean)

            num = o.semimajor_axis
            self.ax2.set_xlim(-num*2,num*2)
            self.ax2.set_ylim(-num*2,num*2)
            self.ax2.legend(loc='upper right')

    def animate_manual_3d(self, f):

        frame = float(f)

        if len(om.celestial_objects) > 0:

            x = np.zeros(len(om.celestial_objects))
            y = np.zeros(len(om.celestial_objects))
            z = np.zeros(len(om.celestial_objects))
            
            for i in range(0, len(om.celestial_objects)):

                a, b, c = om.celestial_objects[i].rotate_radial_scalarDay(frame + om.celestial_objects[i].initial_angle*np.divide(1,om.celestial_objects[i].degreePerDay))
                x[i] = a[0]
                y[i] = b[0]
                z[i] = c[0]
                
                # Check if the scatter plot already exists
                if i < len(self.scatter_plots_3d):
                    # Update the existing scatter plot's data
                    self.scatter_plots_3d[i]._offsets3d=(a, b, c)
                    
                    if om.celestial_objects[i].size > 12:
                        self.scatter_plots_3d[i].set_sizes([12])
                        
                    self.scatter_plots_3d[i].set_sizes([min(om.celestial_objects[i].size*5,20)])
    
    def animate_2d(self, f, selected_id:list):
        frame = float(f)
        if len(selected_id) > 0:

            a = selected_id[0].semimajor_axis
            e = selected_id[0].eccentricity
            
            # degrees per day * days *pi/180 converts an input of days to radians
            #ac.set_anomalies(e,v,E,m,id)
            ac.set_anomalies(e,[0],[0],[selected_id[0].degreePerDay*frame*np.pi/180],"Mean Anomaly")

            # convert angles from degrees back to radians
            v = ac.get_true_anomaly()*np.pi/180
            E = ac.get_eccentric_anomaly()*np.pi/180
            m = ac.get_mean_anomaly()*np.pi/180

            r = selected_id[0].radial_scalarAngle(v + selected_id[0].initial_angle*np.pi/180)

            center_ellipse_x = -a*e
            center_ellipse_y = 0

            """
            ecc_cir_vector = [ a*cos(E), -2ae ],[a*sin(E), 0]
            m_vector = [a*cos(m)-a*e, a*e],[a*sin(m), 0]
            ecc_rad_vector = [radial(a,e,v)*cos(v), radial(a,e,v)*cos(v)], [a*sin(E),radial(a,e,v)*sin(v)]
            true_angle_vector = [0, radial(a,e,v)*cos(v)],[0, radial(a,e,v)*sin(v)]
            """

            # plot the position of the object with scatter plot
            data_2d = np.column_stack([[r*np.cos(v)], [r*np.sin(v)]])
            self.scatter_plots_2d[0].set_offsets(data_2d)
            self.scatter_plots_2d[0].set_color(selected_id[0].color)

            # plot the eccentric circle for the selected orbit
            x_2d_E = selected_id[0].semimajor_axis*(np.cos(selected_id[0].theta)-selected_id[0].eccentricity)
            y_2d_E = selected_id[0].semimajor_axis*(np.sin(selected_id[0].theta))
            self.ax2.plot(x_2d_E, y_2d_E, color = selected_id[0].color, linestyle=(0,(1,10)), linewidth=min(selected_id[0].size/1.5,1))

 
            # "Plotting a line for the eccentric anomaly"
            # ecc_cir_vector = self.ax2.plot([np.multiply(a,a*np.cos(E))-a*e,center_ellipse_x],[np.multiply(a,np.sin(E)),0], color= 'darkorange', label='Eccentric Anomaly r Vector')
            # # ecc_cir_vector = plt.plot([ a*cos(E), -2ae ],[a*sin(E), 0])
            
            # "Plotting a line for the mean anomaly"
            # # and a line is drawn out using the mean anomaly
            self.lines_mean[0].set_xdata([np.multiply(a, np.cos(m))+center_ellipse_x, center_ellipse_x])
            self.lines_mean[0].set_ydata([np.multiply(a, np.sin(m)), center_ellipse_y])
            # m_vector = ax.plot([a*cos(m)-a*e, a*e],[a*sin(m), 0])
            
            # "Plotting the line connecting the radial equation to the eccentric circle"
            # # a final line to connect the ellipse to the eccentric circle
            # self.lines_ecc[0].set_xdata([np.multiply(r,np.cos(v)), np.multiply(r, np.cos(v))])
            # self.lines_ecc[0].set_ydata([a*np.sin(E), np.multiply(r, np.sin(v))])
            # [radial(a,e,v)*cos(v), radial(a,e,v)*cos(v)],[a*sin(E),radial(a,e,v)*sin(v)]

            # "Plotting a line for the true anomaly"
            # # and a line is drawn using the angle of choice using the distance formula
            self.lines_true[0].set_xdata([0, np.multiply(r,np.cos(v))])
            self.lines_true[0].set_ydata([0 ,np.multiply(r,np.sin(v))])
            # [0, radial(a,e,v)*cos(v)],[0, radial(a,e,v)*sin(v)]
 
    def delete_animation_3d(self):
        self.anim3d._stop()
        return
            
    def delete_animation_2d(self):
        self.anim._stop()
        return
    
    def toggle_pause_3d(self):
        if self.is_paused_3d:
            self.anim3d.resume()
            # self.anim.resume()
        else:
            self.anim3d.pause()
            # self.anim3d.pause()

        self.is_paused_3d = not self.is_paused_3d
        return
    
    def toggle_pause_2d(self):
        if self.is_paused_2d:
            self.anim.resume()
            # self.anim.resume()
        else:
            self.anim.pause()
            # self.anim3d.pause()

        self.is_paused_2d = not self.is_paused_2d

    def plot_sequence_animation_2d(self, plot_figure, selected_id: list):
        
        self.is_paused_2d = False

        if len(selected_id) > 0:
            self.anim = animation.FuncAnimation(fig=plot_figure, func=self.animate_2d, fargs = (selected_id,), frames=max(8,int(365*selected_id[0].period)), interval=120)
            
        return

    def plot_sequence_animation_3d(self, plot_figure):
        
        self.is_paused_3d = False
        self.anim3d = animation.FuncAnimation(fig=plot_figure, func=self.animate_manual_3d, frames=int(365*5), interval = 120)

plot_manager = PlotManager()