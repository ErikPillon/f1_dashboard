import streamlit as st

from fetcher import (
    fetch_fastest_laps_by_driver,
    fetch_number_of_laps_completed_by_driver,
    fetch_number_of_poles_by_driver,
    fetch_number_of_world_titles_by_driver,
    fetch_laps_led_by_driver,
    fetch_cumulative_points_by_driver,
    fetch_cumulative_points_by_constructor,
    fetch_seasons_years,
    fetch_number_of_wins_by_driver,
)

st.title("All Time Stats")

st.markdown(
    """This page is dedicated to the all time stats. It displays the total number of points by driver, 
    by constructor, the total number of world titles, total number of poles, total number of wins, and total number of fastest laps."""
)

season_years = fetch_seasons_years()
min_year = season_years["year"].min()
max_year = season_years["year"].max()

st.select_slider(
    "Select range", options=season_years["year"], value=(min_year, max_year)
)

st.markdown("## Total number of laps led by driver")

fastest_laps_by_driver = fetch_laps_led_by_driver()
st.dataframe(fastest_laps_by_driver)


st.markdown("## Number of laps completed by driver")

number_of_laps_completed_by_driver = fetch_number_of_laps_completed_by_driver()
st.dataframe(number_of_laps_completed_by_driver)


st.markdown("## number of poles by driver")

number_of_poles_by_driver = fetch_number_of_poles_by_driver()
st.dataframe(number_of_poles_by_driver)

st.markdown("## number of wins by driver")

number_of_wins_by_driver = fetch_number_of_wins_by_driver()
st.dataframe(number_of_wins_by_driver)


st.markdown("## number_of_world_titles_by_driver")

number_of_world_titles_by_driver = fetch_number_of_world_titles_by_driver()
st.dataframe(number_of_world_titles_by_driver)
