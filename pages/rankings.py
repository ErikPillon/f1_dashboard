import streamlit as st
import plotly.express as px

from fetcher import (
    fetch_cumulative_points_by_constructor,
    fetch_cumulative_points_by_driver,
    fetch_seasons_years,
)

st.title("F1 Dashboard")

st.markdown(
    "This dashboard displays the cumulative points for each team and driver in the 2024 F1 season."
)

championship_years = fetch_seasons_years()

year_selected = st.selectbox(
    "Select championship year",
    championship_years["year"],
    index=int(championship_years.idxmax()[0]),
)

df_teams = fetch_cumulative_points_by_constructor(year=year_selected)
df_drivers = fetch_cumulative_points_by_driver(year=year_selected)

st.markdown(f"""
            **Championship year: {year_selected}**
            
            The **{year_selected}** F1 season is the {year_selected - 1950 +1}th year of the Formula 1 Championship.
            Saw the participation of {df_teams["name"].unique().shape[0]} teams and {df_drivers["code"].unique().shape[0]} drivers in the season.
            """)

if not year_selected == int(championship_years.max()):
    st.markdown("""
            _This championship is already over._
            """)

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
