from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.animation as animation
import random
from SensorDataProvidersFactoryTest import SensorDataProvidersFactoryTest
from SensorDataProvidersFactory import SensorDataProvidersFactory
import threading
import time

class EventPlotter:

    def __init__(self, sensors):
    # TODO: identify sensors by id not by type

        self.values_list = {}
        # self.subplots = []
        self.x = 0.0
        self.xmin = 0.0
        self.xmax = 5.0
        self.sensor_num = len(sensors)

        for sensor in sensors:
            self.values_list[sensor.type] = zeros(0)

        # Sent for figure
        font = {'size'   : 9}
        matplotlib.rc('font', **font)
        self.event_plot = {}
        ax_cols = 1
        ax_rows = 1

        # Setup figure and subplots
        self.f0 = figure(num = 0, figsize = (12, 8))#, dpi = 100)
        self.f0.suptitle("Oscillation decay", fontsize=12)


        # if sensors_num > 1:
        #     ax_cols = 2
        # if sensors_num > 2:
        #     ax_rows = int((sensors_num + 1)/2)

        # initialize subplots for every sensor

        self.t = zeros(0)

        row = 0
        for sensor in sensors:
            curr_subplot = subplot2grid((self.sensor_num, 1), (row, 0))
            curr_subplot.set_title(sensor.type + "::" + sensor.name)
            curr_subplot.set_ylim(0, 200);
            curr_subplot.set_xlim(0,5.0)
            curr_subplot.grid(True)
            curr_subplot.set_xlabel("time")
            curr_subplot.set_ylabel(sensor.type)

            self.event_plot[sensor.type], = curr_subplot.plot(self.t, self.values_list.get(sensor.type), 'b-', label=sensor.type)
            # p011, = ax01.plot(t,yp1,'b-', label="yp1")

            row += 1





        # Data Update


    def updatePlottingData(self,i):
        for cur_key, cur_value in self.values_list.items():
            self.event_plot[cur_key].set_data(self.t, cur_value)
            print(self.t)
            # self.values_list[key]



            # self.event_plot['temperature'].set_data(self.t, self.values_list.get('temperature'))
            # self.event_plot['humidity'].set_data(self.t, self.values_list.get('temperature'))
            # self.event_plot['pressure'].set_data(self.t, self.values_list.get('pressure'))


            # if self.x >= self.xmax-1.00:
            #     self.event_plot[key].axes.set_xlim(self.x - self.xmax+1.0, self.x+1.0)





    def plot(self):

        simulation = animation.FuncAnimation(self.f0, self.updatePlottingData, blit=False, frames=100, interval=10, repeat=True)
        plt.show()

    def update(self, sensor_values):
            for key,value in sensor_values.items():
                self.values_list[key] = append(self.values_list[key], value)
            self.t = append(self.t, self.x)
            self.x += 0.05


    def sensors_data(self,sensors):
        values = {}
        while(True):
            for sensor in sensors:
                values[sensor.type] = sensor.get_data()
            self.update(values)
            time.sleep(0.1)

sensors = []
virt_temp = SensorDataProvidersFactoryTest.get_data_provider('virtual', 'temperature')
virt_hum = SensorDataProvidersFactoryTest.get_data_provider('virtual', 'humidity')
pot = SensorDataProvidersFactory.get_data_provider('Potentiometer', 'angle')


sensors.append(virt_temp)
sensors.append(virt_hum)
sensors.append(pot)



plotter = EventPlotter(sensors)
thread = threading.Thread(target=plotter.sensors_data, args=[sensors])
thread.start()

plotter.plot()
# plotter_thread = threading.Thread(target=plotter.plot)
# plotter_thread.start()



