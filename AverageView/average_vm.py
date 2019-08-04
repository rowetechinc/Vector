
from . import average_view
from PyQt5.QtWidgets import QFileDialog
from rti_python.Utilities.read_binary_file import ReadBinaryFile
from rti_python.Post_Process.Average.AverageWaterColumn import AverageWaterColumn
from rti_python.Ensemble.Ensemble import Ensemble
from rti_python.Ensemble.EnsembleData import EnsembleData
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from . import PandasDfTableModel


class AverageVM(average_view.Ui_AverageView):

    def __init__(self, parent):
        average_view.Ui_AverageView.__init__(self)
        self.setupUi(parent)
        self.parent = parent

        # Browse button
        self.browseButton.clicked.connect(self.browse_button_click)

        # Read the binary file
        self.read_binary = ReadBinaryFile()
        self.read_binary.ensemble_event += self.process_ens

        # Process average
        self.avg_ens_dict = {}                      # Average Water Column for each subsystem config
        self.avg_count_dict = {}                    # Keep count of ensembles to average

        self.num_avg_ens = 5

        # Dataframe results
        self.df_earth_east = pd.DataFrame()
        self.df_earth_north = pd.DataFrame()
        self.df_earth_vertical = pd.DataFrame()
        self.df_earth_error = pd.DataFrame()

    def browse_button_click(self):
        """
        Button Clicked to open a file browser to select the files to playback.
        :return:
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self.parent, "QFileDialog.getOpenFileNames()", "",
                                                "Ensemble Files (*.ens);;Binary Files (*.bin);;All Files (*)", options=options)
        if files:
            print(files)
            # Process the files
            self.read_ens(files)

    def read_ens(self, files):
        """
        Read in all the data from the ENS file.
        :param files: Files to process.
        :return:
        """
        # Read the data from the files
        for ens_file in files:
            # Read in the file
            self.read_binary.playback(ens_file)

            # Set the Tableview with the dataframe
            #east_model = PandasDfTableModel.PandasDfTableModel(self.df_earth_east)
            east_mean = self.df_earth_east.mean()
            east_std = self.df_earth_east.std()
            east_model = PandasDfTableModel.DataFrameModel(self.df_earth_east)
            east_avg_model = PandasDfTableModel.PandasDfTableModel(east_mean.to_frame().transpose())
            east_std_model = PandasDfTableModel.PandasDfTableModel(east_std.to_frame().transpose())
            self.eastTableView.setModel(east_model)
            self.eastTableView.show()
            self.eastAvgTableView.setModel(east_avg_model)
            self.eastAvgTableView.show()
            self.eastStdTableView.setModel(east_std_model)
            self.eastStdTableView.show()

            # Plot the data
            east_mean.plot(kind='line', label='Mean', y=east_mean.index)
            east_std.plot(kind='line', label='STD')
            plt.legend(loc='best')
            plt.show()

    def process_ens(self, sender, ens):
        """
        Process the ENS data.  Add the ensemble to the averager.  If the configuration
        does not exist in the dictionary, add it to the dictionary.  Then accumulate
        the ensemble data.  Once the data accumulation has reached the limit, generate the
        average.
        :param sender: NOT USED
        :param ens: Ensemble data to process.
        :return:
        """
        #if ens.IsEnsembleData:
            #print(str(ens.EnsembleData.EnsembleNumber))

        # Ensemble Key
        key = self.gen_dict_key(ens)

        if key:
            # If the key does not exist, add it to the dictionary
            if key not in self.avg_ens_dict:
                self.avg_ens_dict[key] = AverageWaterColumn(self.num_avg_ens,
                                                            ens.EnsembleData.SysFirmwareSubsystemCode,
                                                            ens.EnsembleData.SubsystemConfig)
                self.avg_count_dict[key] = 0

            # Accumulate the average
            self.avg_ens_dict[key].add_ens(ens)
            self.avg_count_dict[key] = self.avg_count_dict[key] + 1

            if self.avg_count_dict[key] >= self.num_avg_ens:
                # Average the data
                avg_ens = self.avg_ens_dict[key].average()

                # Process the average data
                self.process_avg(avg_ens)

                # Reset the average and count
                self.avg_ens_dict[key].reset()
                self.avg_count_dict[key] = 0

    def process_avg(self, avg_ens):
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

            #print(self.df_earth_east.shape)
            #print(self.df_earth.head())
            #print("Average:")
            #print(self.df_earth_east.mean())
            #print("Standard Deviation Beams:")
            #print(self.df_earth_east.std())
            #print("Standard Deviation Bins:")
            #print(self.df_earth_east.std(axis=1))

        """
        if avg_ens[AverageWaterColumn.INDEX_NUM_BEAM] == 3:
            if self.df_earth.empty:
                # Create Dataframe
                self.df_earth = pd.DataFrame(avg_ens[AverageWaterColumn.INDEX_EARTH], columns=["East", "North", "Vertical"])
            else:
                # Append to dataframe
                df_earth = pd.DataFrame(avg_ens[AverageWaterColumn.INDEX_EARTH], columns=["East", "North", "Vertical"])
                self.df_earth = self.df_earth.append(df_earth, ignore_index=True)
            print(self.df_earth.shape)
            #print(self.df_earth.head())
            print("Average:")
            print(self.df_earth.mean())
            print("Standard Deviation Beams:")
            print(self.df_earth.std())
            print("Standard Deviation Bins:")
            print(self.df_earth.std(axis=1))

        if avg_ens[AverageWaterColumn.INDEX_NUM_BEAM] == 1:
            df_beam = pd.DataFrame(avg_ens[AverageWaterColumn.INDEX_BEAM], columns=["Beam0"])
            print(df_beam.shape)
            print(df_beam.head())
        """

    def gen_dict_key(self, ens):
        """
        Generate a dictionary key from the subsystem code and
        subsystem configuration.
        [ssCode_ssConfig]
        :param ens: Ensemble to get the informaton
        :return: Key for an ensemble based off configuration.
        """
        if ens.IsEnsembleData:
            ss_code = ens.EnsembleData.SysFirmwareSubsystemCode
            ss_config = ens.EnsembleData.SubsystemConfig
            return str(str(ss_code) + "_" + str(ss_config))
        else:
            return None



