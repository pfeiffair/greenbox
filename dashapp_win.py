################################################################
# Packages
###############################################################

from dash import Dash, dcc, html, Input, Output, State, callback
import plotly.express as px
import pandas as pd
import sys
import threading
import time

################################################################
# Check for Raspberry Pi and GPIO Initialization
###############################################################

# Check if RPi module is available
if 'RPi' in sys.modules:
    # Import GPIO module for Raspberry Pi
    import RPi.GPIO as GPIO
    # Set GPIO mode
    GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
    # Define GPIO pins for relay control
    RELAIS_1_GPIO = 4
    RELAIS_2_GPIO = 17
    RELAIS_3_GPIO = 27
    RELAIS_4_GPIO = 22
else:
    # If RPi module is not available, set GPIO to None
    GPIO = None

################################################################
# Dash App Initialization
###############################################################

# Initialize Dash app
app = Dash(__name__)

# Define app layout
app.layout = html.Div([
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
    ], style={'width': '100vh', 'height': '100vh','padding': 5, 'flex': 1}), 

    ################################################################
    # Manual Control Section
    ###############################################################

    html.Div(children=[
        html.H4('Control Fan and Humidifier Manually'),

        # Fan Control
        html.P("Fan control:"),
        html.Div(id='container-button-basic', children='Enter a value in seconds and press Start'),
        html.Div(dcc.Input(id='input-on-submit', type='text')),
        html.Button('Start', id='submit-val', n_clicks=0),

        # Humidifier Control
        html.P("Humidifier control:"),
        html.Div(id='container-button-humid', children='Enter a value in seconds and press Start'),
        html.Div(dcc.Input(id='input-on-submit-humid', type='text')),
        html.Button('Start', id='submit-val-humid', n_clicks=0),

        # Camera Image
        html.Img(src=app.get_asset_url('cam.png'), id='campic')
    ], style={'padding': 10,'width': '50vh', 'flex': 1})
], style={'display': 'flex', 'flexDirection': 'row'})

################################################################
# Helper Functions
###############################################################

# Function to run a job in a separate thread
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

################################################################
# Relay Control Functions
###############################################################

# Function to turn on Relay 1
def R1on():
    if GPIO:
        GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
        print("R1 on")
        GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on

# Function to turn off Relay 1
def R1off():
    if GPIO:
        GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
        print("R1 off")
        GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # off

# Function to turn on Relay 2
def R2on():
    if GPIO:
        GPIO.setup(RELAIS_2_GPIO, GPIO.OUT) # GPIO Assign mode
        print("R2 on")
        GPIO.output(RELAIS_2_GPIO, GPIO.HIGH) # on

# Function to turn off Relay 2
def R2off():
    if GPIO:
        GPIO.setup(RELAIS_2_GPIO, GPIO.OUT) # GPIO Assign mode
        print("R2 off")
        GPIO.output(RELAIS_2_GPIO, GPIO.LOW) # off

# Function to turn on Relay 3
def R3on():
    if GPIO:
        GPIO.setup(RELAIS_3_GPIO, GPIO.OUT) # GPIO Assign mode
        print("R3 on")
        GPIO.output(RELAIS_3_GPIO, GPIO.HIGH) # on

# Function to turn off Relay 3
def R3off():
    if GPIO:
        GPIO.setup(RELAIS_3_GPIO, GPIO.OUT) # GPIO Assign mode
        print("R3 off")
        GPIO.output(RELAIS_3_GPIO, GPIO.LOW) # off

# Function to turn on Relay 4
def R4on():
    if GPIO:
        GPIO.setup(RELAIS_4_GPIO, GPIO.OUT) # GPIO Assign mode
        print("R4 on")
        GPIO.output(RELAIS_4_GPIO, GPIO.HIGH) # on

# Function to turn off Relay 4
def R4off():
    if GPIO:
        GPIO.setup(RELAIS_4_GPIO, GPIO.OUT) # GPIO Assign mode
        print("R4 off")
        GPIO.output(RELAIS_4_GPIO, GPIO.LOW) # off

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

