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
from bokeh.models import HoverTool, Title
from bokeh.layouts import grid, column


class PlotData(QtCore.QThread):

    def __init__(self, parent, avg_result):
        QtCore.QThread.__init__(self, parent)

        self.avg_result = avg_result
        self.scale_factor_remove_gridline = 1.06
        self.earth_plot_file_name = "plot.html"
        self.bt_color = "#737373"
        self.bt_alpha = 0.85
        self.bt_line_color = "red"

    def run(self):
        # Plot the East STD and Mean
        #self.plot_mpl_avg_east_std_mean(self.avg_result.df_earth_east)
        self.plot_bokeh(self.avg_result)

    def plot_mpl_avg_east_std_mean(self, east_df):
        east_mean = east_df.mean()
        east_std = east_df.std()

        # Plot the data
        east_mean.plot(kind='line', label='Mean', y=east_mean.index)
        east_std.plot(kind='line', label='STD')
        plt.legend(loc='best')
        plt.show()

    def plot_bokeh_heatmap(self,
                           df,
                           vel_min,
                           vel_max,
                           bt_range,
                           ens_time_sec,
                           num_bins,
                           is_upward,
                           plot_title,
                           value_scale="m/s",
                           color_palette="Viridis256",
                           bt_color="#737373",
                           bt_alpha=0.85,
                           bt_line_color="red"):
        """
        Create a heatmap plot.  This will create a heatmap for velocites.  It will use the colormap
        palette to map the colors to the min and max value in the df "value" column.  If bottom track data is available,
        it will show the bottom track value.  It will flip the plot if the data is upward or downward.
        :param df: Dataframe contain a "time_stamp", "value", "bin_depth" columns.
        :param vel_min: Minimum Velocity for the color bar.
        :param vel_max: Maximum velocity for the color bar.
        :param bt_range: Bottom Track Range dataframe "time_stamp", "value" columns.
        :param ens_time_sec: Time between ensembles used to create a block size for each bin.
        :param num_bins: Number of bins.
        :param is_upward: Flag for upward or downward.
        :param plot_title: Title of the plot.
        :param value_scale: Title for the scale of the value column.  Default: m/s
        :param color_palette: Color Palette.  Default: Viridis256
        :param bt_color: Bottom Track Shade color. DEFAULT: #737373 (grey)
        :param bt_alpha: Bottom Track Shade alpha channel (transparent).  Default: 0.85
        :param bt_line_color: Bottom Track Line color.  Default: Red.
        :return: Plot figure with heatmap, bottom track line and shade and colorbar.
        """

        # Convert the east array to df
        # params: vel_array, dt, ss_code, ss_config, blank, bin_size
        # DF Columns: Index, time_stamp, ss_code, ss_config, bin_num, beam_num, bin_depth, value

        # Find the min and max value for the bin depth
        # Create a height based off the bin size
        bin_depth_min = df.bin_depth.min()
        bin_depth_max = df.bin_depth.max()
        height = ((bin_depth_max - bin_depth_min) / num_bins) * self.scale_factor_remove_gridline

        # Multiple by 1000 to get it in the same scale
        # Multiple by scale_factor to get rid of the grid line
        time_width = ens_time_sec * 1000 * self.scale_factor_remove_gridline

        # Create a mapping between min and max value and the colors
        mapper = LinearColorMapper(palette=color_palette, low=vel_min, high=vel_max)

        # Create the figure with plot title and datetime x axis
        p = figure(title=plot_title,
                   x_axis_type='datetime')

        # Create a heatmap
        p.rect(x='time_stamp',
               y='bin_depth',
               source=df,
               width=time_width,
               height=height,
               fill_color={'field': 'value', 'transform': mapper},
               line_color=None)

        # Create a Bottom Track line and shade
        # Verify at least one value is greater than 0 for the range (value column)
        # If all values are 0, then bottom track is not on
        if not bt_range.empty and bt_range.value.max() > 0:
            # Create Bottom Track Line
            # Create Y1 as the line on the bottom
            # y2 will be all the bottom track range values
            y1 = [bin_depth_max] * len(bt_range.value)
            bt_range['y1'] = [bin_depth_max] * len(bt_range.value)

            # Create the BT Line and Shaded area
            p.varea(x='time_stamp', y1='y1', y2='value', source=bt_range, fill_color=bt_color, fill_alpha=bt_alpha)              # Shaded area
            p.line(x='time_stamp', y='value', source=bt_range, line_color=bt_line_color, line_width=2, line_alpha=bt_alpha)    # Line

        # Set the plot upward or downward looking
        if is_upward:
            p.y_range.range_padding = 0                             # Upward looking
        else:
            p.y_range = Range1d(bin_depth_max, bin_depth_min)       # Downward looking
        p.x_range.range_padding = 0

        # Create a colorbar
        color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="6pt",
                             ticker=BasicTicker(desired_num_ticks=6),
                             formatter=PrintfTickFormatter(format="%.1f" + value_scale),
                             label_standoff=6, border_line_color=None, location=(0, 0))

        # Create Tooltip
        hover = HoverTool(
            tooltips=[
                ("DateTime", "@time_stamp{%Y-%m-%d %H:%M:%S}"),
                #("Value", "@value  $color[swatch]:value"),
                ("Value", "@value " + value_scale),
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

        # Add colorbar to plot
        p.add_layout(color_bar, 'right')

        return p

    def plot_bokeh_timeseries(self,
                              df,
                              is_upward,
                              plot_title,
                              value_scale="m/s"):

        # Create plot
        p = figure(title=plot_title,
                   x_axis_type='datetime')

        # Find the min and max value for the bin depth
        # Create a height based off the bin size
        bin_depth_min = df.bin_depth.min()
        bin_depth_max = df.bin_depth.max()

        # Set the data to a ColumnDataSource to use tooltips
        source = ColumnDataSource(df)

        p.line(x='time_stamp', y='value', source=source)

        # Set the plot upward or downward looking
        if is_upward:
            p.y_range.range_padding = 0                             # Upward looking
        else:
            p.y_range = Range1d(bin_depth_max, bin_depth_min)       # Downward looking
        p.x_range.range_padding = 0

        # Create Tooltip
        hover = HoverTool(
            tooltips=[
                ("DateTime", "@time_stamp{%Y-%m-%d %H:%M:%S}"),
                #("Value", "@value  $color[swatch]:value"),
                ("Value", "@value " + value_scale),
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

        return p


    def plot_bokeh(self, avg_result):
        """
        Plot the data with the given layout.
        :param avg_result: Average Results.
        :return:
        """
        # Set the variables
        df_east = avg_result.df_earth[avg_result.df_earth['beam_num'] == 0].reset_index(drop=True)
        df_north = avg_result.df_earth[avg_result.df_earth['beam_num'] == 1].reset_index(drop=True)
        df_vertical = avg_result.df_earth[avg_result.df_earth['beam_num'] == 2].reset_index(drop=True)
        df_error = avg_result.df_earth[avg_result.df_earth['beam_num'] == 3].reset_index(drop=True)
        df_mag = avg_result.df_mag
        bt_range = avg_result.df_avg_bt_range
        rt_range = avg_result.df_avg_rt_range
        df_dir = avg_result.df_dir
        ens_time_sec = avg_result.time_diff.seconds
        num_bins = avg_result.num_bins
        ss_code = avg_result.ss_code
        ss_config = avg_result.ss_config
        is_upward = avg_result.is_upward

        # Get the min and max velocity
        min_earth = avg_result.df_earth['value'].min()
        max_earth = avg_result.df_earth['value'].max()
        min_mag = avg_result.df_mag['value'].min()
        max_mag = avg_result.df_mag['value'].max()
        min_vel = min(min_earth, min_mag)
        max_vel = max(max_earth, max_mag)


        # Create the file name and output
        self.earth_plot_file_name = "plots_water_" + str(ss_code) + "_" + str(ss_config) + ".html"
        output_file(self.earth_plot_file_name)

        # Get the plots
        #mag_plot = self.plot_bokeh_mag_heatmap(mag, bt_range, ens_time_sec, num_bins, is_upward)
        #dir_plot = self.plot_bokeh_dir_heatmap(dir, bt_range, ens_time_sec, num_bins, is_upward)
        mag_plot = self.plot_bokeh_heatmap(df_mag, min_vel, max_vel, bt_range, ens_time_sec, num_bins, is_upward, "Water Velocity", "m/s")
        dir_plot = self.plot_bokeh_heatmap(df_dir, df_dir['value'].min(), df_dir['value'].max(), bt_range, ens_time_sec, num_bins, is_upward, "Water Direction", "deg")
        east_plot = self.plot_bokeh_heatmap(df_east, min_vel, max_vel, bt_range, ens_time_sec, num_bins, is_upward, "East Velocity", "m/s")
        north_plot = self.plot_bokeh_heatmap(df_north, min_vel, max_vel, bt_range, ens_time_sec, num_bins, is_upward, "North Velocity", "m/s")
        vert_plot = self.plot_bokeh_heatmap(df_vertical, df_vertical['value'].min(), df_vertical['value'].max(), bt_range, ens_time_sec, num_bins, is_upward, "Vertical Velocity", "m/s")
        error_plot = self.plot_bokeh_heatmap(df_error, df_error['value'].min(), df_error['value'].max(), bt_range, ens_time_sec, num_bins, is_upward, "Error Velocity", "m/s")

        # Check if we have bottom track range values
        if not bt_range.empty and bt_range.value.max() > 0:
            range_plot = self.plot_bokeh_timeseries(bt_range, is_upward, "Bottom Track Range", "m")

        # Check if we have range track range values
        if not rt_range.empty and rt_range.value.max() > 0:
            range_plot = self.plot_bokeh_timeseries(rt_range, is_upward, "Range Track Range", "m")

        # Add addtional title
        #p.add_layout(Title(text="Subsystem: SubsystemConfig", align="center"), "top")

        # Set the layout of the plot webpage
        lo = grid([
            [mag_plot],
            [dir_plot],
            [east_plot, north_plot],
            [vert_plot, error_plot],
            [range_plot]
            ], sizing_mode='stretch_both')

        show(lo)
