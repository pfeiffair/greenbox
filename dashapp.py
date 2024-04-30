from dash import Dash, dcc, html, Input, Output, State, callback
import plotly.express as px
import pandas as pd

app = Dash(__name__)
app.layout = html.Div([
    html.Div(children=[
        #html.Label('Datenvisualisierung: Temperatur und Luftfeuchtigkeit 2 Sensoren'),
        html.H4('Datavisualisation: 2x BME280 Sensor '),
        #html.P("Temperatur:"),
        #dcc.Graph(id="time-series-chart_temp"),
        dcc.Graph(id='time-series-chart-temp', style={'width': '100vh', 'height': '40vh','padding': 5}),
        dcc.Interval(
            id='interval-component-t',
            interval=10*1000, # in milliseconds
            n_intervals=0
        ),
        dcc.Graph(id='time-series-chart-humid', style={'width': '100vh', 'height': '40vh','padding': 5}),
        dcc.Interval(
            id='interval-component-h',
            interval=10*1000, # in milliseconds
            n_intervals=0
        ),
    ], style={'width': '100vh', 'height': '100vh','padding': 5, 'flex': 1}), #SIDEBAR_STYLE  
    
    html.Div(children=[
       # html.Label('Manual controller'),
        html.H4('Control Fan and Humidifier manually'),
        html.P("Fan control:"),
        html.Div(id='container-button-basic',
                children='Enter a value in seconds and press Start'),
        html.Div(dcc.Input(id='input-on-submit', type='text')),
        html.Button('Start', id='submit-val', n_clicks=0),
        html.P("Humidifier control:"),
        html.Div(id='container-button-humid',
            children='Enter a value in seconds and press Start'),
        html.Div(dcc.Input(id='input-on-submit-humid', type='text')),
        html.Button('Start', id='submit-val-humid', n_clicks=0)
    ], style={'padding': 10,'width': '50vh', 'flex': 1})
], style={'display': 'flex', 'flexDirection': 'row'})
    # html.P("Sensor auswählen:"),
    # dcc.Dropdown(
    #     id="ticker",
    #     options=["Temp1", "Temp2"],
    #     value="Temp1",
    #     clearable=False,
    # ),

# for threading
import threading
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

# for relay control
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
RELAIS_1_GPIO = 4
RELAIS_2_GPIO = 17
RELAIS_3_GPIO = 27
RELAIS_4_GPIO = 22

#GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
       
# Turn on / off Relais 1
def R1on():
    GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
    print("R1 on")
    GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on
    #	GPIO.cleanup()  
def R1off():
    GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
    print("R1 off")
    GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # off
# Turn on / off Relais 2
def R2on():
	GPIO.setup(RELAIS_2_GPIO, GPIO.OUT) # GPIO Assign mode
	print("R2 on")
	GPIO.output(RELAIS_2_GPIO, GPIO.HIGH) # on

def R2off():
	GPIO.setup(RELAIS_2_GPIO, GPIO.OUT) # GPIO Assign mode
	print("R2 off")
	GPIO.output(RELAIS_2_GPIO, GPIO.LOW) # off

# Turn on / off Relais 3
def R3on():
	GPIO.setup(RELAIS_3_GPIO, GPIO.OUT) # GPIO Assign mode
	print("R3 on")
	GPIO.output(RELAIS_3_GPIO, GPIO.HIGH) # on

def R3off():
	GPIO.setup(RELAIS_3_GPIO, GPIO.OUT) # GPIO Assign mode
	print("R3 off")
	GPIO.output(RELAIS_3_GPIO, GPIO.LOW) # off

# Turn on / off Relais 4
def R4on():
	GPIO.setup(RELAIS_4_GPIO, GPIO.OUT) # GPIO Assign mode
	print("R4 on")
	GPIO.output(RELAIS_4_GPIO, GPIO.HIGH) # on

def R4off():
	GPIO.setup(RELAIS_4_GPIO, GPIO.OUT) # GPIO Assign mode
	print("R4 off")
	GPIO.output(RELAIS_4_GPIO, GPIO.LOW) # off

