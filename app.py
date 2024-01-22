import dash
from dash import html, dcc, Input, Output
import dash_daq as daq
from dash.dependencies import State
from common.ftp import FTP
from infos import capteur
import pandas as pd

app = dash.Dash(__name__)

# Layout for the FTP connection window
ftp_layout = html.Div(
    children=[
            html.H1("FTP Connection"),
            html.Label("FTP Server:"),
            dcc.Input(id='ftp-server-input', type='text', value='mafreebox.freebox.fr'),
            html.Label("Username:"),
            dcc.Input(id='ftp-username-input', type='text', value='freebox'),
            html.Label("Password:"),
            dcc.Input(id='ftp-password-input', type='password', value='your_password'),
            html.Button('Connect', id='ftp-connect-button'),
            html.Div(id='ftp-status', children='Not connected yet')
    ],
    style={
        'backgroundColor': 'lightgrey',
        'border': 'thin lightgrey solid',
        'border-radius': '5px',
        'padding': '5px',
        'marginTop': '10px',
    }
)

# Layout for the graph display window
data_layout = html.Div(
    children=[
        html.H1("Data Display"),html.Br(),
        # cycle counter and operation time display 50% width
        html.Div(id='cycle-counter', children=[
            html.H2("Cycle counter"),html.Br(),
            daq.LEDDisplay(
                id='our-LED-display',
                value="0",
                color="#FF5E5E",
                backgroundColor="lightgrey",
            )
        ]),
        html.Div(id='operation-time', children=[
            html.H2("Operation time"),html.Br(),
            html.Time(
                id='time-display',
                children='00:00:00', 
                style={
                    'fontSize': 30,
                    'textAlign': 'center'
            })
        ]),html.Br(),
        html.Div(id='average-activity', children=[
            html.H2("Average activity"),html.Br(),
            html.Time(
                id='time-average-display',
                children='00:00:00', 
                style={
                    'fontSize': 30,
                    'textAlign': 'center'
            })
        ]),html.Br(),
        html.H2("Average activity per hour"),html.Br(),
        dcc.Graph(id='graph-display'),html.Br(),
        html.H2("Activity per day"),html.Br(),
        dcc.Graph(id='graph-display2'),html.Br(),
        html.Div(id='graph-status')
    ],
    style={
        'textAlign': 'center',
        'border': 'thin lightgrey solid',
        'border-radius': '5px',
        'padding': '5px',
        'marginTop': '10px',
    }
)

# Connect to FTP server and retrieve CSV data
@app.callback(
    [Output('ftp-status', 'children'),
     Output('graph-display', 'figure'),
     Output('graph-display2', 'figure'),
     Output('time-display', 'children'),
     Output('our-LED-display', 'value'),
     Output('time-average-display', 'children'),
     Output('graph-status', 'children')],
    [Input('ftp-connect-button', 'n_clicks')],
    [State('ftp-server-input', 'value'),
     State('ftp-username-input', 'value'),
     State('ftp-password-input', 'value')]
)
def connect_to_ftp(n_clicks, server, username, password):
    if n_clicks is None:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    try:
        # Establish FTP connection
        ftp = FTP(passwd=password, user=username, ip=server, link=capteur["capteur_1"]["link"], file_id=capteur["capteur_1"]["file_id"])
        ftp.download()

        # Read CSV data into a DataFrame
        df = pd.read_csv("output/" + capteur["capteur_1"]["file_id"])

        cycles = df["activity"].sum()
        # each digit is a LED
        value = str(cycles)

        df["timestamp"] = pd.to_datetime(df["time"], format="%Y-%m-%d %H:%M:%S")
        df.drop(columns=["time"])
        df["diff"] = df["timestamp"].diff().fillna(pd.Timedelta(seconds=0))
        df["diff"] = df["diff"].where(df["activity"] == 0, pd.Timedelta(seconds=0))
        duree_totale = df["diff"].sum()

        df2 = df.groupby(df["timestamp"].dt.date).count()
        df2 = df2["activity"].where(df2["activity"] != 0)
        df2 = df2.reset_index()

        fig2 = {
            'data': [
                {'x': df2["timestamp"], 'y': df2["activity"], 'type': 'line', 'name': 'Activity per day'},
            ],
            'layout': {
                'xaxis': {
                    'title': 'Day'
                },
                'yaxis': {
                    'title': 'Number of cycles'
                },
                'plot_bgcolor': 'lightgrey',
                'paper_bgcolor': 'lightgrey'
            },
        }

        # Display total operation time
        hours = duree_totale.seconds // 3600 + duree_totale.days * 24
        minutes = (duree_totale.seconds % 3600) // 60
        seconds = duree_totale.seconds % 60
        time = f"{hours}:{minutes}:{seconds}"
        
        diff = df[df["activity"] == 0]
        moy = diff["diff"].mean()
        hours = moy.seconds // 3600
        minutes = (moy.seconds % 3600) // 60
        seconds = moy.seconds % 60
        time_average = f"{hours}:{minutes}:{seconds}"


        df["hour"] = df["timestamp"].dt.hour
        df["day"] = df["timestamp"].dt.day

        df2 = df.groupby(["day", "hour"]).count()
        df2 = df2["activity"]
        df2 = df2.reset_index()
        df2 = df2["activity"].groupby(df2["hour"]).mean()

        # Plot graph
        fig = {
            'data': [
                {'x': df2.index, 'y': df2, 'type': 'bar', 'name': 'Average activity per hour'},
            ],
            'layout': {
                'xaxis': {
                    'title': 'Hour'
                },
                'yaxis': {
                    'title': 'Number of cycles'
                },
                'plot_bgcolor': 'lightgrey',
                'paper_bgcolor': 'lightgrey'
            },
        }

        return f"Connected to {server}", fig, fig2, time, value, time_average, ''
    except Exception as e:
        return f"Error: {str(e)}", dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

# Define the app layout using the FTP and graph layouts
app.layout = html.Div(
    children=[
    dcc.Tabs([
        dcc.Tab(label='FTP Connection', children=[ftp_layout]),
        dcc.Tab(label='Data Display', children=[data_layout]),
    ])
    ],
    style={
        'width': '100%',
        'height': '100%',
        'margin': '0 auto',
        'backgroundColor': 'lightgrey',
        'border': 'thin lightgrey solid'
    }
)

if __name__ == '__main__':
    app.run_server(debug=True)
