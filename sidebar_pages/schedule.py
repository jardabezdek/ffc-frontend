"""
Frozen Facts Center - Schedule page

This script provides a Streamlit web application for viewing NHL game schedule for the following 
days, including regular season and playoff data. It reads data from an S3 bucket, allows users 
to filter schedule by team, and presents the schedule in a user-friendly format.
"""

from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path

import pandas as pd
import pytz
import streamlit as st
from st_files_connection import FilesConnection
from streamlit_javascript import st_javascript

from utils.style import style_page
from utils.time import (
    convert_utc_to_user_timezone,
    get_user_timezone,
    remove_whitespace_from_st_javascript,
)

DATA_PATH_SCHEDULE = "frozen-facts-center-prod/fact_schedule.parquet"
ALL_TEAMS_OPTION = "All teams"


class TeamType(Enum):
    HOME = "home"
    AWAY = "away"


def main() -> None:
    """Main function to configure and display Schedule page.

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

    # get the list of the next days
    schedule_days = pd.date_range(
        start=datetime.now(tz=pytz.timezone(zone=user_timezone)).date(),
        end=df["start_date_user_tz"].max(),
        freq="D",
    )

    # write info message
    st.write(
        f"""
        _In the current app version, scheduled games are displayed for only 
        the next {len(schedule_days)} days._
        """
    )

    # filter team
    options = [ALL_TEAMS_OPTION] + sorted(set([*df.home_team_full_name, *df.away_team_full_name]))
    filter_team = st.selectbox(label="Team", options=options, label_visibility="hidden")
    if filter_team != ALL_TEAMS_OPTION:
        df = df.loc[
            (df.home_team_full_name == filter_team) | (df.away_team_full_name == filter_team)
        ]

    display_schedule(df=df, schedule_days=schedule_days, filter_team=filter_team)
    remove_whitespace_from_st_javascript()


@st.cache_data(ttl=timedelta(minutes=10), show_spinner=False)
def read_data(user_timezone: str) -> tuple[pd.DataFrame]:
    """Read schedule data from an S3 bucket and preprocess it based on user timezone.

    Parameters:
    -----------
    user_timezone : str
        The user's timezone in IANA Time Zone Database format (e.g., "America/New_York").

    Returns:
    --------
    pd.DataFrame
        The preprocessed DataFrame containing schedule data.
    """
    conn = st.connection("s3", type=FilesConnection)
    df = conn.read(path=DATA_PATH_SCHEDULE, input_format="parquet", ttl=600)

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


def display_schedule(df: pd.DataFrame, schedule_days: pd.DatetimeIndex, filter_team: str) -> None:
    """Display the schedule of games based on the provided DataFrame and filter criteria.

    Parameters:
    -----------
    df : pd.DataFrame
        The DataFrame containing schedule data.
    schedule_days : pd.DatetimeIndex
        The datetime index representing the days for which the schedule is to be displayed.
    filter_team : str
        The optional filter for a specific team. If set to 'All Teams', no team-specific filter
        is applied.

    Returns:
    --------
    None
    """
    for date in schedule_days:
        st.subheader(body=date.strftime("%-d %b %Y"), divider="grey")

        # filter day from data frame
        df_day = df.loc[df.start_date_user_tz == date.strftime("%Y-%m-%d")]

        # print info message, if there is no data to be displayed
        if df_day.empty:
            if filter_team == ALL_TEAMS_OPTION:
                st.markdown("_No games are scheduled for the day._")
            else:
                st.markdown(f"_No {filter_team} game is scheduled for the day._")

            st.markdown("####")
            continue

        # display scheduled games
        for _, row in df_day.iterrows():
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
                st.markdown(body=row.start_time_user_tz)

            with col2:
                display_team_name_and_logo(row=row, team_type=TeamType.HOME.value)

            with col3:
                st.markdown(body="vs.")

            with col4:
                display_team_name_and_logo(row=row, team_type=TeamType.AWAY.value)

        st.markdown("####")


def display_team_name_and_logo(row: dict, team_type: str) -> None:
    """Display team name and logo based on the team type.

    Parameters:
    -----------
    row : dict
        A dictionary representing a row of data frame.
    team_type : str
        Type of the team, should be 'home' or 'away'.

    Returns:
    --------
    None
    """
    name = row[f"{team_type}_team_full_name"]
    logo = row[f"{team_type}_team_logo_url"]

    if team_type == TeamType.HOME.value:
        st.markdown(
            body=f"{name} &nbsp; &nbsp; <img src='{logo}' alt='drawing' width='40'/>",
            unsafe_allow_html=True,
        )

    if team_type == TeamType.AWAY.value:
        st.markdown(
            body=f"<img src='{logo}' alt='drawing' width='40'/> &nbsp; &nbsp; {name}",
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
