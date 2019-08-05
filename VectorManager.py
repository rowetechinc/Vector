import Dashboard
from AverageView import average_vm


class VectorManager:

    def __init__(self, parent):
        # Set the parent
        self.parent = parent

        # Setup the Average VM
        self.avg_vm = average_vm.AverageVM(self.parent)

        #Dashboard
        #self.dashboard = Dashboard.Dashboard()
        #self.dashboard.start()
        #self.dashboard.app_setup()

    def set_mag_df(self, df):
        self.dashboard.set_vel_df(df)
