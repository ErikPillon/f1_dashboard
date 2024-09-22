import streamlit as st
from colors import Colors

from fetcher import fetch_seasons_years, fetch_championship_gp, fetch_gp_laps
from viz_utils.line_plots import plot_race_progression, plot_race_pace_progression

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


@st.cache_data
def get_colors(year, round):
    return Colors(year=year, round=round)


colors = get_colors(year=year_selected, round=round_selected)

fig = plot_race_progression(laps, colors=colors)

st.plotly_chart(fig)

driver_selected = st.multiselect(
    "Select driver", laps["code"].unique(), default=laps["code"].unique()
)

fig = plot_race_pace_progression(laps, driver_selected, colors=colors)

st.plotly_chart(fig)
