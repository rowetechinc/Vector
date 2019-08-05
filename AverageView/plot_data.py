from bokeh.io import show
from bokeh.models import LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
import matplotlib.pyplot as plt
from PyQt5 import QtCore
from rti_python.Ensemble.Ensemble import Ensemble
from rti_python.Post_Process.Average.AverageWaterColumn import AverageWaterColumn


class PlotData(QtCore.QThread):

    def __init__(self, parent, avg_result):
        QtCore.QThread.__init__(self, parent)

        self.avg_result = avg_result

    def run(self):
        # Plot the East STD and Mean
        #self.plot_mpl_avg_east_std_mean(self.avg_result.df_earth_east)
        self.plot_bokeh_avg_east_heatmap(self.avg_result.df_earth, self.avg_result.time_diff.seconds)

    def plot_mpl_avg_east_std_mean(self, east_df):
        east_mean = east_df.mean()
        east_std = east_df.std()

        # Plot the data
        east_mean.plot(kind='line', label='Mean', y=east_mean.index)
        east_std.plot(kind='line', label='STD')
        plt.legend(loc='best')
        plt.show()

    def plot_bokeh_avg_east_heatmap(self, earth_vel, ens_time_sec):
        # Convert the east array to df
        # params: vel_array, dt, ss_code, ss_config, blank, bin_size
        # DF Columns: Index, time_stamp, ss_code, ss_config, bin_num, beam_num, bin_depth, value

        # Select just the East value
        df_east = earth_vel[earth_vel['beam_num'] == 0].reset_index(drop=True)

        # Create a mapping between min and max value and the colors
        mapper = LinearColorMapper(palette="Viridis256", low=df_east.value.min(), high=df_east.value.max())

        p = figure(title="East Velocity",
                   x_axis_type='datetime',
                   tooltips=[("DateTime", "@time_stamp"),
                             #("Value", "@value  $color[swatch]:value"),
                             ("Value", "@value m/s"),
                             ("Depth", "@bin_depth m"),
                             ("Bin", "@bin_num"),
                             ("SS Code", "@ss_code"),
                             ("SS Config", "@ss_config")])

        p.rect(x='time_stamp', y='bin_depth', source=df_east, width=50000, height=1,
               fill_color={'field': 'value', 'transform': mapper})

        color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="6pt",
                             ticker=BasicTicker(desired_num_ticks=6),
                             formatter=PrintfTickFormatter(format="%.1fm/s"),
                             label_standoff=6, border_line_color=None, location=(0, 0))

        #p.hover.tooltips = [
        #    ("DateTime", "@time_stamp"),
        #    ("Value", "@value  $color[swatch]:value"),
        #    ("Value", "@value"),
        #    ("Depth", "@bin_depth"),
        #    ("Bin", "@bin_num"),
        #    ("SS Code", "@ss_code"),
        #    ("SS Config", "@ss_config"),
        #]

        p.add_layout(color_bar, 'right')

        output_file("avg_east_vel.html")

        show(p)
