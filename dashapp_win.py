################################################################
# Packages
###############################################################

from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

################################################################
# Dash App Initialization
###############################################################

# Initialize Dash app
app = Dash(__name__)

# Define app layout
app.layout = html.Div([
    # Navigation Tabs
    dcc.Tabs(id='tabs', value='tab-realtime', children=[
        dcc.Tab(label='Realtime View', value='tab-realtime'),
        dcc.Tab(label='Historic View', value='tab-historic'),
        dcc.Tab(label='Config', value='tab-config'),
        dcc.Tab(label='Misc', value='tab-misc'),
    ]),
    
    # Content of the tabs
    html.Div(id='tabs-content')
])

################################################################
# Data Loading Function
###############################################################

# Function to load data from CSV
def loaddata():
    df = pd.read_csv('sensor_readings_bme280_long.csv')
    df["date"] = pd.to_datetime(df["date"],dayfirst=True) 
    return df

################################################################
# Callbacks
###############################################################

# Callback to update the content based on the selected tab
@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-realtime':
        return html.Div(children=[
            ################################################################
            # Visualization Section
            ###############################################################

            html.Div(children=[
                html.H4('Data Visualization: 2x BME280 Sensors'),

                # Temperature Chart
                dcc.Graph(id='time-series-chart-temp', style={'width': '100vh', 'height': '40vh','padding': 5}),
                dcc.Interval(id='interval-component-t', interval=10*1000, n_intervals=0),

                # Humidity Chart
                dcc.Graph(id='time-series-chart-humid', style={'width': '100vh', 'height': '40vh','padding': 5}),
                dcc.Interval(id='interval-component-humid', interval=10*1000, n_intervals=0),

                # Vapor Pressure Deficit Chart
                dcc.Graph(id='time-series-chart-vpd', style={'width': '100vh', 'height': '40vh','padding': 5}),
                dcc.Interval(id='interval-component-vpd', interval=10*1000, n_intervals=0),
            ], style={'width': '100vh', 'height': '100vh','padding': 5, 'flex': 1})
        ])
    elif tab == 'tab-historic':
        return html.Div(children=[
            html.H4('Historic View')
            # Add your content for Historic View here
        ])
    elif tab == 'tab-config':
        return html.Div(children=[
            html.H4('Config')
            # Add your content for Config here
        ])
    elif tab == 'tab-misc':
        return html.Div(children=[
            html.H4('Misc')
            # Add your content for Misc here
        ])

# Callback to update the Temperature Chart
@app.callback(
    Output("time-series-chart-temp", "figure"), 
    Input('interval-component-t', 'n_intervals'))
def display_time_series_temp(ticker):
    df = loaddata()
    df = df[((df['type'] == 'Temp1') | (df['type'] == 'Temp2'))]
    
    fig = px.line(df, x="date", y="value", color="type", 
                  labels=dict(date="Time", value="Temperature (°C)", type="Sensor"))
    fig.update_xaxes(rangeselector=dict(
        buttons=list([
            dict(count=10, label="10 mim", step="minute", stepmode="backward"),
            dict(count=2, label="2 h", step="hour", stepmode="backward"),
            dict(count=12, label="12 h", step="hour", stepmode="todate"),
            dict(count=2, label="2 days", step="day", stepmode="backward"),
            dict(step="all") 
        ])
    ))
    fig.update_layout(title_text="Temperature in °C", title_font_size=30)
    fig.update_layout(uirevision="fix")
    return fig

# Callback to update the Humidity Chart
@app.callback(
    Output("time-series-chart-humid", "figure"),
    Input('interval-component-humid', 'n_intervals'))
def display_time_series_humid(ticker):
    df = loaddata()
    df = df[((df['type'] == 'Humid1') | (df['type'] == 'Humid2'))]
    
    fig = px.line(df, x="date", y="value", color="type",
                  labels=dict(date="Time", value="Humidity (%)", type="Sensor"))
    fig.update_layout(title_text="Humidity in %", title_font_size=30, yaxis_range=[30,100])
    fig.update_yaxes(nticks=8)
    fig.update_xaxes(rangeslider_visible=True, 
                     rangeselector=dict(
                         buttons=list([
                             dict(count=10, label="10 mim", step="minute", stepmode="todate"),
                             dict(count=2, label="2 h", step="hour", stepmode="todate"),
                             dict(count=12, label="12 h", step="hour", stepmode="todate"),
                             dict(count=2, label="2 days", step="day", stepmode="todate"),
                             dict(step="all") 
                         ])
                     ))
    fig['layout']['uirevision'] = 'some-constant'
    return fig

# Callback to update the Vapor Pressure Deficit Chart
@app.callback(
    Output("time-series-chart-vpd", "figure"),
    Input('interval-component-vpd', 'n_intervals'))
def display_time_series_vpd(ticker):
    df = loaddata()
    df = df[((df['type'] == 'vpd1') | (df['type'] == 'vpd2'))]
    
    fig = px.line(df, x="date", y="value", color="type",
                  labels=dict(date="Time", value="VPD", type="Sensor"))
    fig.update_layout(title_text="Vapor Pressure Deficit", title_font_size=30)
    fig.update_yaxes(nticks=8)
    fig.update_xaxes(rangeslider_visible=True, 
                     rangeselector=dict(
                         buttons=list([
                             dict(count=10, label="10 mim", step="minute", stepmode="backward"),
                             dict(count=2, label="2 h", step="hour", stepmode="backward"),
                             dict(count=12, label="12 h", step="hour", stepmode="todate"),
                             dict(count=2, label="2 days", step="day", stepmode="backward"),
                             dict(step="all") 
                         ])
                     ))
    fig['layout']['uirevision'] = 'some-constant'
    return fig

# Run the Dash app
app.config.suppress_callback_exceptions = True
app.run_server(debug=True)
