# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 14:16:45 2020

@author: Milosh
"""

import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('Manual_Log_Filtered_Final.csv')

servers = df['Server'].unique()
metrics = df['variable'].unique()
errors = df['Error_count'].unique()
print(errors)


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.Div([
        dcc.Dropdown(
        id='servers-radio',
        options=[{'label': k, 'value': k} for k in servers],
        value='A'
        )],style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
        dcc.Dropdown(id='metrics-radio')] ,style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ]),

    html.Hr(),

    html.Div(id='display-selected-values'),
    dcc.Graph(id='indicator-graphic')
])


@app.callback(
    Output('metrics-radio', 'options'),
    [Input('servers-radio', 'value')])
def set_metrics_options(selected_country):
    return [{'label': i, 'value': i} for i in metrics]


@app.callback(
    Output('metrics-radio', 'value'),
    [Input('metrics-radio', 'options')])
def set_metrics_value(available_options):
    print(available_options[0]['value'])
    return available_options[0]['value']

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('servers-radio', 'value'),
     Input('metrics-radio', 'value')])

def update_graph(servers,metrics):
    
    print(servers)
    print(metrics)
    
    dff = df[(df["Server"] == servers) & (df["variable"] == metrics)]
    trace1 = go.Scatter(
        x=dff["Time_floor"],
        y=dff["Value"],
        name='Metrics value'
    )   
    trace2 = go.Scatter(
        x=dff["Time_floor"],
        y=dff["Error_count"],
        name='Error count',
        yaxis='y2'
    )
    print(dff)

    return {
        'data': [
                trace1, trace2]
        ,
        'layout': go.Layout(
                title='Metrics',
                xaxis=dict(
                    title='Time'
                ),
                yaxis=dict(
                    title='Value'
                ),
                yaxis2=dict(
                    title='Error_count',
                    overlaying='y',
                    side='right'
                )
        )
    }



if __name__ == '__main__':
    app.run_server()