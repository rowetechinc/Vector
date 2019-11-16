from bokeh.models import Panel, Tabs, CustomJS
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models.widgets import FileInput, Dropdown
from bokeh.layouts import grid


class MenuView:

    def __init__(self):
        self.file_input = self.create_file_input()
        self.main_menu = self.create_menu()

    def create_menu(self):
        menu = [("Item 1", "item_1"), ("Item 2", "item_2"), None, ("Item 3", "item_3")]
        dropdown = Dropdown(label="Dropdown button", button_type="warning", menu=menu)
        return dropdown

    def create_file_input(self, para=None):
        file_input = FileInput(accept=".ens,.bin")

        callback = CustomJS(args=dict(para=para, file_input=file_input), code="""
            para.text = "<p><b>filename:</b> " + file_input.filename  + \
                        "<p><b>number of lines:</b> " + atob(file_input.value).split('\\n').length
        """)

        #file_input.js_on_change('value', callback)
        file_input.on_change('value', self.select_file_handler)
        return file_input

    def select_file_handler(self, attr, old, new):
        print("fit data upload succeeded")
        print(new)

    def get_layout(self):
        lo = grid([[self.file_input],
                   [self.main_menu]],
                   sizing_mode='stretch_both')

        return lo

