import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from fetcher import fetch_seasons_years, fetch_championship_gp, fetch_gp_laps

st.title("Race Analysis")

st.markdown(
    "The following dashboard allows an analysis and comparison of the different drivers racepace, divided by GP and by driver."
)

championship_years = fetch_seasons_years()

year_selected = st.selectbox(
    "Select championship year",
    championship_years["year"],
    index=int(championship_years.idxmax()[0]),
)

championship_rounds = fetch_championship_gp(year=year_selected)

round_selected = st.selectbox(
    "Select championship gp",
    championship_rounds["round"],
    index=int(championship_years.idxmax()[0]),
)

laps = fetch_gp_laps(year=year_selected, round=round_selected)

championship_gp = championship_rounds[championship_rounds["round"] == round_selected]

st.markdown(f"""
            #### Brief Info
            
            The {championship_gp.iloc[0]["name"]} was round {championship_gp.iloc[0]["round"]} of the {year_selected} F1 Championship and was held at {championship_gp.iloc[0]["circuit"]} in {championship_gp.iloc[0]["location"]} ({championship_gp.iloc[0]["country"]}) on {championship_gp.iloc[0]["date"]}.
            
            The GP saw the participation of {laps["code"].unique().shape[0]} drivers and a total of {laps.shape[0]} laps were completed.
            """)

st.markdown("""
    ## GP Race Pace Analysis

    Select a driver (resp. multiple drivers) below to see its (resp. their) race pace progression over the GP.""")


driver_selected = st.multiselect("Select driver", laps["code"].unique())


def plot_race_progression(df: pd.DataFrame) -> go.Figure:
    """
    Create a Plotly line plot to show the race progression for multiple drivers.

    Parameters:
    df (pd.DataFrame): A DataFrame containing columns 'round', 'driver', and 'position'.

    Returns:
    fig: A Plotly figure object.
    """

    assert "code" in df.columns, "The DataFrame must contain a 'code' column"
    assert "lap" in df.columns, "The DataFrame must contain a 'lap' column"
    assert "position" in df.columns, "The DataFrame must contain a 'position' column"

    # Create the figure object
    fig = go.Figure()

    drivers = df["code"].unique()

    # Plot each driver as a separate line
    for driver in drivers:
        driver_data = df[df["code"] == driver]
        fig.add_trace(
            go.Scatter(
                x=driver_data["lap"],
                y=driver_data["position"],
                mode="lines+markers",
                name=driver,
                line_shape="linear",
            )
        )

    # Invert the y-axis to show 1st position at the top
    fig.update_yaxes(autorange="reversed")

    # Update the layout for the chart
    # fig.update_layout(
    #     title="Championship Standings Progression",
    #     xaxis_title="Round",
    #     yaxis_title="Championship Position",
    #     legend_title="Driver",
    #     hovermode="x unified",
    #     plot_bgcolor="rgba(240,240,240,0.8)",  # Light background similar to the image
    #     font=dict(size=12),
    # )

    # Show the plot
    return fig


fig = plot_race_progression(laps)

st.plotly_chart(fig)
