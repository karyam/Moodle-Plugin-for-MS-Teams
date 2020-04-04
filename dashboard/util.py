from wordcloud import WordCloud, STOPWORDS
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
import igraph as ig
import json
import random
from data_wrapper import DataWrapper
#from textblob import *
import plotly.express as px

dw = DataWrapper()
df_sentiment = dw.get_sentiment_df()


def plotly_wordcloud(msgs:'list'=[]):

    if len(msgs) < 1:
        return {}, {}, {}

    # join all documents in corpus
    msgs= " ".join(list(msgs))

    word_cloud = WordCloud(stopwords=set(STOPWORDS), max_words=100, max_font_size=90)
    word_cloud.generate(msgs)

    word_list = []
    freq_list = []
    fontsize_list = []
    position_list = []
    orientation_list = []
    color_list = []

    for (word, freq), fontsize, position, orientation, color in word_cloud.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)

    # get the positions
    x_arr = []
    y_arr = []
    for i in position_list:
        x_arr.append(i[0])
        y_arr.append(i[1])

    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i * 80)

    trace = go.Scatter(
        x=x_arr,
        y=y_arr,
        textfont=dict(size=new_freq_list, color=color_list),
        hoverinfo="text",
        textposition="top center",
        hovertext=["{0} - {1}".format(w, f) for w, f in zip(word_list, freq_list)],
        mode="text",
        text=word_list,
    )

    layout = go.Layout(
        {
            "xaxis": {
                "showgrid": False,
                "showticklabels": False,
                "zeroline": False,
                "automargin": True,
                "range": [-100, 250],
            },
            "yaxis": {
                "showgrid": False,
                "showticklabels": False,
                "zeroline": False,
                "automargin": True,
                "range": [-100, 450],
            },
            "margin": dict(t=20, b=20, l=10, r=10, pad=4),
            "hovermode": "closest",
        }
    )

    wordcloud_figure_data = {"data": [trace], "layout": layout}
    word_list_top = word_list[:25]
    word_list_top.reverse()
    freq_list_top = freq_list[:25]
    freq_list_top.reverse()


    treemap_trace = go.Treemap(
        labels=word_list_top, parents=[""] * len(word_list_top), values=freq_list_top
    )
    treemap_layout = go.Layout({"margin": dict(t=10, b=10, l=5, r=5, pad=4)})
    treemap_figure = {"data": [treemap_trace], "layout": treemap_layout}
    return wordcloud_figure_data, treemap_figure


def build_connectivity_graph():
    # data = []
    # req = urllib.Request("https://raw.githubusercontent.com/plotly/datasets/master/miserables.json")
    # opener = urllib.build_opener()
    # f = opener.open(req)
    # data = json.loads(f.read())
    
    N=50
    L=80

    Edges=[(random.randrange(0,50), random.randrange(0,50)) for k in range(L)]

    G=ig.Graph(Edges, directed=False)
    labels=[]
    # group=[]
    
    for node in range(N):
        labels.append(node)
        #group.append(node['group'])
    
    layt=G.layout('kk', dim=3)
    
    Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
    Yn=[layt[k][1] for k in range(N)]# y-coordinates
    Zn=[layt[k][2] for k in range(N)]# z-coordinates
    
    Xe=[]
    Ye=[]
    Ze=[]
    for e in Edges:
        Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
        Ye+=[layt[e[0]][1],layt[e[1]][1], None]
        Ze+=[layt[e[0]][2],layt[e[1]][2], None]


    trace1=go.Scatter3d(x=Xe,
               y=Ye,
               z=Ze,
               mode='lines',
               line=dict(color='rgb(125,125,125)', width=1),
               hoverinfo='none'
               )

    trace2=go.Scatter3d(x=Xn,
                y=Yn,
                z=Zn,
                mode='markers',
                name='actors',
                marker=dict(symbol='circle',
                                size=6,
                                #color=group,
                                colorscale='Viridis',
                                line=dict(color='rgb(50,50,50)', width=0.5)
                                ),
                text=labels,
                hoverinfo='text'
                )

    axis=dict(showbackground=False,
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title=''
            )

    layout = go.Layout(
            #title="Network of coappearances of characters in Victor Hugo's novel<br> Les Miserables (3D visualization)",
            width=1000,
            height=1000,
            showlegend=False,
            scene=dict(
                xaxis=dict(axis),
                yaxis=dict(axis),
                zaxis=dict(axis),
            ),
        margin=dict(
            t=100
        ),
        hovermode='closest',   
    )

    data=[trace1, trace2]
    fig=go.Figure(data=data, layout=layout)
    return fig



def build_polarity_plot():
    """
    Function to build default verions of the sentiment analysis graph.
    """
    fig = px.line(df_sentiment, x='sent', y='polarity')
    return fig


def build_subjectivity_plot():
    """
    Function to build default verions of the sentiment analysis graph.
    """
    fig = px.line(df_sentiment, x='sent', y='subjectivity')
    return fig


def build_most_active_plot():
    df_most_active = dw.get_most_active_df()
    fig = px.bar(df_most_active, x='Name', y='Message Count')
    return fig

def build_least_active_plot():
    df_least_active = dw.get_least_active_df()
    fig = px.bar(df_least_active, x='Name', y='Message Count')
    return fig