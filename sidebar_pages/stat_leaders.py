"""
Frozen Facts Center - Stats page
"""

from datetime import timedelta
from pathlib import Path

import pandas as pd
import streamlit as st
from st_files_connection import FilesConnection
from streamlit_theme import st_theme

from utils.style import style_leaders_df, style_page

# define the data path
DATA_PATH_SKATER_STATS = "frozen-facts-center-prod/fact_stats.parquet"

# define the filters and corresponding column names
FILTER_NAME_TO_COL = {
    "Season": "season_long",
    "Season Type": "season_type_long",
    "Team": "team_full_name",
}

# define the tabs and corresponding stat column names
TAB_TO_COL = {
    "skaters": {
        "Points": "points",
        "Goals": "goals",
        "Assists": "assists",
        "Plus-Minus": "plus_minus",
        "Even Strength Points": "even_strength_points",
        "Even Strength Goals": "even_strength_goals",
        "Power Play Points": "power_play_points",
        "Power Play Goals": "power_play_goals",
        "Shorthanded Points": "shorthanded_points",
        "Shorthanded Goals": "shorthanded_goals",
        "Overtime Goals": "ot_goals",
        "Game Winning Goals": "game_winning_goals",
        "Shots": "shots",
        "Shoot %": "shoot_pct",
        "Penalty Minutes": "pim",
    },
    "goalies": {
        "GAA": "gaa",
        "Save %": "save_pct",
        "Shutouts": "shutouts",
    },
}

# define the standings and corresponding emoji
STANDING_TO_EMOJI = {
    1: "🥇",
    2: "🥈",
    3: "🥉",
}

# define columns that need to be sorted ascending
ASCENDING_COLS = ["gaa"]

# define (probably) the highest number of goalies per team per season
MAX_GOALIES_PER_TEAM = 3


def main() -> None:
    """Main function to configure and display Stats page.

    Parameters:
    -----------
    None

    Returns:
    --------
    None
    """
    style_page(file_path=Path(__file__))
    theme = st_theme()

    df = read_data()
    df = apply_filters(df=df)

    create_leaders_section(
        df=df.loc[df.position_code != "G"],
        header="Skaters",
        is_skaters_section=True,
        theme=theme,
    )
    create_leaders_section(
        df=df.loc[df.position_code == "D"],
        header="Defensmen",
        is_skaters_section=True,
        theme=theme,
    )
    create_leaders_section(
        df=df.loc[df.position_code == "G"],
        header="Goaltenders",
        is_skaters_section=False,
        theme=theme,
    )


@st.cache_data(ttl=timedelta(minutes=10), show_spinner=False)
def read_data() -> pd.DataFrame:
    """Read stats from S3 storage.

    Parameters:
    -----------
    None

    Returns:
    --------
    pd.DataFrame
    """
    conn = st.connection("s3", type=FilesConnection)
    return conn.read(path=DATA_PATH_SKATER_STATS, input_format="parquet", ttl=600)


def apply_filters(df: pd.DataFrame, all_teams_option: str = "All teams") -> pd.DataFrame:
    """Apply interactive filters to a DataFrame using Streamlit widgets.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to be filtered.
    all_teams_option : str, optional
        The label for the option to select all teams in the "Team" filter (default is "All teams").

    Returns
    -------
    pd.DataFrame
    """
    # create columns for filters
    filter_columns = st.columns(3)

    for (filter_name, column_name), filter_col in zip(FILTER_NAME_TO_COL.items(), filter_columns):
        with filter_col:
            if filter_name == "Team":
                options = [all_teams_option] + sorted(df[column_name].unique())
            else:
                options = df[column_name].unique()

            filter_value = st.selectbox(
                label=filter_name,
                options=options,
                label_visibility="hidden",
            )

            if filter_value != all_teams_option:
                df = df[df[column_name] == filter_value]

    return df


