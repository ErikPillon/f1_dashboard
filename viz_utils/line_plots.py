import pandas as pd
import plotly.graph_objects as go
import fastf1 as ff1
from colors import Colors


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
