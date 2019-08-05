import pandas as pd
from rti_python.Post_Process.Average.AverageWaterColumn import AverageWaterColumn
import numpy as np


class AverageResult:

    def __init__(self):
        # Dataframe results
        self.df_earth_east = pd.DataFrame()
        self.df_earth_north = pd.DataFrame()
        self.df_earth_vertical = pd.DataFrame()
        self.df_earth_error = pd.DataFrame()

    def update_results(self, avg_ens):
        print("SS Code: " + str(avg_ens[AverageWaterColumn.INDEX_SS_CODE]))
        print("SS Config: " + str(avg_ens[AverageWaterColumn.INDEX_SS_CONFIG]))
        print("first time: " + str(avg_ens[AverageWaterColumn.INDEX_FIRST_TIME]))
        print("last time: " + str(avg_ens[AverageWaterColumn.INDEX_LAST_TIME]))
        print("Num Beams: " + str(avg_ens[AverageWaterColumn.INDEX_NUM_BEAM]))
        print("Num Bins: " + str(avg_ens[AverageWaterColumn.INDEX_NUM_BINS]))

        if avg_ens[AverageWaterColumn.INDEX_NUM_BEAM] == 4:
            # Create Dataframe
            df_earth = pd.DataFrame(avg_ens[AverageWaterColumn.INDEX_EARTH], columns=["East", "North", "Vertical", "Error"])

            # Replace bad values
            #east_array = np.array(df_earth['East'].values.tolist())                      # Faster to convert to numpy array and replace BAD_VELOCITY
            #df_earth['East'] = np.where(east_array > 88, None, east_array).tolist()      # Replace BAD_VELOCITY with None
            df_earth['East'] = self.replace_bad_val_with_none(df_earth['East'])
            df_earth['North'] = self.replace_bad_val_with_none(df_earth['North'])
            df_earth['Vertical'] = self.replace_bad_val_with_none(df_earth['Vertical'])
            df_earth['Error'] = self.replace_bad_val_with_none(df_earth['Error'])

            # Convert the bin rows to bin columns
            df_earth = df_earth.transpose()

            # Bin names
            bin_nums = []
            for bin_num in range(avg_ens[AverageWaterColumn.INDEX_NUM_BINS]):
                bin_nums.append(bin_num)

            # Set the new column names with the bin numbers
            df_earth.columns = bin_nums
            #df_earth.reindex(columns=sorted(df_earth.columns))

            # Velocities
            self.df_earth_east = self.df_earth_east.append(df_earth.loc["East"], ignore_index=True)
            self.df_earth_north = self.df_earth_north.append(df_earth.loc["North"], ignore_index=True)
            self.df_earth_vertical = self.df_earth_vertical.append(df_earth.loc["Vertical"], ignore_index=True)
            self.df_earth_error = self.df_earth_error.append(df_earth.loc["Error"], ignore_index=True)

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