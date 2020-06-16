import Dashboard
from AverageView import average_vm
from AverageView import menu_view
from bokeh.io import show
from bokeh.models import Panel, Tabs
from rti_bokeh_server import RtiBokehServer
from rti_bokeh_plot_manager import RtiBokehPlotManager
from rti_python.Utilities.config import RtiConfig


class VectorManager:

    def __init__(self, parent):
        # Set the parent
        self.parent = parent

        # Setup the Average VM
        #self.avg_vm = average_vm.AverageVM(self.parent)

        self.rti_config = RtiConfig()
        self.rti_config.init_average_waves_config()
        self.rti_config.init_terminal_config()
        self.rti_config.init_waves_config()
        self.rti_config.init_plot_server_config()

        self.plot_manager = RtiBokehPlotManager(self.rti_config)
        self.plot_manager.start()
        self.bokeh_server = RtiBokehServer(self.rti_config, self.plot_manager)

        menu = menu_view.MenuView()
        menu_panel = Panel(child=menu.get_layout(), title="menu")
        main_lo = Tabs(tabs=[menu_panel])
        #show(main_lo)

        #Dashboard
        #self.dashboard = Dashboard.Dashboard()
        #self.dashboard.start()
        #self.dashboard.app_setup()

    def set_mag_df(self, df):
        self.dashboard.set_vel_df(df)
