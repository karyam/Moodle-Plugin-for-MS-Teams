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



LEFT_COLUMN_USER = dbc.Jumbotron(
    [
        html.H4(children="Select student & dataset size", className="display-5"),
        html.Hr(className="my-2"),
        html.Label("Search a student", style={"marginTop": 50}, className="lead"),
        html.P(
            "(You can search a student either by full name of Azure AD Id)",
            style={"fontSize": 10, "font-weight": "lighter"},
        ),
        dcc.Input(
            id="user-search", style={"marginBottom": 50, "font-size": 12}, placeholder="Search"
        ),
        html.Hr(className="my-2"),
        html.Label("Select time frame", className="lead"),
        html.Div(dcc.RangeSlider(id="user-time-window-slider", 
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

USER_ACTIVITY_PLOT = [
    dbc.CardHeader(html.H5("Student activity across all teams")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-user-hist",
                children=[
                    dbc.Alert(
                        "Not enough data to render this plot, please adjust the filters",
                        id="no-data-alert-user",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dcc.Graph(id="user-plot"),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

WORDCLOUD_PLOTS_USER = [
    dbc.CardHeader(html.H5("Most frequently used words in student's messages")),
    dbc.Alert(
        "Not enough data to render these plots, please adjust the filters",
        id="no-data-alert-worcloud3",
        color="warning",
        style={"display": "none"},
    ),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Loading(
                            id="loading-user-frequencies",
                            children=[dcc.Graph(id="user-frequency-figure")],
                            type="default",
                        )
                    ),
                    dbc.Col(
                        [
                            dcc.Tabs(
                                id="tabs",
                                children=[
                                    dcc.Tab(
                                        label="Treemap",
                                        children=[
                                            dcc.Loading(
                                                id="loading-treemap",
                                                children=[dcc.Graph(id="user-treemap")],
                                                type="default",
                                            )
                                        ],
                                    ),
                                    dcc.Tab(
                                        label="Wordcloud",
                                        children=[
                                            dcc.Loading(
                                                id="loading-wordcloud",
                                                children=[
                                                    dcc.Graph(id="user-wordcloud")
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

SENTIMENT_PLOTS_USER = [
    dbc.CardHeader(html.H5("Sentiment analysis")),
    dbc.Alert(
        "Not enough data to render these plots, please adjust the filters",
        id="no-data-alert-sentiment",
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
                                id="tabs",
                                children=[
                                    dcc.Tab(
                                        label="Polarity",
                                        children=[
                                            dcc.Loading(
                                                id="loading-polarity",
                                                children=[dcc.Graph(id="polarity-graph", figure=build_polarity_plot())],
                                                type="default",
                                            )
                                        ],
                                    ),
                                    dcc.Tab(
                                        label="Subjectivity",
                                        children=[
                                            dcc.Loading(
                                                id="loading-subjectivity",
                                                children=[
                                                    dcc.Graph(id="subjectivity-graph", figure=build_subjectivity_plot())
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
        ],
    ),
]


USER_CONNECTIVITY_GRAPH = [
    dbc.CardHeader(html.H5("Connectivity graph")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-graph",
                children=[
                    dbc.Alert(
                        "Not enough data to render this plot, please adjust the filters",
                        id="no-data-alert-user",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dcc.Graph(id="connectivity-graph", figure=build_connectivity_graph()),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

USER_LDA_PLOT = dcc.Loading(
    id="loading-user-lda-plot", children=[dcc.Graph(id="user-tsne-lda")], type="default"
)

USER_LDA_TABLE = html.Div(
    id="user-lda-table-block",
    children=[
        dcc.Loading(
            id="user-loading-lda-table",
            children=[
                dash_table.DataTable(
                    id="user-lda-table",
                    style_cell_conditional=[
                        {
                            "if": {"column_id": "Text"},
                            "textAlign": "left",
                            "whiteSpace": "normal",
                            "height": "auto",
                            "min-width": "50%",
                        }
                    ],
                    style_data_conditional=[
                        {
                            "if": {"row_index": "odd"},
                            "backgroundColor": "rgb(243, 246, 251)",
                        }
                    ],
                    style_cell={
                        "padding": "16px",
                        "whiteSpace": "normal",
                        "height": "auto",
                        "max-width": "0",
                    },
                    style_header={"backgroundColor": "white", "fontWeight": "bold"},
                    style_data={"whiteSpace": "normal", "height": "auto"},
                    filter_action="native",
                    page_action="native",
                    page_current=0,
                    page_size=5,
                    columns=[],
                    data=[],
                )
            ],
            type="default",
        )
    ],
    style={"display": "none"},
)

USER_LDA_PLOTS = [
    dbc.CardHeader(html.H5("Topic modelling using LDA")),
    dbc.Alert(
        "Not enough data to render LDA plots, please adjust the filters",
        id="no-data-alert-lda",
        color="warning",
        style={"display": "none"},
    ),
    dbc.CardBody(
        [
            html.P(
                "Click on a complaint point in the scatter to explore that specific complaint",
                className="mb-0",
            ),
            html.P(
                "(not affected by sample size or time frame selection)",
                style={"fontSize": 10, "font-weight": "lighter"},
            ),
            USER_LDA_PLOT,
            html.Hr(),
            USER_LDA_TABLE,
        ]
    ),
]

USER_TAB_BODY = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(LEFT_COLUMN_USER, md=4, align="center"),
                dbc.Col(dbc.Card(USER_ACTIVITY_PLOT), md=8),
            ],
            style={"marginTop": 30},
        ),
        dbc.Card(WORDCLOUD_PLOTS_USER),
        dbc.Row([dbc.Col([dbc.Card(USER_CONNECTIVITY_GRAPH)])], style={"marginTop": 50}),
        dbc.Row([dbc.Col([dbc.Card(SENTIMENT_PLOTS_USER)])], style={"marginTop": 50}),
        #dbc.Row([dbc.Col([dbc.Card(USER_LDA_PLOTS)])], style={"marginTop": 50}),
    ],
    className="mt-12",
)