# load Data
def loaddata():
    df = pd.read_csv('sensor_readings_bme280_long.csv')
    df["date"] = pd.to_datetime(df["date"],dayfirst=True) 
    return df

# Fan
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

    return 'Fan running for {} secondsand the button has been clicked {} times'.format(
        value,
        n_clicks
    )

# Humidifier
@callback(
    Output('container-button-humid', 'children'),
    Input('submit-val-humid', 'n_clicks'),
    State('input-on-submit-humid', 'value'),
    prevent_initial_call=True
)
def update_output(n_clicks, value):
    
  
    def humidon(duration=30):
        print("Humindifier on for "+ str(duration) +" seconds")
        R2on()
        time.sleep(2)
        R3on()
        time.sleep(1)
        R3off()
        time.sleep(duration)
        R2off()
        print("Humindifier off")
    
    run_threaded(humidon(duration=int(value)))
    return 'Humidifier is running for {} seconds and the button has been clicked {} times'.format(
        value,
        n_clicks
    )


@app.callback(
    Output("time-series-chart-temp", "figure"), 
   # Output("time-series-chart_temp", "figure"), 
   Input('interval-component-t', 'n_intervals'))

def display_time_series(ticker):
        
    df = loaddata()
    # selecting rows based on condition
    df = df[((df['type'] == 'Temp1') | (df['type'] == 'Temp2'))]
    
    fig = px.line(df, x="date", y="value", color = "type", 
                    labels=dict(date="Time", value="Temperature (°C)", type="Sensor"))
                    #range_x=['2024-04-30','2024-05-01'],)
    fig.update_xaxes(rangeslider_visible=True, 
                     rangeselector=dict(
                        buttons=list([
                        dict(count=10, label="10 mim", step="minute", stepmode="backward"),
                        dict(count=2, label="2 h", step="hour", stepmode="backward"),
                        dict(count=12, label="12 h", step="hour", stepmode="todate"),
                        dict(count=2, label="2 days", step="day", stepmode="backward"),
                        dict(step="all") ]))
                    )
    fig.update_layout(title_text="Temperature in °C",
                  title_font_size=30)#,
                  #yaxis_range=[17,25])
    fig.update_yaxes(minor_tickmode="auto")
    fig.update_yaxes(nticks=5)
    #fig.update_yaxes(minor_tickvals=["18","19","20"])
    #fig.update_layout(uirevision="fix")
    #fig.update_layout(newshape_showlegend=False)
    #fig.update_layout(newshape_label_text="<VALUE>")
    #fig.update_layout(showlegend=False)
    #fig.update_layout(legend_title_text="")
    #fig.update_layout(legend_title_side="top")
    fig['layout']['uirevision'] = 'some-constant'
    
    return fig

@app.callback(
    Output("time-series-chart-humid", "figure"),
    Input('interval-component-h', 'n_intervals'))

def display_time_series(ticker):
    df = loaddata()
    # selecting rows based on condition
    df = df[((df['type'] == 'Humid1') | (df['type'] == 'Humid2'))]
    
    fig = px.line(df, x="date", y="value", color = "type",labels=dict(date="Time", value="Humidity (%)", type="Sensor"))

    fig.update_layout(title_text="Humidity in %",
                  title_font_size=30,
                  yaxis_range=[30,100])
    fig.update_yaxes(minor_tickmode="auto")
    fig.update_yaxes(nticks=8)
    fig.update_xaxes(rangeslider_visible=True, 
                     rangeselector=dict(
                        buttons=list([
                        dict(count=10, label="10 mim", step="minute", stepmode="backward"),
                        dict(count=2, label="2 h", step="hour", stepmode="backward"),
                        dict(count=12, label="12 h", step="hour", stepmode="todate"),
                        dict(count=2, label="2 days", step="day", stepmode="backward"),
                        dict(step="all") ]))
                    )
    fig['layout']['uirevision'] = 'some-constant'
    return fig

app.run_server(debug=True)