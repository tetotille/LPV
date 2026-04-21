import pyqtgraph as pg

class MotorPlots:
    def __init__(self, speed_limit, temp_limit):
        self.speed_plot = pg.PlotWidget(title="Velocidad (RPM)")
        self.temp_plot = pg.PlotWidget(title="Temperatura (°C)")
        self.speed_curve = self.speed_plot.plot(pen='r')
        self.temp_curve = self.temp_plot.plot(pen='b')

        self.speed_limit_line = pg.InfiniteLine(pos=speed_limit, angle=0, pen='r', label='Límite')
        self.speed_plot.addItem(self.speed_limit_line)

        self.temp_limit_line = pg.InfiniteLine(pos=temp_limit, angle=0, pen='b', label='Límite')
        self.temp_plot.addItem(self.temp_limit_line)

    def update_limits(self, speed_limit, temp_limit):
        self.speed_limit_line.setPos(speed_limit)
        self.temp_limit_line.setPos(temp_limit)

    def update_data(self, x_values, speed_values, temp_values):
        self.speed_curve.setData(x_values, speed_values)
        self.temp_curve.setData(x_values, temp_values)