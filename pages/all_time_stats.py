import streamlit as st
import pandas as pd
import plotly.express as px

from fetcher import (
    fetch_cumulative_points_by_constructor,
    fetch_cumulative_points_by_driver,
)

st.title("All Time Stats")

st.markdown(
    """This page is dedicated to the all time stats. It displays the total number of points by driver, 
    by constructor, the total number of world titles, total number of poles, total number of wins, and total number of fastest laps."""
)
