import os
import pathlib
import dash
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import dash_daq as daq
import dash_bootstrap_components as dbc
from util import *
import plotly.express as px



LEFT_COLUMN_TEAM = dbc.Jumbotron(
    [
        html.H4(children="Select team & dataset size", className="display-5"),
        html.Hr(className="my-2"),
        html.Label("Search a team", style={"marginTop": 50}, className="lead"),
        html.P(
            "(You can search a team by its corresponding id)",
            style={"fontSize": 10, "font-weight": "lighter"},
        ),
        dcc.Input(
            id="team-search", style={"marginBottom": 50, "font-size": 12}, placeholder="Search"
        ),
        html.Hr(className="my-2"),
        html.Label("Select time frame", className="lead"),
        html.Div(dcc.RangeSlider(id="team-time-window-slider", 
                                 min=0,
                                 max=5,
                                 step=None,
                                 marks={
                                    0: '2014',
                                    1: '2015',
                                    2: '2016',
                                    3: '2017',
                                    4: '2018'
                                 }),
                                 style={"marginBottom": 50}),
        html.P(
            "(You can define the time frame down to year granularity)",
            style={"fontSize": 10, "font-weight": "lighter"},
        ),
    ]
)

TEAM_ACTIVITY_PLOT = [
    dbc.CardHeader(html.H5("Activity inside selected team")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-team-hist",
                children=[
                    dbc.Alert(
                        "Not enough data to render this plot, please adjust the filters",
                        id="no-data-alert-team",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dcc.Graph(id="team-plot"),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]


WORDCLOUD_PLOTS_TEAM = [
    dbc.CardHeader(html.H5("Most frequently used words inside selected team")),
    dbc.Alert(
        "Not enough data to render these plots, please adjust the filters",
        id="no-data-alert-wordcloud2",
        color="warning",
        style={"display": "none"},
    ),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Tabs(
                                id="team-wordcloud-tabs",
                                children=[
                                    dcc.Tab(
                                        label="Treemap",
                                        children=[
                                            dcc.Loading(
                                                id="loading-treemap-team",
                                                children=[dcc.Graph(id="team-treemap")],
                                                type="default",
                                            )
                                        ],
                                    ),
                                    dcc.Tab(
                                        label="Wordcloud",
                                        children=[
                                            dcc.Loading(
                                                id="loading-wordcloud-team",
                                                children=[
                                                    dcc.Graph(id="team-wordcloud")
                                                ],
                                                type="default",
                                            )
                                        ],
                                    ),
                                ],
                            )
                        ],
                        md=8,
                    ),
                ]
            )
        ]
    ),
]


MOST_ACTIVE_PLOT = [
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-most-active-hist",
                children=[
                    dbc.Alert(
                        "Not enough data to render this plot, please adjust the filters",
                        id="no-data-alert-bank",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dcc.Graph(id="most-active", figure=build_most_active_plot()),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]


LEAST_ACTIVE_PLOT = [
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-least-active-hist",
                children=[
                    dbc.Alert(
                        "Not enough data to render this plot, please adjust the filters",
                        id="no-data-alert-bank",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dcc.Graph(id="least-active", figure=build_least_active_plot()),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]


EXTREME_ACTIVITY_PLOT = [
    #dbc.CardHeader(html.H5("Most frequently used words inside selected team")),
    dbc.Alert(
        "Not enough data to render these plots, please adjust the filters",
        id="no-data-alert-extreme",
        color="warning",
        style={"display": "none"},
    ),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Tabs(
                                id="team-extreme-tabs",
                                children=[
                                    dcc.Tab(
                                        label="Most active users",
                                        children=[
                                            dcc.Loading(
                                                id="loading-most-active",
                                                children=[dbc.Row(MOST_ACTIVE_PLOT)],
                                                type="default",
                                            )
                                        ],
                                    ),
                                    dcc.Tab(
                                        label="Least active users",
                                        children=[
                                            dcc.Loading(
                                                id="loading-least-active",
                                                children=[dbc.Row(LEAST_ACTIVE_PLOT)],
                                                type="default",
                                            )
                                        ],
                                    ),
                                ],
                            )
                        ],
                        md=8,
                    ),
                ]
            )
        ]

    ),
]


SENTIMENT_PLOTS_TEAM = [
    dbc.CardHeader(html.H5("Sentiment analysis")),
    dbc.Alert(
        "Not enough data to render these plots, please adjust the filters",
        id="no-data-alert-team",
        color="warning",
        style={"display": "none"},
    ),
    #TODO: add emoji
]

TEAM_CONNECTIVITY_GRAPH = [
    dbc.CardHeader(html.H5("Team dynamics")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-graph-team",
                children=[
                    dbc.Alert(
                        "Not enough data to render this plot, please adjust the filters",
                        id="no-data-alert-team-graph",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dcc.Graph(id="team-connectivity-graph", figure=build_connectivity_graph()),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),

]



TEAM_TAB_BODY = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(LEFT_COLUMN_TEAM, md=4, align="center"),
                dbc.Col(dbc.Card(TEAM_ACTIVITY_PLOT), md=8),
            ],
            style={"marginTop": 30},
        ),
        dbc.Card(WORDCLOUD_PLOTS_TEAM, style={"marginTop": 50}),
        dbc.Card(EXTREME_ACTIVITY_PLOT, style={"marginTop": 50}),
        dbc.Row([dbc.Col([dbc.Card(TEAM_CONNECTIVITY_GRAPH)])], style={"marginTop": 50}),
        dbc.Row([dbc.Col([dbc.Card(SENTIMENT_PLOTS_TEAM)], align="center")], style={"marginTop": 50}),
    ],
    className="mt-12",
)
