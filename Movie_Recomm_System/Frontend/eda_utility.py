import pandas as pd
import plotly.graph_objects as go
import warnings
import numpy as np
warnings.filterwarnings("ignore")


def grouped_bar_ch(
    values_A,
    values_B,
    groups,
    tle="",
    v1="hit",
    v2="flop",
    title_x="",
    title_y="Amount in USD ($)",
):
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=groups, y=values_A, name=v1, marker_color="blue", textposition="outside"
        )
    )

    fig.add_trace(
        go.Bar(
            x=groups, y=values_B, name=v2, marker_color="orange", textposition="outside"
        )
    )

    # Group bars side-by-side
    fig.update_layout(
        barmode="group",
        title=tle,
        xaxis_title=title_x,
        yaxis_title=title_y,
        xaxis=dict(categoryorder="array", categoryarray=groups),
    )

    return fig


df1 = pd.read_csv("./Movie_Recomm_System/Frontend/deps/Frontend.csv")


def draw_graph(name, lst):
    revenues_hit = []
    revenues_flop = []
    count_hit = []
    count_flop = []
    budget_hit = []
    budget_flop = []
    total_rev = []
    total_bug = []
    for comp in lst:
        total_rev.append(df1[df1[comp] == 1]["revenue"].sum())
        total_bug.append(df1[df1[comp] == 1]["budget"].sum())
        revenues_hit.append(
            df1[(df1[comp] == 1) & (df1["hit/flop"] == "hit")]["revenue"].sum()
        )
        revenues_flop.append(
            df1[(df1[comp] == 1) & (df1["hit/flop"] == "flop")]["revenue"].sum()
        )
        budget_hit.append(
            df1[(df1[comp] == 1) & (df1["hit/flop"] == "hit")]["budget"].sum()
        )
        budget_flop.append(
            df1[(df1[comp] == 1) & (df1["hit/flop"] == "flop")]["budget"].sum()
        )
        count_hit.append(df1[(df1[comp] == 1) & (df1["hit/flop"] == "hit")].shape[0])
        count_flop.append(df1[(df1[comp] == 1) & (df1["hit/flop"] == "flop")].shape[0])
    fig1 = grouped_bar_ch(
        revenues_hit, revenues_flop, lst, "Revenue comparison", title_x=name
    )
    fig2 = grouped_bar_ch(
        count_hit,
        count_flop,
        lst,
        "Total no of movies",
        title_x=name,
        title_y="Total No of Movies",
    )
    fig3 = grouped_bar_ch(
        budget_hit, budget_flop, lst, "Budget of all movies", title_x=name
    )
    fig4 = grouped_bar_ch(
        total_rev, total_bug, lst, "Revenue and Budget", "Reveue", "Budget", name
    )
    return fig1, fig2, fig3, fig4
