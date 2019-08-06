from . import average_view
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore
from . import PandasDfTableModel
from . import process_average
from . import plot_data


class AverageVM(average_view.Ui_AverageView):

    def __init__(self, parent):
        average_view.Ui_AverageView.__init__(self)
        self.setupUi(parent)
        self.parent = parent

        # Browse button
        self.browseButton.clicked.connect(self.browse_button_click)

        # Set the number of ensembles to average
        self.num_avg_ens = self.avgNumSpinBox.value()

    def browse_button_click(self):
        """
        Button Clicked to open a file browser to select the files to playback.
        :return:
        """
        # Set the number of ensembles to average
        self.num_avg_ens = self.avgNumSpinBox.value()

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self.parent, "QFileDialog.getOpenFileNames()", "",
                                                "Ensemble Files (*.ens);;Binary Files (*.bin);;All Files (*)", options=options)

        if files:
            print(files)
            # Process the files
            #self.read_ens(files)
            self.process_avg = process_average.ProcessAverage(self.parent, files, self.num_avg_ens)
            #self.process_avg.finished.connect(self.on_finished)
            #self.process_avg.start()
            results = self.process_avg.read_ens_files(files)

            # Update the Table Views
            self.update_table_views(results)

    def update_table_views(self, results_dict):
        # Set the Tableview with the dataframe
        for avg_result_ss_config in results_dict.values():
            if not avg_result_ss_config.df_earth_east.empty:
                east_mean = avg_result_ss_config.df_earth_east.mean()
                east_std = avg_result_ss_config.df_earth_east.std()
                east_model = PandasDfTableModel.DataFrameModel(avg_result_ss_config.df_earth_east)
                east_avg_model = PandasDfTableModel.PandasDfTableModel(east_mean.to_frame().transpose())
                east_std_model = PandasDfTableModel.PandasDfTableModel(east_std.to_frame().transpose())
                self.eastTableView.setModel(east_model)
                self.eastTableView.show()
                self.eastAvgTableView.setModel(east_avg_model)
                self.eastAvgTableView.show()
                self.eastStdTableView.setModel(east_std_model)
                self.eastStdTableView.show()

                # Plot the data
                plot_thread = plot_data.PlotData(self.parent, avg_result_ss_config)
                plot_thread.start()
