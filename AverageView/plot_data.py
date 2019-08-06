from bokeh.io import show
from bokeh.models import LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models import Range1d
import matplotlib.pyplot as plt
from PyQt5 import QtCore
from rti_python.Ensemble.Ensemble import Ensemble
from rti_python.Post_Process.Average.AverageWaterColumn import AverageWaterColumn
from bokeh.models import HoverTool
from bokeh.layouts import grid, column


class PlotData(QtCore.QThread):

    def __init__(self, parent, avg_result):
        QtCore.QThread.__init__(self, parent)

        self.avg_result = avg_result

    def run(self):
        # Plot the East STD and Mean
        #self.plot_mpl_avg_east_std_mean(self.avg_result.df_earth_east)
        self.plot_bokeh(self.avg_result.df_earth,
                        self.avg_result.df_mag,
                        self.avg_result.df_dir,
                        self.avg_result.time_diff.seconds,
                        self.avg_result.num_bins)


    def plot_mpl_avg_east_std_mean(self, east_df):
        east_mean = east_df.mean()
        east_std = east_df.std()

        # Plot the data
        east_mean.plot(kind='line', label='Mean', y=east_mean.index)
        east_std.plot(kind='line', label='STD')
        plt.legend(loc='best')
        plt.show()

    def plot_bokeh_avg_earth_east_heatmap(self, earth_vel, ens_time_sec, num_bins):
        # Convert the east array to df
        # params: vel_array, dt, ss_code, ss_config, blank, bin_size
        # DF Columns: Index, time_stamp, ss_code, ss_config, bin_num, beam_num, bin_depth, value

        # Select just the East value
        df_east = earth_vel[earth_vel['beam_num'] == 0].reset_index(drop=True)

        bin_depth_min = df_east.bin_depth.min()
        bin_depths_max = df_east.bin_depth.max()
        height = (bin_depths_max - bin_depth_min) / num_bins

        time_width = ens_time_sec * 1000

        # Create a mapping between min and max value and the colors
        mapper = LinearColorMapper(palette="Viridis256", low=earth_vel.value.min(), high=earth_vel.value.max())

        plot = figure(title="East Velocity",
                   x_axis_type='datetime')

        plot.rect(x='time_stamp', y='bin_depth', source=df_east, width=time_width, height=height,
               fill_color={'field': 'value', 'transform': mapper})

        plot.x_range.range_padding = plot.y_range.range_padding = 0

        color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="6pt",
                             ticker=BasicTicker(desired_num_ticks=6),
                             formatter=PrintfTickFormatter(format="%.1fm/s"),
                             label_standoff=6, border_line_color=None, location=(0, 0))

        hover = HoverTool(
            tooltips=[
                ("DateTime", "@time_stamp{%Y-%m-%d %H:%M:%S}"),
                #("Value", "@value  $color[swatch]:value"),
                ("Value", "@value m/s"),
                ("Depth", "@bin_depth m"),
                ("Bin", "@bin_num"),
                ("SS Code", "@ss_code"),
                ("SS Config", "@ss_config")
            ],
            formatters={
                'time_stamp': 'datetime'
            },
        )
        plot.add_tools(hover)

        plot.add_layout(color_bar, 'right')

        return plot

    def plot_bokeh_avg_earth_north_heatmap(self, earth_vel, ens_time_sec, num_bins):
        # Convert the east array to df
        # params: vel_array, dt, ss_code, ss_config, blank, bin_size
        # DF Columns: Index, time_stamp, ss_code, ss_config, bin_num, beam_num, bin_depth, value

        # Select just the North value
        df_north = earth_vel[earth_vel['beam_num'] == 1].reset_index(drop=True)

        bin_depth_min = df_north.bin_depth.min()
        bin_depths_max = df_north.bin_depth.max()
        height = (bin_depths_max - bin_depth_min) / num_bins

        time_width = ens_time_sec * 1000

        # Create a mapping between min and max value and the colors
        mapper = LinearColorMapper(palette="Viridis256", low=earth_vel.value.min(), high=earth_vel.value.max())

        plot = figure(title="North Velocity",
                   x_axis_type='datetime')

        plot.rect(x='time_stamp', y='bin_depth', source=df_north, width=time_width, height=height,
               fill_color={'field': 'value', 'transform': mapper})

        plot.x_range.range_padding = plot.y_range.range_padding = 0

        color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="6pt",
                             ticker=BasicTicker(desired_num_ticks=6),
                             formatter=PrintfTickFormatter(format="%.1fm/s"),
                             label_standoff=6, border_line_color=None, location=(0, 0))

        hover = HoverTool(
            tooltips=[
                ("DateTime", "@time_stamp{%Y-%m-%d %H:%M:%S}"),
                #("Value", "@value  $color[swatch]:value"),
                ("Value", "@value m/s"),
                ("Depth", "@bin_depth m"),
                ("Bin", "@bin_num"),
                ("SS Code", "@ss_code"),
                ("SS Config", "@ss_config")
            ],
            formatters={
                'time_stamp': 'datetime'
            },
        )
        plot.add_tools(hover)

        plot.add_layout(color_bar, 'right')

        return plot

    def plot_bokeh_avg_earth_vertical_heatmap(self, earth_vel, ens_time_sec, num_bins):
        # Convert the east array to df
        # params: vel_array, dt, ss_code, ss_config, blank, bin_size
        # DF Columns: Index, time_stamp, ss_code, ss_config, bin_num, beam_num, bin_depth, value

        # Select just the East value
        df_vertical = earth_vel[earth_vel['beam_num'] == 2].reset_index(drop=True)

        bin_depth_min = df_vertical.bin_depth.min()
        bin_depths_max = df_vertical.bin_depth.max()
        height = (bin_depths_max - bin_depth_min) / num_bins

        time_width = ens_time_sec * 1000

        # Create a mapping between min and max value and the colors
        mapper = LinearColorMapper(palette="Viridis256", low=earth_vel.value.min(), high=earth_vel.value.max())

        plot = figure(title="Vertical Velocity",
                   x_axis_type='datetime')

        plot.rect(x='time_stamp', y='bin_depth', source=df_vertical, width=time_width, height=height,
               fill_color={'field': 'value', 'transform': mapper})

        plot.x_range.range_padding = plot.y_range.range_padding = 0

        color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="6pt",
                             ticker=BasicTicker(desired_num_ticks=6),
                             formatter=PrintfTickFormatter(format="%.1fm/s"),
                             label_standoff=6, border_line_color=None, location=(0, 0))

        hover = HoverTool(
            tooltips=[
                ("DateTime", "@time_stamp{%Y-%m-%d %H:%M:%S}"),
                #("Value", "@value  $color[swatch]:value"),
                ("Value", "@value m/s"),
                ("Depth", "@bin_depth m"),
                ("Bin", "@bin_num"),
                ("SS Code", "@ss_code"),
                ("SS Config", "@ss_config")
            ],
            formatters={
                'time_stamp': 'datetime'
            },
        )
        plot.add_tools(hover)

        plot.add_layout(color_bar, 'right')

        return plot

    def plot_bokeh_mag_heatmap(self, mag, ens_time_sec, num_bins):
        # Convert the east array to df
        # params: vel_array, dt, ss_code, ss_config, blank, bin_size
        # DF Columns: Index, time_stamp, ss_code, ss_config, bin_num, beam_num, bin_depth, value

        bin_depth_min = mag.bin_depth.min()
        bin_depths_max = mag.bin_depth.max()
        height = (bin_depths_max - bin_depth_min) / num_bins

        time_width = ens_time_sec * 1000

        # Create a mapping between min and max value and the colors
        mapper = LinearColorMapper(palette="Viridis256", low=mag.value.min(), high=mag.value.max())

        p = figure(title="Water Velocity",
                   x_axis_type='datetime')

        p.rect(x='time_stamp', y='bin_depth', source=mag, width=time_width, height=height,
               fill_color={'field': 'value', 'transform': mapper})

        p.x_range.range_padding = p.y_range.range_padding = 0

        color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="6pt",
                             ticker=BasicTicker(desired_num_ticks=6),
                             formatter=PrintfTickFormatter(format="%.1fm/s"),
                             label_standoff=6, border_line_color=None, location=(0, 0))

        hover = HoverTool(
            tooltips=[
                ("DateTime", "@time_stamp{%Y-%m-%d %H:%M:%S}"),
                #("Value", "@value  $color[swatch]:value"),
                ("Value", "@value m/s"),
                ("Depth", "@bin_depth m"),
                ("Bin", "@bin_num"),
                ("SS Code", "@ss_code"),
                ("SS Config", "@ss_config")
            ],
            formatters={
                'time_stamp': 'datetime'
            },
        )
        p.add_tools(hover)

        p.add_layout(color_bar, 'right')

        return [p]

    def plot_bokeh_dir_heatmap(self, dir, ens_time_sec, num_bins):
        # Convert the east array to df
        # params: vel_array, dt, ss_code, ss_config, blank, bin_size
        # DF Columns: Index, time_stamp, ss_code, ss_config, bin_num, beam_num, bin_depth, value

        bin_depth_min = dir.bin_depth.min()
        bin_depths_max = dir.bin_depth.max()
        height = (bin_depths_max - bin_depth_min) / num_bins

        time_width = ens_time_sec * 1000

        # Create a mapping between min and max value and the colors
        mapper = LinearColorMapper(palette="Viridis256", low=dir.value.min(), high=dir.value.max())

        p = figure(title="Water Direction",
                   x_axis_type='datetime')

        p.rect(x='time_stamp', y='bin_depth', source=dir, width=time_width, height=height,
               fill_color={'field': 'value', 'transform': mapper})

        p.x_range.range_padding = p.y_range.range_padding = 0

        color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="6pt",
                             ticker=BasicTicker(desired_num_ticks=6),
                             formatter=PrintfTickFormatter(format="%.1f deg"),
                             label_standoff=6, border_line_color=None, location=(0, 0))

        hover = HoverTool(
            tooltips=[
                ("DateTime", "@time_stamp{%Y-%m-%d %H:%M:%S}"),
                #("Value", "@value  $color[swatch]:value"),
                ("Value", "@value m/s"),
                ("Depth", "@bin_depth m"),
                ("Bin", "@bin_num"),
                ("SS Code", "@ss_code"),
                ("SS Config", "@ss_config")
            ],
            formatters={
                'time_stamp': 'datetime'
            },
        )
        p.add_tools(hover)

        p.add_layout(color_bar, 'right')

        return [p]

    def plot_bokeh(self, earth_vel, mag, dir, ens_time_sec, num_bins):
        """
        Plot the data with the given layout.
        :param earth_vel:
        :param mag:
        :param ens_time_sec:
        :param num_bins:
        :return:
        """

        output_file("plots.html")

        # Get the plots
        mag_plot = self.plot_bokeh_mag_heatmap(mag, ens_time_sec, num_bins)
        dir_plot = self.plot_bokeh_dir_heatmap(dir, ens_time_sec, num_bins)
        east_plot = self.plot_bokeh_avg_earth_east_heatmap(earth_vel, ens_time_sec, num_bins)
        north_plot = self.plot_bokeh_avg_earth_north_heatmap(earth_vel, ens_time_sec, num_bins)
        vert_plot = self.plot_bokeh_avg_earth_vertical_heatmap(earth_vel, ens_time_sec, num_bins)

        lo = grid([
            mag_plot,
            dir_plot,
            [east_plot, north_plot, vert_plot]
            ], sizing_mode='stretch_both')

        show(lo)