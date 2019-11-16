import Dashboard
from AverageView import average_vm
from AverageView import menu_view
from bokeh.io import show
from bokeh.models import Panel, Tabs


class VectorManager:

    def __init__(self, parent):
        # Set the parent
        self.parent = parent

        # Setup the Average VM
        #self.avg_vm = average_vm.AverageVM(self.parent)

        menu = menu_view.MenuView()
        menu_panel = Panel(child=menu.get_layout(), title="menu")
        main_lo = Tabs(tabs=[menu_panel])
        show(main_lo)

        #Dashboard
        #self.dashboard = Dashboard.Dashboard()
        #self.dashboard.start()
        #self.dashboard.app_setup()

    def set_mag_df(self, df):
        self.dashboard.set_vel_df(df)
