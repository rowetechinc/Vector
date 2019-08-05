import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import threading
import multiprocessing


class Dashboard(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.vel_df = pd.DataFrame()

    def run(self):
        app = self.app_setup()
        #self.start_server(app)


    def set_vel_df(self, vel_df):
        self.vel_df = vel_df

    def generate_table(self, max_rows=10):
        return html.Table(
            # Header
            [html.Tr([html.Th(col) for col in self.vel_df.columns])] +

            # Body
            [html.Tr([
                html.Td(self.vel_df.iloc[i][col]) for col in self.vel_df.columns
            ]) for i in range(min(len(self.vel_df), max_rows))]
        )

    def app_setup(self):

        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

        if not self.vel_df.empty:
            app.layout = html.Div(children=[
                html.H4(children='Velocity Magnitude'),
                self.generate_table(self.vel_df)
            ])
        else:
            app.layout = html.Div(children=[
                html.H4(children='Velocity Magnitude'),
            ])

        return app

    def start_server(self, app, **kwargs):
        def run():
            app.run_server(**kwargs)

        # Run on a separate process so that it doesn't block
        server_process = multiprocessing.Process(target=run)
        server_process.start()


if __name__ == '__main__':
    app.run_server(debug=True)