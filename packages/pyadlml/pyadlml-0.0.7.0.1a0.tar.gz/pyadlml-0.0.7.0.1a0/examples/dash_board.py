import argparse
import dash_bootstrap_components as dbc
import dash
from dask.distributed import Client, LocalCluster


try:
    import pyadlml
except:
    import sys
    from pathlib import Path
    sys.path.append(str(Path.cwd()))

from pyadlml.constants import TIME, START_TIME, END_TIME, ACTIVITY
from pyadlml.dataset import set_data_home
from pyadlml.dataset.plotly.dashboard import dashboard, create_callbacks
from pyadlml.dataset.util import fetch_data_by_string


"""
Example application:
 On how to use the dash-board 
 Link: http://127.0.0.1:8050/

 Add ...:/path/to/pyadlml/examples/:... to the PYTHONPATH

"""



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset', type=str, default='amsterdam')
    parser.add_argument('-i', '--identifier', type=str)
    parser.add_argument('-p', '--port', type=str, default='8050')
    parser.add_argument('-dh', '--data-home', type=str, default='/tmp/pyadlml/')
    args = parser.parse_args()

    from pandarallel import pandarallel
    pandarallel.initialize()

    # Setup dask
    #cluster = LocalCluster(n_workers=12)
    #client = Client(cluster)

    # Setup data
    set_data_home(args.data_home)
    data = fetch_data_by_string(args.dataset, identifier=args.identifier)

    # Create global variables
    df_acts = data.df_activities
    df_devs = data.df_devices

    # Determine plot dimensions based on #devices and #activities

    start_time = min(df_devs[TIME].iloc[0], df_acts[START_TIME].iloc[0])
    end_time = max(df_devs[TIME].iloc[-1], df_acts[END_TIME].iloc[-1])
    start_time = start_time.floor('D')
    end_time = end_time.ceil('D')

    # Initialize graph and functions
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    dashboard(app, args.dataset, True, df_acts, df_devs, start_time, end_time)


    print('Start server under: http://127.0.0.1:8050/')
    debug = True
    app.run(debug=debug, host='127.0.0.1', port=args.port)
