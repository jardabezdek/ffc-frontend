from pathlib import Path

import streamlit as st
from st_pages import show_pages_from_config

from utils.style import add_footer, style_page

style_page(file_path=Path(__file__))
show_pages_from_config()

st.write(
    """
    Welcome to **Frozen Facts Center**, a hub for NHL stats, standings, and analytics. 

    #### 🔎 What You'll Find Here
    
    ✅ **Standings:** Stay up to date with team rankings across the league, conferences, and divisions. \\
    ✅ **Scores:** Get results from recently played games. \\
    ✅ **Schedule:** Don't miss a game—check out upcoming matchups. \\
    ✅ **Stat Leaders:** Dive deep into player stats, from goals and assists to advanced metrics like xG.

    #### 📊 Built for Data Enthusiasts by Data Enthusiast
    
    Frozen Facts Center isn't just about stats — it's also a showcase of the tech stack I love to use. 
    The infrastructure is hosted on AWS, built with AWS CDK for infrastructure as code. The data pipelines
    are powered by duckdb and dbt, and the web app itself runs on the one and only Streamlit.

    The code is open source! You can check out the repositories here:
    [backend](https://github.com/jardabezdek/ffc-backend) & [frontend](https://github.com/jardabezdek/ffc-frontend).

    #### 🚀 Start Exploring Now!
    Click through the sections on the left and uncover the numbers that define the game!
    """
)

add_footer()
