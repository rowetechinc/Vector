from PyQt5.QtCore import QThread
from rti_python.Utilities.read_binary_file import ReadBinaryFile
from rti_python.Post_Process.Average.AverageWaterColumn import AverageWaterColumn
from . import average_result
import pandas as pd
import logging
from obsub import event


class ProcessAverage:

    def __init__(self, parent, file_paths, num_avg_ens):
        #QThread.__init__(self, parent)

        self.file_paths = file_paths

        # Read the binary file
        self.read_binary = ReadBinaryFile()
        self.read_binary.ensemble_event += self.process_ens         # Process the ensemble
        self.read_binary.file_progress += self.read_file_progress   # Monitor the file progress

        # Process average
        self.avg_ens_dict = {}                      # Average Water Column for each subsystem config
        self.avg_count_dict = {}                    # Keep count of ensembles to average

        self.num_avg_ens = num_avg_ens

        # Dataframe results
        self.results_dict = {}

        self.earth_df = None

    def run(self):
        # Process the files
        self.read_ens_files(self.file_paths)

        return self.results_dict

    def read_ens_files(self, files):
        """
        Read in all the data from the ENS file.
        :param files: Files to process.
        :return:
        """
        # Read the data from the files
        for ens_file in files:
            # Read in the file
            self.read_binary.playback(ens_file)

        return self.results_dict

    @event
    def file_progress(self, bytes_read, total_bytes, ens_file_path):
        """
        Monitor the file progress.  This will give the current number of bytes read, the total bytes
        and the file name.
        :param bytes_read: Bytes read.
        :param total_bytes: Total bytes in file.
        :param ens_file_path: File path.
        :return:
        """
        logging.debug("ProcessAverage: Bytes Read: " + str(bytes_read) + " - Total Bytes: " + str(total_bytes) + " -- " + ens_file_path)

    def read_file_progress(self, sender, bytes_read, total_bytes, ens_file_path):
        """
        Pass the file progress along to the next object.
        :param sender:
        :param bytes_read: Bytes read.
        :param total_bytes: Total bytes.
        :param ens_file_path: File path
        :return:
        """
        self.file_progress(bytes_read, total_bytes, ens_file_path)

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
        # if ens.IsEnsembleData:
        # print(str(ens.EnsembleData.EnsembleNumber))

        # Ensemble Key
        key = self.gen_dict_key(ens)

        if key:
            # If the key does not exist, add it to the dictionary
            if key not in self.avg_ens_dict:
                self.avg_ens_dict[key] = AverageWaterColumn(self.num_avg_ens,
                                                            ens.EnsembleData.SysFirmwareSubsystemCode,
                                                            ens.EnsembleData.SubsystemConfig)
                self.avg_count_dict[key] = 0
                self.results_dict[key] = average_result.AverageResult()

            # Accumulate the average
            self.avg_ens_dict[key].add_ens(ens)
            self.avg_count_dict[key] = self.avg_count_dict[key] + 1

            if self.avg_count_dict[key] >= self.num_avg_ens:
                # Average the data
                avg_ens = self.avg_ens_dict[key].average()

                # Process the average data
                self.results_dict[key].update_results(avg_ens)
                # self.process_avg(key, avg_ens)

                # Reset the average and count
                self.avg_ens_dict[key].reset()
                self.avg_count_dict[key] = 0

    def process_avg(self, key, avg_ens):
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