def create_leaders_section(
    df: pd.DataFrame,
    header: str,
    is_skaters_section: bool,
    theme: dict,
) -> None:
    """Create and display a section for statistical leaders.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the players' statistics.
    header : str
        The header title for the section.
    is_skaters_section : bool
        A flag indicating if the section is for skaters (True) or goalies (False).
    theme : dict
        A dictionary containing theme information for styling.

    Returns
    -------
    None

    Notes
    -----
    The function performs the following steps:
    - Adds a header to the section.
    - If displaying goalies and the number of goalies exceeds a threshold, adds a slider for
      filtering by minimum games played.
    - Creates tabs for different statistical categories.
    - Sorts the DataFrame and displays player information within columns.
    - Styles and paginates the DataFrame for the selected tab.
    """
    # add skaters header
    st.header(header)

    # add min games slider (if comparing all teams stats)
    if not is_skaters_section and len(df) > MAX_GOALIES_PER_TEAM:
        max_games_played = df.games_played.max()

        if max_games_played > 5:
            step = 5 if max_games_played > 15 else 2
            max_value = max_games_played - (max_games_played % step)

            min_games_played = st.slider(
                label="Minimum of played games",
                min_value=0,
                max_value=max_value,
                value=max_value,
                step=step,
                label_visibility="visible",
            )
            df = df.loc[df.games_played >= min_games_played]

    # create tabs
    tab_to_col = TAB_TO_COL["skaters"] if is_skaters_section else TAB_TO_COL["goalies"]
    tabs = st.tabs(tabs=tab_to_col.keys())

    # iterate over tabs and create content
    for (tab_name, col_name), tab in zip(tab_to_col.items(), tabs):

        with tab:
            df_sorted = df.sort_values(
                by=[col_name, "games_played", "toi_minutes"],
                ascending=[col_name in ASCENDING_COLS, True, True],
            )

            col1, col2, col3 = st.columns(3)
            align_columns_to_center()

            for idx, col in enumerate([col1, col2, col3]):
                if idx + 1 <= len(df_sorted):
                    with col:
                        display_player_info(
                            row=df_sorted.iloc[idx],
                            col_name=col_name,
                            tab_name=tab_name,
                            standing=idx + 1,
                        )

            if not df_sorted.empty:
                style_leaders_df(
                    df_sorted,
                    col_name=col_name,
                    section_name=header.lower(),
                    theme=theme,
                    is_skaters_section=is_skaters_section,
                )


def align_columns_to_center() -> st.markdown:
    """Align the content of Streamlit columns to the center.

    Returns
    -------
    st.markdown
    """
    st.markdown(
        body="""
            <style>
                div[data-testid="column"]:nth-of-type(1) {text-align: center;}
                div[data-testid="column"]:nth-of-type(2) {text-align: center;}
                div[data-testid="column"]:nth-of-type(3) {text-align: center;}
            </style>
            """,
        unsafe_allow_html=True,
    )


def display_player_info(row: dict, col_name: str, tab_name: str, standing: int) -> None:
    """Displays player information.

    Parameters
    ----------
    row : dict
        A dictionary containing the player's information.
    col_name : str
        The name of the column used to display the player's statistic.
    tab_name : str
        The name of the current tab displaying the player's information.
    standing : int
        The player's standing or rank, used to retrieve an emoji.

    Returns
    -------
    None

    Notes
    -----
    The function displays the following player information:
    - Headshot image centered in the column.
    - Player's full name with an emoji representing their standing.
    - Player's team abbreviation, sweater number, and position code.
    - The value of the player's statistic from the specified column.
    - The name of the player's statistic.
    """
    st.markdown(
        body=f"<img src='{row.headshot_url}' width='125' style='display: block; margin: 0 auto;'>",
        unsafe_allow_html=True,
    )
    st.write("####")
    st.write(f"##### {STANDING_TO_EMOJI.get(standing)} {row.full_name}")
    st.markdown(
        body=f"{row.team_abbrev_name} &#8226; #{row.sweater_number} &#8226; {row.position_code}",
        unsafe_allow_html=True,
    )
    st.write(f"# {row[col_name]}")
    st.write(tab_name)


if __name__ == "__main__":
    main()
