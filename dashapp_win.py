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
    df["date"] = pd.to_datetime(df["date"], dayfirst=True) 
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

            # Current Sensor Values in Row 1
            html.Div(children=[
                # Temperature Values in A1
                html.Div(id='current-temp-values', style={'width': '33%', 'display': 'inline-block', 'background-color': 'red', 'color': 'white', 'font-size': '20px', 'text-align': 'center'}),
                # Humidity Values in B1
                html.Div(id='current-humid-values', style={'width': '33%', 'display': 'inline-block', 'background-color': 'blue', 'color': 'white', 'font-size': '20px', 'text-align': 'center'}),
                # VPD Values in C1
                html.Div(id='current-vpd-values', style={'width': '33%', 'display': 'inline-block', 'background-color': 'green', 'color': 'white', 'font-size': '20px', 'text-align': 'center'}),
            ], style={'width': '100%', 'display': 'flex', 'justify-content': 'center'}),
            
            # Second row for additional sensor values
            html.Div(children=[
                html.Div(id='current-temp-values2', style={'width': '33%', 'display': 'inline-block', 'background-color': 'red', 'color': 'white', 'font-size': '20px', 'text-align': 'center'}),
                html.Div(id='current-humid-values2', style={'width': '33%', 'display': 'inline-block', 'background-color': 'blue', 'color': 'white', 'font-size': '20px', 'text-align': 'center'}),
                html.Div(id='current-vpd-values2', style={'width': '33%', 'display': 'inline-block', 'background-color': 'green', 'color': 'white', 'font-size': '20px', 'text-align': 'center'}),
            ], style={'width': '100%', 'display': 'flex', 'justify-content': 'center'}),
            
            # Placeholder Text in Row 3
            html.Div(children=[
                html.Div(children='Test', style={'width': '33%', 'display': 'inline-block'}),
                html.Div(children='Test', style={'width': '33%', 'display': 'inline-block'}),
                html.Div(children='Test', style={'width': '33%', 'display': 'inline-block'}),
            ], style={'width': '100%', 'display': 'flex', 'justify-content': 'center'}),
            
            # Temperature Chart in Row 4, Column A
            dcc.Graph(id='time-series-chart-temp', style={'width': '33%', 'display': 'inline-block'}),
            dcc.Interval(id='interval-component-t', interval=10*1000, n_intervals=0),
            
            # Humidity Chart in Row 4, Column B
            dcc.Graph(id='time-series-chart-humid', style={'width': '33%', 'display': 'inline-block'}),
            dcc.Interval(id='interval-component-humid', interval=10*1000, n_intervals=0),
            
            # Vapor Pressure Deficit Chart in Row 4, Column C
            dcc.Graph(id='time-series-chart-vpd', style={'width': '33%', 'display': 'inline-block'}),
            dcc.Interval(id='interval-component-vpd', interval=10*1000, n_intervals=0),
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
    fig.update_layout(title_text="Temperature in °C", title_font_size=16, title_x=0.5)
    fig.update_yaxes(title=None)
    fig.update_xaxes(tickangle=0)
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                thickness=0.05,  # Hier wird die Dicke des Rangesliders in vertikaler Richtung festgelegt
            )
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="center", x=0.5) # Legende zentral ausrichten
    )
    fig.update_layout(
        xaxis_title="Time",
        legend_title="Sensor"
    )
    fig.update_layout(uirevision="fix")
    
    # Neu: Breite des Div-Elements anpassen
    fig.update_layout(width=500)
    
    # Neu: Buttons unterhalb der Grafik
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=10, label="10 mim", step="minute", stepmode="backward"),
                    dict(count=2, label="2 h", step="hour", stepmode="backward"),
                    dict(count=12, label="12 h", step="hour", stepmode="todate"),
                    dict(count=2, label="2 days", step="day", stepmode="backward"),
                    dict(step="all") 
                ]),
                x=0.1,
                y=-0.2, # Positionierung der Buttons unterhalb der Grafik
                xanchor='left',
                yanchor='bottom',
                bgcolor='rgba(0,0,0,0)'
            ),
            showticklabels=False, # Die ursprünglichen Buttons über der Grafik ausblenden
        )
    )
    
    # Neu: Graph etwas nach links verschieben
    fig.update_layout(margin=dict(l=50))
    
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
    fig.update_layout(title_text="Humidity in %", title_font_size=16, title_x=0.5, yaxis_range=[30,100])
    fig.update_yaxes(title=None)
    fig.update_xaxes(tickangle=0)
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
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                thickness=0.05,  # Hier wird die Dicke des Rangesliders in vertikaler Richtung festgelegt
            )
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="center", x=0.5) # Legende zentral ausrichten
    )
    fig.update_layout(
        xaxis_title="Time",
        legend_title="Sensor"
    )
    fig['layout']['uirevision'] = 'some-constant'
    
    # Neu: Breite des Div-Elements anpassen
    fig.update_layout(width=500)
    
    # Neu: Buttons unterhalb der Grafik
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=10, label="10 mim", step="minute", stepmode="todate"),
                    dict(count=2, label="2 h", step="hour", stepmode="todate"),
                    dict(count=12, label="12 h", step="hour", stepmode="todate"),
                    dict(count=2, label="2 days", step="day", stepmode="todate"),
                    dict(step="all") 
                ]),
                x=0.1,
                y=-0.2, # Positionierung der Buttons unterhalb der Grafik
                xanchor='left',
                yanchor='bottom',
                bgcolor='rgba(0,0,0,0)'
            ),
            showticklabels=False, # Die ursprünglichen Buttons über der Grafik ausblenden
        )
    )
    
    # Neu: Graph etwas nach links verschieben
    fig.update_layout(margin=dict(l=50))
    
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
    fig.update_layout(title_text="Vapor Pressure Deficit in kPa", title_font_size=16, title_x=0.5)
    fig.update_yaxes(title=None)
    fig.update_xaxes(tickangle=0)
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
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                thickness=0.05,  # Hier wird die Dicke des Rangesliders in vertikaler Richtung festgelegt
            )
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="center", x=0.5) # Legende zentral ausrichten
    )
    fig.update_layout(
        xaxis_title="Time",
        legend_title="Sensor"
    )
    fig['layout']['uirevision'] = 'some-constant'
    
    # Neu: Breite des Div-Elements anpassen
    fig.update_layout(width=500)
    
    # Neu: Buttons unterhalb der Grafik
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=10, label="10 mim", step="minute", stepmode="backward"),
                    dict(count=2, label="2 h", step="hour", stepmode="backward"),
                    dict(count=12, label="12 h", step="hour", stepmode="todate"),
                    dict(count=2, label="2 days", step="day", stepmode="backward"),
                    dict(step="all") 
                ]),
                x=0.1,
                y=-0.2, # Positionierung der Buttons unterhalb der Grafik
                xanchor='left',
                yanchor='bottom',
                bgcolor='rgba(0,0,0,0)'
            ),
            showticklabels=False, # Die ursprünglichen Buttons über der Grafik ausblenden
        )
    )
    
    # Neu: Graph etwas nach links verschieben
    fig.update_layout(margin=dict(l=50))
    
    return fig



