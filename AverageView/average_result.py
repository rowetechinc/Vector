import pandas as pd
from rti_python.Post_Process.Average.AverageWaterColumn import AverageWaterColumn
import numpy as np
from rti_python.Ensemble.Ensemble import Ensemble
import time


class AverageResult:

    def __init__(self):
        # Dataframe results
        self.df_earth_east = pd.DataFrame()
        self.df_earth_north = pd.DataFrame()
        self.df_earth_vertical = pd.DataFrame()
        self.df_earth_error = pd.DataFrame()
        self.df_earth = pd.DataFrame()              # Accumulate the earth data
        self.df_mag = pd.DataFrame()                # Accumulate the mag data
        self.df_dir = pd.DataFrame()                # Accumulate the dir data
        self.df_bt_range = pd.DataFrame()           # Accumulate the BT Range
        self.df_avg_bt_range = pd.DataFrame()       # Accumulate the Average Bottom Track Range
        self.prev_dt = None                         # Track ensemble time differences
        self.time_diff = 1                          # Initialize to 1 second
        self.num_bins = 1                           # Initialize number of bins
        self.ss_code = ""                           # Initialize the code
        self.ss_config = 0                          # Initialize the config
        self.is_upward = False                      # Orientation of the ADCP

    def update_results(self, awc):
        #print("SS Code: " + str(awc[AverageWaterColumn.INDEX_SS_CODE]))
        #print("SS Config: " + str(awc[AverageWaterColumn.INDEX_SS_CONFIG]))
        #print("first time: " + str(awc[AverageWaterColumn.INDEX_FIRST_TIME]))
        #print("last time: " + str(awc[AverageWaterColumn.INDEX_LAST_TIME]))
        #print("Num Beams: " + str(awc[AverageWaterColumn.INDEX_NUM_BEAM]))
        #print("Num Bins: " + str(awc[AverageWaterColumn.INDEX_NUM_BINS]))

        if awc[AverageWaterColumn.INDEX_NUM_BEAM] == 4:
            # Create Dataframe
            df_earth = pd.DataFrame(awc[AverageWaterColumn.INDEX_EARTH], columns=["East", "North", "Vertical", "Error"])

            # Replace bad values
            df_earth['East'] = self.replace_bad_val_with_none(df_earth['East'])
            df_earth['North'] = self.replace_bad_val_with_none(df_earth['North'])
            df_earth['Vertical'] = self.replace_bad_val_with_none(df_earth['Vertical'])
            df_earth['Error'] = self.replace_bad_val_with_none(df_earth['Error'])

            # Convert the bin rows to bin columns
            df_earth = df_earth.transpose()

            # Bin names
            bin_nums = []
            for bin_num in range(awc[AverageWaterColumn.INDEX_NUM_BINS]):
                bin_nums.append(bin_num)

            # Set the new column names with the bin numbers
            df_earth.columns = bin_nums
            #df_earth.reindex(columns=sorted(df_earth.columns))

            # Velocities
            self.df_earth_east = self.df_earth_east.append(df_earth.loc["East"], ignore_index=True)
            self.df_earth_north = self.df_earth_north.append(df_earth.loc["North"], ignore_index=True)
            self.df_earth_vertical = self.df_earth_vertical.append(df_earth.loc["Vertical"], ignore_index=True)
            self.df_earth_error = self.df_earth_error.append(df_earth.loc["Error"], ignore_index=True)

        # Accumulate the velocity data
        self.accum_earth_vel(awc)

        # Accumulate the mag data
        self.accum_mag_dir(awc)

        # Accumulate the mag data
        self.accum_bt_range(awc)

        # Set the latest number of bins
        self.num_bins = awc[AverageWaterColumn.INDEX_NUM_BINS]

        # Set the latest ss_code
        self.ss_code = awc[AverageWaterColumn.INDEX_SS_CODE]

        # Set the latest ss_config
        self.ss_config = awc[AverageWaterColumn.INDEX_SS_CONFIG]

        # Get the latest time diff
        if not self.prev_dt:
            self.prev_dt = awc[AverageWaterColumn.INDEX_LAST_TIME]
        else:
            self.time_diff = awc[AverageWaterColumn.INDEX_LAST_TIME] - self.prev_dt
            self.prev_dt = awc[AverageWaterColumn.INDEX_LAST_TIME]

        # Set Orientation
        self.is_upward = awc[AverageWaterColumn.INDEX_IS_UPWARD]

        #self.time_diff = awc[AverageWaterColumn.INDEX_LAST_TIME] - awc[AverageWaterColumn.INDEX_FIRST_TIME]

    def accum_earth_vel(self, awc):
        """
        Create the Earth Velocity dataframe.  This takes all the information
        from the earth velocity and creates a row in the dataframe for each bin,beam value.
        :param awc: Average data.
        :return:
        """
        # Convert the east array to df
        # params: vel_array, dt, ss_code, ss_config, blank, bin_size
        # DF Columns: Index, time_stamp, ss_code, ss_config, bin_num, beam_num, bin_depth, value
        df = Ensemble.array_2d_to_df(awc[AverageWaterColumn.INDEX_EARTH],
                                     awc[AverageWaterColumn.INDEX_LAST_TIME],
                                     awc[AverageWaterColumn.INDEX_SS_CODE],
                                     awc[AverageWaterColumn.INDEX_SS_CONFIG],
                                     awc[AverageWaterColumn.INDEX_BLANK],
                                     awc[AverageWaterColumn.INDEX_BIN_SIZE])

        # Store the results
        if self.df_earth.empty:
            self.df_earth = df
        else:
            self.df_earth = pd.concat([self.df_earth, df], ignore_index=True)

    def accum_mag_dir(self, awc):
        """
        Create the Magnitude dataframe.  This takes all the information
        from the Magnitude and creates a row in the dataframe for each bin,beam value.
        :param awc: Average data.
        :return:
        """
        # Convert the east array to df
        # params: vel_array, dt, ss_code, ss_config, blank, bin_size
        # DF Columns: Index, time_stamp, ss_code, ss_config, bin_num, beam_num, bin_depth, value
        df_mag = Ensemble.array_1d_to_df(awc[AverageWaterColumn.INDEX_MAG],
                                         awc[AverageWaterColumn.INDEX_LAST_TIME],
                                         awc[AverageWaterColumn.INDEX_SS_CODE],
                                         awc[AverageWaterColumn.INDEX_SS_CONFIG],
                                         awc[AverageWaterColumn.INDEX_BLANK],
                                         awc[AverageWaterColumn.INDEX_BIN_SIZE])

        # Store the mag results
        if self.df_mag.empty:
            self.df_mag = df_mag
        else:
            self.df_mag = pd.concat([self.df_mag, df_mag])

        df_dir = Ensemble.array_1d_to_df(awc[AverageWaterColumn.INDEX_DIR],
                                         awc[AverageWaterColumn.INDEX_LAST_TIME],
                                         awc[AverageWaterColumn.INDEX_SS_CODE],
                                         awc[AverageWaterColumn.INDEX_SS_CONFIG],
                                         awc[AverageWaterColumn.INDEX_BLANK],
                                         awc[AverageWaterColumn.INDEX_BIN_SIZE])

        # Store the dir results
        if self.df_dir.empty:
            self.df_dir = df_dir
        else:
            self.df_dir = pd.concat([self.df_dir, df_dir], ignore_index=True)

    def accum_bt_range(self, awc):
        """
        Create the Magnitude dataframe.  This takes all the information
        from the Magnitude and creates a row in the dataframe for each bin,beam value.
        :param awc: Average data.
        :return:
        """
        # Convert the east array to df
        # params: vel_array, dt, ss_code, ss_config, blank, bin_size
        # DF Columns: Index, time_stamp, ss_code, ss_config, bin_num, beam_num, bin_depth, value
        df = Ensemble.array_beam_1d_to_df(awc[AverageWaterColumn.INDEX_BT_RANGE],
                                          awc[AverageWaterColumn.INDEX_LAST_TIME],
                                          awc[AverageWaterColumn.INDEX_SS_CODE],
                                          awc[AverageWaterColumn.INDEX_SS_CONFIG])

        # Store the range results
        if self.df_bt_range.empty:
            self.df_bt_range = df
        else:
            self.df_bt_range = pd.concat([self.df_bt_range, df], ignore_index=True)

        #Average the Bottom Track Range
        avg_range = Ensemble.get_avg_range(awc[AverageWaterColumn.INDEX_BT_RANGE])

        # Create a dict entry
        dict_result = {}
        dict_result[0] = {'time_stamp': awc[AverageWaterColumn.INDEX_LAST_TIME],
                          'ss_code': awc[AverageWaterColumn.INDEX_SS_CODE],
                          'ss_config': awc[AverageWaterColumn.INDEX_SS_CONFIG],
                          'bin_num': 0,
                          'beam_num': 0,
                          'bin_depth': avg_range,
                          'value': avg_range}

        # Create the dataframe from the dictionary
        # important to set the 'orient' parameter to "index" to make the keys as rows
        df = pd.DataFrame.from_dict(dict_result, "index")

        # Store the range results
        if self.df_avg_bt_range.empty:
            self.df_avg_bt_range = df
        else:
            self.df_avg_bt_range = pd.concat([self.df_avg_bt_range, df], ignore_index=True)

    def replace_bad_val_with_none(self, df):
        """
        Replace the BAD VALUE 88.888 with NONE.
        This way the plots will not process the data as a high value.

        Converting to a numpy was faster than doing it through the dataframe.

        :param df: Data frame to replace values.
        :return: Dataframe with no bad values.
        """
        df_as_array = np.array(df.values.tolist())                      # Faster to convert to numpy array and replace BAD_VELOCITY
        return np.where(df_as_array > 88, None, df_as_array).tolist()   # Replace BAD_VELOCITY with None