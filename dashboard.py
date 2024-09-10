import logging
import pandas as pd
from fetcher import (
    fetch_cumulative_points_by_driver,
    fetch_cumulative_points_by_constructor,
)
import plotly.express as px
import streamlit as st

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

st.title("F1 Dashboard")

st.markdown(
    "This dashboard displays the cumulative points for each team and driver in the 2024 F1 season."
)

df_teams = fetch_cumulative_points_by_constructor()
# st.dataframe(df_teams)

teams_selected = st.multiselect("Select team", df_teams["name"].unique())


fig = px.line(
    df_teams[df_teams["name"].isin(teams_selected)],
    x="round",
    y="cumulative_points",
    color="name",
    title="Cumulative Points by Team (2024 Season)",
    labels={"round": "Round", "cumulative_points": "Cumulative Points", "name": "Team"},
    markers=True,  # Adds markers for each data point
)

# Customize the layout (optional)
fig.update_layout(
    xaxis_title="Round",
    yaxis_title="Cumulative Points",
    legend_title_text="Team",
    hovermode="x unified",
)

st.plotly_chart(fig)
# fig = plot_cumulative_points(df)
# st.plotly_chart(fig)

st.markdown("""
    ## Drivers Ranking

    Select a driver (resp. multiple drivers) below to see its (resp. their) points progression in the 2024 F1 season.""")

df_drivers = fetch_cumulative_points_by_driver()

driver_selected = st.multiselect("Select driver", df_drivers["code"].unique())

fig = px.line(
    df_drivers[df_drivers["code"].isin(driver_selected)],
    x="round",
    y="cumulative_points",
    color="code",
    title="Cumulative Points by Driver (2024 Season)",
    labels={
        "round": "Round",
        "cumulative_points": "Cumulative Points",
        "code": "Driver",
    },
    markers=True,
)

# Customize the layout (optional)
fig.update_layout(
    xaxis_title="Round",
    yaxis_title="Cumulative Points",
    legend_title_text="Driver",
    hovermode="x unified",
)

st.plotly_chart(fig)


def main():
    pass