# Callback to update the current sensor values
@app.callback(
    Output("current-temp-values", "children"),
    Output("current-humid-values", "children"),
    Output("current-vpd-values", "children"),
    Output("current-temp-values2", "children"),
    Output("current-humid-values2", "children"),
    Output("current-vpd-values2", "children"),
    Input('interval-component-t', 'n_intervals'))
def update_current_sensor_values(ticker):
    df = loaddata()
    current_temp1 = df[df['type'] == 'Temp1']['value'].iloc[-1]
    current_temp2 = df[df['type'] == 'Temp2']['value'].iloc[-1]
    current_humid1 = df[df['type'] == 'Humid1']['value'].iloc[-1]
    current_humid2 = df[df['type'] == 'Humid2']['value'].iloc[-1]
    current_vpd1 = df[df['type'] == 'vpd1']['value'].iloc[-1]
    current_vpd2 = df[df['type'] == 'vpd2']['value'].iloc[-1]
    
    return f'Temp1: {current_temp1}°C', f'Humid1: {current_humid1}%', f'VPD1: {current_vpd1} kPa', f'Temp2: {current_temp2}°C', f'Humid2: {current_humid2}%', f'VPD2: {current_vpd2} kPa'

# Run the Dash app
app.config.suppress_callback_exceptions = True
app.run_server(debug=True)
