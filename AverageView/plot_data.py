from bokeh.io import show
from bokeh.models import LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
import matplotlib.pyplot as plt
from PyQt5 import QtCore


class PlotData(QtCore.QThread):

    def __init__(self, parent, avg_result):
        QtCore.QThread.__init__(self, parent)

        self.avg_result = avg_result

    def run(self):
        # Plot the East STD and Mean
        #self.plot_mpl_avg_east_std_mean(self.avg_result.df_earth_east)
        self.plot_bokeh_avg_east_heatmap(self.avg_result.df_earth_east)

    def plot_mpl_avg_east_std_mean(self, east_df):
        east_mean = east_df.mean()
        east_std = east_df.std()

        # Plot the data
        east_mean.plot(kind='line', label='Mean', y=east_mean.index)
        east_std.plot(kind='line', label='STD')
        plt.legend(loc='best')
        plt.show()

    def plot_bokeh_avg_east_heatmap(self, east_df):

        source = ColumnDataSource(east_df)

        p = figure()
        p.rect(source=source, title='East Velocity Average', stat=None)
        show(p)
