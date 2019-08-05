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

        if avg_ens[AverageWaterColumn.INDEX_NUM_BEAM] == 4:
            #if self.df_earth_east.empty:
            # Create Dataframe
            df_earth = pd.DataFrame(avg_ens[AverageWaterColumn.INDEX_EARTH], columns=["East", "North", "Vertical", "Error"])

            east_array = np.array(df_earth['East'].values.tolist())                      # Faster to convert to numpy array and replace BAD_VELOCITY
            df_earth['East'] = np.where(east_array > 88, None, east_array).tolist()      # Replace BAD_VELOCITY with None

            # Convert the bin rows to bin columns
            df_earth = df_earth.transpose()

            # East Velocities
            east_series = df_earth.loc["East"]

            self.df_earth_east = self.df_earth_east.append(east_series, ignore_index=True)
            self.df_earth_north = self.df_earth_north.append(df_earth.loc["North"], ignore_index=True)
            self.df_earth_vertical = self.df_earth_vertical.append(df_earth.loc["Vertical"], ignore_index=True)
            self.df_earth_error = self.df_earth_error.append(df_earth.loc["Error"], ignore_index=True)

