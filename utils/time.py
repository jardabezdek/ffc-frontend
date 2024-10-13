"""Utils funtions for handling dates and times."""

from datetime import datetime

import pytz
import streamlit as st
from streamlit_javascript import st_javascript


def get_user_timezone() -> str:
    """Get the user's timezone using JavaScript in the browser.

    Returns:
    --------
    str
        The user's timezone in the "Area/Location" format (e.g., "America/New_York").
    """
    user_timezone = st_javascript("Intl.DateTimeFormat().resolvedOptions().timeZone")

    if isinstance(user_timezone, str):
        return user_timezone

    return "Europe/Prague"


def convert_utc_to_user_timezone(date_utc: str, user_timezone: str, date_format: str) -> str:
    """Convert a UTC time string to the user's timezone and return the formatted date.

    This function takes a UTC time string, the user's timezone, and a date format. It parses the
    UTC time string, converts it to the user's timezone, and returns the formatted date string.

    Parameters:
    -----------
    date_utc : str
        The input UTC time string to be converted.
    user_timezone : str
        The timezone of the user in the "Area/Location" format (e.g., "America/New_York").
    date_format : str
        The desired format for the output date string.

    Returns:
    --------
    str
        The formatted date string in the user's timezone.
    """
    return (
        datetime.strptime(date_utc, "%Y-%m-%dT%H:%M:%SZ")
        .astimezone(pytz.timezone(zone=user_timezone))
        .strftime(date_format)
    )


def get_current_user_datetime(user_timezone: str, date_format: str = "%Y-%m-%d %H:%M") -> str:
    """Get the current date and time in a specified user's timezone, formatted as a string.

    Parameters
    ----------
    user_timezone : str
        The timezone of the user, specified as a string that is compatible with the `pytz` library.
    date_format : str, optional
        The format in which to return the date and time, by default "%Y-%m-%d %H:%M".

    Returns
    -------
    str
    """
    return datetime.now().astimezone(pytz.timezone(user_timezone)).strftime(date_format)


def remove_whitespace_from_st_javascript() -> None:
    """Remove whitespace from the Streamlit component generated by st_javascript.

    This function uses a custom CSS style to hide the Streamlit component associated
    with the st_javascript function. It targets the specific iframe generated by st_javascript
    with the title "streamlit_javascript.streamlit_javascript" and sets its display property
    to 'none', effectively removing it from the layout.

    The purpose of this function is to eliminate unwanted whitespace or empty space that may be
    introduced by st_javascript, improving the overall visual appearance of the Streamlit app.

    More info here: https://github.com/thunderbug1/streamlit-javascript/issues/11

    Returns:
    --------
    None
    """
    st.markdown(
        body="""
        <style>
            .element-container:has(
                iframe[title="streamlit_javascript.streamlit_javascript"]
            ) {
                display: none
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
