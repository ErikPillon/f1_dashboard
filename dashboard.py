import logging
import streamlit as st

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

st.markdown(
    """
    # Welcome!
    
    Welcome to my website, born from a deep passion for data engineering, data analysis, and coding, all fueled by a love for Formula 1. 
    This platform is dedicated to exploring the fascinating world of statistics and data visualization, especially through the lens of F1.

    You'll find a variety of interactive dashboards and insights, each offering a unique perspective on the numbers behind the sport. 
    The website is designed to make it easy to navigate—simply use the menu on the left to explore different sections. 
    Whether you're interested in race results, driver performance, or cumulative points, there's something here for every F1 fan and data enthusiast alike.

    I hope this site serves as a place where both data lovers and motorsport fans can come together to uncover new stories hidden in the data."""
)


def main():
    pass
