import dash
from dash import html, dcc, Input, Output
from dash.dependencies import State
from ftplib import FTP
import pandas as pd
import io

app = dash.Dash(__name__)

# Layout for the FTP connection window
ftp_layout = html.Div([
    html.H1("FTP Connection"),
    html.Label("FTP Server:"),
    dcc.Input(id='ftp-server-input', type='text', value='ftp.example.com'),
    html.Label("Username:"),
    dcc.Input(id='ftp-username-input', type='text', value='your_username'),
    html.Label("Password:"),
    dcc.Input(id='ftp-password-input', type='password', value='your_password'),
    html.Button('Connect', id='ftp-connect-button'),
    html.Div(id='ftp-status')
])

# Layout for the graph display window
graph_layout = html.Div([
    html.H1("Graph Display"),
    dcc.Graph(id='graph-display'),
    html.Div(id='graph-status')
])

# Connect to FTP server and retrieve CSV data
@app.callback(
    Output('ftp-status', 'children'),
    Output('graph-display', 'figure'),
    Output('graph-status', 'children'),
    Input('ftp-connect-button', 'n_clicks'),
    State('ftp-server-input', 'value'),
    State('ftp-username-input', 'value'),
    State('ftp-password-input', 'value')
)
def connect_to_ftp(n_clicks, server, username, password):
    if n_clicks is None:
        return '', dash.no_update, ''

    try:
        # Establish FTP connection
        ftp = FTP(server)
        ftp.login(user=username, passwd=password)

        # Replace 'your_file.csv' with the actual filename on the FTP server
        file_path = 'your_file.csv'

        # Download CSV file
        data = io.BytesIO()
        ftp.retrbinary(f"RETR {file_path}", data.write)
        data.seek(0)

        # Read CSV data into a DataFrame
        df = pd.read_csv(data)

        # Plot graph
        fig = {
            'data': [
                {'x': df['x'], 'y': df['y'], 'type': 'scatter', 'mode': 'lines+markers', 'name': 'Data'}
            ],
            'layout': {
                'title': 'Graph from FTP CSV',
                'xaxis': {'title': 'X-axis'},
                'yaxis': {'title': 'Y-axis'}
            }
        }

        return f"Connected to {server}", fig, ''
    except Exception as e:
        return f"Error: {str(e)}", dash.no_update, ''

# Define the app layout using the FTP and graph layouts
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='FTP Connection', children=[ftp_layout]),
        dcc.Tab(label='Graph Display', children=[graph_layout]),
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