# Fan Control Callback
@callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value'),
    prevent_initial_call=True
)
def update_output(n_clicks, value):
       
    def windon(duration = 30):
        print("Wind on for " + str(duration)+ " seconds")
        R1on()
        time.sleep(duration)
        R1off()
    
    windon(duration=int(value))

    return 'Fan running for {} seconds and the button has been clicked {} times'.format(value, n_clicks)

# Humidifier Control Callback
@callback(
    Output('container-button-humid', 'children'),
    Input('submit-val-humid', 'n_clicks'),
    State('input-on-submit-humid', 'value'),
    prevent_initial_call=True
)
def update_output(n_clicks, value):
    
  
    def humidon(duration=30):
        print("Humidifier on for "+ str(duration) +" seconds")
        R2on()
        time.sleep(2)
        R3on()
        time.sleep(1)
        R3off()
        time.sleep(duration)
        R2off()
        print("Humidifier off")
    
    run_threaded(humidon(duration=int(value)))
    return 'Humidifier is running for {} seconds and the button has been clicked {} times'.format(value, n_clicks)

# Temperature Chart Update Callback
@app.callback(
    Output("time-series-chart-temp", "figure"), 
    Input('interval-component-t', 'n_intervals'))
def display_time_series(ticker):
    df = loaddata()
    df = df[((df['type'] == 'Temp1') | (df['type'] == 'Temp2'))]
    
    fig = px.line(df, x="date", y="value", color = "type", 
                    labels=dict(date="Time", value="Temperature (°C)", type="Sensor"))
    fig.update_xaxes(rangeselector=dict(
                        buttons=list([
                        dict(count=10, label="10 mim", step="minute", stepmode="backward"),
                        dict(count=2, label="2 h", step="hour", stepmode="backward"),
                        dict(count=12, label="12 h", step="hour", stepmode="todate"),
                        dict(count=2, label="2 days", step="day", stepmode="backward"),
                        dict(step="all") ])))
    fig.update_layout(title_text="Temperature in °C", title_font_size=30)
    fig.update_layout(uirevision="fix")
    return fig

# Humidity Chart Update Callback
@app.callback(
    Output("time-series-chart-humid", "figure"),
    Input('interval-component-humid', 'n_intervals'))
def display_time_series(ticker):
    df = loaddata()
    df = df[((df['type'] == 'Humid1') | (df['type'] == 'Humid2'))]
    
    fig = px.line(df, x="date", y="value", color = "type",labels=dict(date="Time", value="Humidity (%)", type="Sensor"))
    fig.update_layout(title_text="Humidity in %", title_font_size=30, yaxis_range=[30,100])
    fig.update_yaxes(nticks=8)
    fig.update_xaxes(rangeslider_visible=True, 
                     rangeselector=dict(
                        buttons=list([
                        dict(count=10, label="10 mim", step="minute", stepmode="todate"),
                        dict(count=2, label="2 h", step="hour", stepmode="todate"),
                        dict(count=12, label="12 h", step="hour", stepmode="todate"),
                        dict(count=2, label="2 days", step="day", stepmode="todate"),
                        dict(step="all") ])))
    fig['layout']['uirevision'] = 'some-constant'
    return fig

# Vapor Pressure Deficit Chart Update Callback
@app.callback(
    Output("time-series-chart-vpd", "figure"),
    Input('interval-component-vpd', 'n_intervals'))
def display_time_series(ticker):
    df = loaddata()
    df = df[((df['type'] == 'vpd1') | (df['type'] == 'vpd2'))]
    fig = px.line(df, x="date", y="value", color = "type",labels=dict(date="Time", value="VPD", type="Sensor"))
    fig.update_layout(title_text="Vapor Pressure Deficit", title_font_size=30)
    fig.update_yaxes(nticks=8)
    fig.update_xaxes(rangeslider_visible=True, 
                     rangeselector=dict(
                        buttons=list([
                        dict(count=10, label="10 mim", step="minute", stepmode="backward"),
                        dict(count=2, label="2 h", step="hour", stepmode="backward"),
                        dict(count=12, label="12 h", step="hour", stepmode="todate"),
                        dict(count=2, label="2 days", step="day", stepmode="backward"),
                        dict(step="all") ])))
    fig['layout']['uirevision'] = 'some-constant'
    return fig

# Run the Dash app
app.run_server(debug=True)
