import numpy as np
import pandas as pd
import plotly.graph_objects as go
from colors import Colors


def ms_to_mmssmmm(ms: int) -> str:
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    milliseconds = ms % 1000
    return f"{minutes:02}:{seconds:02}:{milliseconds:03}"


def plot_race_progression(df: pd.DataFrame, colors: Colors) -> go.Figure:
    """Create a Plotly line plot to show the race progression for multiple drivers.

    Args:
        df (pd.DataFrame): DataFrame with the lap-position for all the drivers for a given GP.
                The DataFrame must contain columns 'round', 'driver', and 'position'.

    Returns:
        go.Figure: _description_
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
                line=dict(color=colors.get_driver_color(driver)),
            )
        )

    # Invert the y-axis to show 1st position at the top
    fig.update_yaxes(autorange="reversed")

    # Update the layout for the chart
    fig.update_layout(
        title="Race Progression",
        xaxis_title="Lap",
        yaxis_title="Race Position",
        legend_title="Driver",
        hovermode="x unified",
        plot_bgcolor="rgba(240,240,240,0.8)",  # Light background similar to the image
        font=dict(size=12),
    )

    # Show the plot
    return fig


def plot_race_pace_progression(
    df: pd.DataFrame, drivers: list = [], colors: Colors = None
) -> go.Figure:
    """_summary_

    Args:
        df (pd.DataFrame): _description_
        drivers (list): _description_
        colors (Colors): _description_

    Returns:
        go.Figure: _description_
    """
    assert "code" in df.columns, "The DataFrame must contain a 'code' column"
    assert "lap" in df.columns, "The DataFrame must contain a 'lap' column"
    assert (
        "milliseconds" in df.columns
    ), "The DataFrame must contain a 'milliseconds' column"

    drivers = drivers or df["code"].unique()

    # Create the figure object
    fig = go.Figure()

    # Plot each driver as a separate line
    for driver in drivers:
        driver_data = df[df["code"] == driver]

        driver_data["milliseconds_ma"] = driver_data["milliseconds"].rolling(3).mean()

        driver_data["cleaned_times"] = driver_data["milliseconds"].where(
            driver_data["milliseconds"] <= driver_data["milliseconds_ma"] * 1.1,
            other=None,
        )

        # driver_data["formatted_times"] = driver_data["cleaned_times"].apply(
        #     lambda x: ms_to_mmssmmm(x) if not pd.isna(x) else np.nan
        # )

        # lap_progression = clean_lap_progression(driver_data["milliseconds"].values)

        fig.add_trace(
            go.Scatter(
                x=driver_data["lap"],
                y=driver_data["cleaned_times"],
                mode="lines+markers",
                name=driver,
                line_shape="linear",
                line=dict(color=colors.get_driver_color(driver)),
            )
        )

    # Update the layout for the chart
    fig.update_layout(
        title="Race Pace Comparison",
        xaxis_title="Lap",
        yaxis_title="Lap Time (mm:ss:mmm)",
        yaxis_tickformat="%M:%S.%3f",
        legend_title="Driver",
        hovermode="x unified",
        plot_bgcolor="rgba(240,240,240,0.8)",  # Light background similar to the image
        font=dict(size=12),
    )

    return fig


if __name__ == "__main__":
    from fetcher import fetch_gp_laps

    laps = fetch_gp_laps(year=2024, round=10)

    fig = plot_race_pace_progression(laps)
