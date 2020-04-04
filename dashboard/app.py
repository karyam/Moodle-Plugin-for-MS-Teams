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
import pandas as pd
from data_wrapper import DataWrapper
from util import *
from user_tab_components import *
from team_tab_components import *
import plotly.express as px
import base64

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

assets = '/Applications/MAMP/htdocs/moodle/mod/teams/dashboard/assets'
LOGO = '/Applications/MAMP/htdocs/moodle/mod/teams/dashboard/assets/logo.png'
encoded_logo = base64.b64encode(open(LOGO, 'rb').read())


APP_PATH = str(pathlib.Path(__file__).parent.resolve())

dw = DataWrapper()


def build_section_banner(title):
    return html.Div(className="section-banner", children=title)

# def build_banner():
#     return html.Div(
#         id="banner",
#         #style={'backgroundColor': '#4D17B3'},
#         className="banner",
#         children=[
#             html.Div(
#                 id="banner-text",
#                 children=[
#                     html.H5("Microsoft Teams Analytics"),
#                     #html.H6("Get inshights into team usage and user reporting"),
#                 ],
#             )
#         ],
#     )

NAVBAR = dbc.Navbar(
    children=[
        html.A(
            dbc.Row(
                [
                    #dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_logo), height="30px")),
                    dbc.Col(
                        dbc.NavbarBrand("Teams Activity Analytics", className="ml-2")
                    ),
                ],
                align="center",
                no_gutters=True,
            ),
            #href="https://plot.ly",
        )
    ],
    color="dark",
    dark=True,
    sticky="top",
)


def build_tabs():
    return html.Div(
        id="tabs",
        # style={'backgroundColor': colors['background']},
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab2",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Team-tab",
                        #style={'backgroundColor': colors['background']},
                        label="Team",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="User-tab",
                        #style={'backgroundColor': colors['background']},
                        label="User",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )

##########################
# TAB 3 LAYOUT COMPONENTS#
##########################


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions'] = True
app.layout = html.Div(
    id="big-app-container",
    #style={'backgroundColor': colors['background']},
    children=[
        NAVBAR,
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                html.Div(id="app-content"),
            ],
        ),
    ],
)



########################
## CALLBACK FUNCTIONS ##
########################

#TODO: chek out the state tutorial
@app.callback(
    Output("app-content", "children"),
    [Input("app-tabs", "value")]
)
def render_app_content(tab_selection):
    if tab_selection == "tab1":
        return TEAM_TAB_BODY
    else: 
        return USER_TAB_BODY
   


#####################
## TAB 2 CALLBACKs ##
#####################

@app.callback(
    [Output("team-plot", "figure"), Output("no-data-alert-team", "style")],
    [Input("team-time-window-slider", "value"), Input("team-search", "value")],
)
def update_team_activity_plot(time_values, team):
    
    print("redrawing team-sample...")
    print("\ttime_values is:", time_values)
    print("\tuser selection is:", team)
    
    df = dw.get_total_msg_count()
    fig = px.line(df, x='Date', y='Message Count')
    return [fig, {"display": "none"}]


@app.callback(
    [Output("team-wordcloud", "figure"), 
     Output("team-treemap", "figure"), 
     Output("no-data-alert-worcloud2", "style")],
    [Input("team-time-window-slider", "value"), 
     Input("team-search", "value")],
)
def update_team_wordcloud_plot(timeframe, username):
    msgs = dw.get_total_message_content()
    wordcloud, treemap = plotly_wordcloud(msgs)
    alert_style = {"display": "none"}
    if (wordcloud == {}) or (treemap == {}):
        alert_style = {"display": "block"}
    return (wordcloud, treemap, alert_style)


@app.callback(
    [Output("most-active", "figure"), 
     Output("least-active", "figure"), 
     Output("no-data-alert-extreme", "style")],
    [Input("team-time-window-slider", "value"), 
     Input("team-search", "value")],
)
def update_extreme_activity_plot(team, timeframe):

    df_most_active = dw.get_most_active_df(team, timeframe)
    most_active = px.bar(df_most_active, x='Name', y='Message Count')
    
    df_least_active = dw.get_least_active_df()
    least_active = px.bar(df_least_active, x='Name', y='Message Count')
    
    alert_style = {"display": "none"}
    if (most_active == {}) or (least_active == {}):
        alert_style = {"display": "block"}

    return (most_active, least_active, alert_style)


#################
#TAB 3 CALLBACKS#
#################

@app.callback(
    [Output("user-plot", "figure"), Output("no-data-alert-user", "style")],
    [Input("user-time-window-slider", "value"), Input("user-search", "value")],
)
def update_user_activity_plot(timeframe, user):
    
    print("redrawing user-sample...")
    print("\ttime_values is:", timeframe)
    print("\tuser selection is:", user)

    df = dw.get_user_sent_msg_count()
    fig = px.line(df, x='Date', y='Message Count')
    return [fig, {"display": "none"}]


@app.callback(
    [Output("user-wordcloud", "figure"), 
     Output("user-treemap", "figure"), 
     Output("no-data-alert-worcloud3", "style")],
    [Input("user-time-window-slider", "value"), 
     Input("user-search", "value")],
)
def update_user_wordcloud_plot(timeframe, username):
    msgs = dw.get_user_message_content()
    wordcloud, treemap = plotly_wordcloud(msgs)
    alert_style = {"display": "none"}
    if (wordcloud == {}) or (treemap == {}):
        alert_style = {"display": "block"}
    return (wordcloud, treemap, alert_style)


def update_connectivity_graph(timeframe, username):
    pass



if __name__ == '__main__':
    app.run_server(debug=True)