"""
Frozen Facts Center - Scores page

This script provides a Streamlit web application for viewing NHL scores, including regular 
season and playoff data. It reads data from an S3 bucket, allows users to filter scores by team, 
and presents the scores in a user-friendly format.
"""

from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path

import pandas as pd
import streamlit as st
from st_files_connection import FilesConnection

from utils.style import style_page
from utils.time import (
    convert_utc_to_user_timezone,
    get_user_timezone,
    remove_whitespace_from_st_javascript,
)

DATA_PATH_SCORES = "frozen-facts-center-prod/fact_scores.parquet"
ALL_TEAMS_OPTION = "All teams"


class TeamType(Enum):
    HOME = "home"
    AWAY = "away"


def main() -> None:
    """Main function to configure and display Scores page.

    This function sets the page style, reads data, filters data based on the selected team,
    and creates a list of games played in the last days.

    Parameters:
    -----------
    None

    Returns:
    --------
    None
    """
    style_page(file_path=Path(__file__))
    user_timezone = get_user_timezone()

    # read data
    df = read_data(user_timezone=user_timezone)

    # write info message
    st.write(
        f"""
        _In the current app version, scores are displayed for only 
        the last {df.date.nunique()} game days._
        """
    )

    # filter team
    options = [ALL_TEAMS_OPTION] + sorted(set([*df.home_team_full_name, *df.away_team_full_name]))
    filter_team = st.selectbox(label="Team", options=options, label_visibility="hidden")

    if filter_team != ALL_TEAMS_OPTION:
        df = df.loc[
            (df.home_team_full_name == filter_team) | (df.away_team_full_name == filter_team)
        ]

    display_scores(df=df)
    remove_whitespace_from_st_javascript()


@st.cache_data(ttl=timedelta(minutes=10), show_spinner=False)
def read_data(user_timezone: str) -> tuple[pd.DataFrame]:
    """Read data from an S3 bucket and preprocess it based on user timezone.

    Parameters:
    -----------
    user_timezone : str
        The user's timezone in IANA Time Zone Database format (e.g., "America/New_York").

    Returns:
    --------
    pd.DataFrame
    """
    conn = st.connection("s3", type=FilesConnection)
    df = conn.read(path=DATA_PATH_SCORES, input_format="parquet", ttl=600)

    # convert game start times from UTC into user timezone
    for col_name, date_format in (
        ("start_date_user_tz", "%Y-%m-%d"),
        ("start_time_user_tz", "%H:%M"),
    ):
        df[col_name] = df.start_time_utc.apply(
            lambda date_utc: convert_utc_to_user_timezone(
                date_utc=date_utc,
                user_timezone=user_timezone,
                date_format=date_format,
            )
        )

    # sort data frame by user timezone date and time
    df = df.sort_values(
        by=["start_date_user_tz", "start_time_user_tz"], ascending=[False, True]
    ).reset_index(drop=True)

    return df


def display_scores(df: pd.DataFrame) -> None:
    """Display scores for each date in the given DataFrame.

    This function iterates through unique dates in the DataFrame and displays scores for each date.
    For each game on a date, it shows the home team's score, and away team's score.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing the scores data.

    Returns:
    --------
    None
    """
    for date in df.start_date_user_tz.unique():
        # display subheader with date
        st.subheader(body=datetime.strptime(date, "%Y-%m-%d").strftime("%-d %b %Y"), divider="grey")

        for _, row in df.loc[df.start_date_user_tz == date].iterrows():
            did_home_team_win = row.home_team_score > row.away_team_score

            st.markdown(
                body="""
                <style>
                    div[data-testid="column"]:nth-of-type(1) {text-align: left;} 
                    div[data-testid="column"]:nth-of-type(2) {text-align: right;} 
                    div[data-testid="column"]:nth-of-type(3) {text-align: center;} 
                    div[data-testid="column"]:nth-of-type(4) {text-align: left;} 
                    div[data-testid="column"]:nth-of-type(5) {text-align: right;} 
                </style>
                """,
                unsafe_allow_html=True,
            )

            column_layout = [1, 5, 1, 5, 1]
            col1, col2, col3, col4, _ = st.columns(spec=column_layout)

            with col1:
                st.markdown(body=row.period_type)

            with col2:
                display_team_name_and_logo(
                    row=row, team_type=TeamType.HOME.value, did_home_team_win=did_home_team_win
                )

            with col3:
                st.markdown(body=f"**{row.home_team_score}-{row.away_team_score}**")

            with col4:
                display_team_name_and_logo(
                    row=row, team_type=TeamType.AWAY.value, did_home_team_win=did_home_team_win
                )

        st.markdown("####")


def display_team_name_and_logo(row: dict, team_type: str, did_home_team_win: bool) -> None:
    """Display team name and logo based on the team type.

    This function takes a row from a DataFrame, the type of team (home or away), and whether
    the home team won or not. It then displays the team's name and logo using Streamlit's markdown
    with HTML support.

    Parameters:
    -----------
    row : dict
        A dictionary representing a row of data frame.
    team_type : str
        Type of the team, should be 'home' or 'away'.
    did_home_team_win : bool
        A boolean indicating whether the home team won the game.

    Returns:
    --------
    None
    """
    name = row[f"{team_type}_team_full_name"]
    logo = row[f"{team_type}_team_logo_url"]

    if team_type == TeamType.HOME.value:
        st.markdown(
            body="{} &nbsp; &nbsp; <img src='{}' alt='drawing' width='40'/>".format(
                f"**{name}**" if did_home_team_win else name,
                logo,
            ),
            unsafe_allow_html=True,
        )

    if team_type == TeamType.AWAY.value:
        st.markdown(
            body="<img src='{}' alt='drawing' width='40'/> &nbsp; &nbsp; {}".format(
                logo,
                f"**{name}**" if not did_home_team_win else name,
            ),
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
