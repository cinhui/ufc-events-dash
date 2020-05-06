import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

import flask
import pandas as pd
import time
import os

# server = flask.Flask('app')
# server.secret_key = os.environ.get('secret_key', 'secret')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css','https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css']
app = dash.Dash(__name__, external_stylesheets=[external_stylesheets,dbc.themes.DARKLY])# dbc.themes.BOOTSTRAP])

server = app.server

app.title = 'UFC'
app.css.config.serve_locally = False
app.scripts.config.serve_locally = False

delta_days_df = pd.read_csv('delta_days.csv')
yearly_df = pd.read_csv('events_by_year.csv')
monthly_df = pd.read_csv('events_by_month.csv')

dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

######
#   Dash Components Start Here
######
colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

_header = dbc.Nav([
    dbc.NavItem(dbc.NavbarBrand(""))
])

_body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("UFC Events Since 2006",
                            style={
                                'color': colors['text']
                            }),
                        html.P(
                            "Data includes past events and scheduled futured events. Cancelled and postponed events are excluded.",
                            style={
                                'color': colors['text']
                            }
                        ),
                        dcc.Dropdown(
                            id='my-dropdown',
                            options=[
                                {'label': 'Number of Events by Year', 'value': 'YEARLY'},
                                {'label': 'Number of Events by Month', 'value': 'MONTHLY'},
                                {'label': 'Number of Days Between Events', 'value': 'DELTA_DAYS'}
                            ],
                            value='DELTA_DAYS'
                        ),
                        dcc.Graph(id='my-graph')
                    ], width=12
                )
            ])
    ])

_footer = dbc.Container(
    [
    html.Div([
        html.Br(),
        html.Br(),
        html.P(
            "",
        ),
        html.Br(),
    ])
    ]
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, \
    children=[_header, _body, _footer],\
        className="container")


@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    dff= delta_days_df[delta_days_df['date']>='2005-11-01']
    # print(selected_dropdown_value)
    if selected_dropdown_value == 'YEARLY':
        dff = yearly_df[yearly_df['date']>=2006]
    elif selected_dropdown_value == 'MONTHLY':
        dff = monthly_df[monthly_df['date']>='2005-11']
    else:
        dff = delta_days_df[delta_days_df['date']>='2005-11-01']
    return {
            'data': [
                go.Scatter(
                    x=dff.date,
                    y=dff.value,
                    name="",
                    opacity=0.8)                               
            ],
            'layout': {
                'title' : '',
                'xaxis':{
                    'title':'Date'
                },
                'yaxis':{
                     'title':'Count'
                },
                'margin': {
                    'l': 50,
                    'r': 50,
                    'b': 50,
                    't': 50
                }
            }
    }

if __name__ == '__main__':
    app.run_server(debug=True)
