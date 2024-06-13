"""Configs for stremlit app styling."""

import streamlit as st

config = {
    "standings": {
        "columns": {
            "rank": st.column_config.NumberColumn(
                label="Rank",
                help="Rank",
            ),
            "team_logo_url": st.column_config.ImageColumn(
                label="Team",
                width="small",
            ),
            "team_full_name": st.column_config.TextColumn(
                label=" ",
                width="medium",
            ),
            "games_played": st.column_config.NumberColumn(
                label="GP",
                help="Games played",
            ),
            "wins": st.column_config.NumberColumn(
                label="W",
                help="Wins (worth two points)",
            ),
            "losses": st.column_config.NumberColumn(
                label="L",
                help="Losses (worth zero points)",
            ),
            "ots": st.column_config.NumberColumn(
                label="OT",
                help="OT/Shootout losses (worth one point)",
            ),
            "points": st.column_config.NumberColumn(
                label="PTS",
                help="Points",
            ),
            "points_pct": st.column_config.NumberColumn(
                label="P %",
                help="Points Percentage",
            ),
            "wins_reg": st.column_config.NumberColumn(
                label="RW",
                help="Regulation Wins",
            ),
            "wins_reg_ot": st.column_config.NumberColumn(
                label="ROW",
                help="Regulation plus Overtime Wins",
            ),
            "goals_for": st.column_config.NumberColumn(
                label="GF",
                help="Goals For",
            ),
            "goals_against": st.column_config.NumberColumn(
                label="GA",
                help="Goals Against",
            ),
            "goals_diff": st.column_config.NumberColumn(
                label="DIFF",
                help="Goal Differential",
            ),
            "record_home": st.column_config.TextColumn(
                label="HOME",
                help="Home Record",
            ),
            "record_away": st.column_config.TextColumn(
                label="AWAY",
                help="Away Record",
            ),
            "record_so": st.column_config.TextColumn(
                label="S/O",
                help="Record in games decided by Shootout",
            ),
            "record_last_10": st.column_config.TextColumn(
                label="L10",
                help="Record in last ten games",
            ),
        },
    },
    "stat_leaders": {
        "skaters": {
            "columns": {
                "rank": st.column_config.NumberColumn(
                    label="Rank",
                    help="Rank",
                ),
                "headshot_url": st.column_config.ImageColumn(
                    label="Photo",
                    width="small",
                ),
                "full_name": st.column_config.TextColumn(
                    label="Name",
                    width="medium",
                ),
                "team_abbrev_name": st.column_config.TextColumn(
                    label="Team",
                    width="small",
                ),
                "games_played": st.column_config.NumberColumn(
                    label="GP",
                    help="Games Played",
                ),
                "toi_minutes": st.column_config.NumberColumn(
                    label="TOI",
                    width="small",
                    help="Time On Ice (in mins)",
                ),
                "points": st.column_config.NumberColumn(
                    label="PTS",
                    help="Points",
                ),
                "goals": st.column_config.NumberColumn(
                    label="G",
                    help="Goals",
                ),
                "assists": st.column_config.NumberColumn(
                    label="A",
                    help="Assists",
                ),
            },
        },
        "goalies": {
            "columns": {
                "rank": st.column_config.NumberColumn(
                    label="Rank",
                    help="Rank",
                ),
                "headshot_url": st.column_config.ImageColumn(
                    label="Photo",
                    width="small",
                ),
                "full_name": st.column_config.TextColumn(
                    label="Name",
                    width="medium",
                ),
                "team_abbrev_name": st.column_config.TextColumn(
                    label="Team",
                    width="small",
                ),
                "games_played": st.column_config.NumberColumn(
                    label="GP",
                    help="Games Played",
                ),
                "toi_minutes": st.column_config.NumberColumn(
                    label="TOI",
                    width="small",
                    help="Time On Ice (in mins)",
                ),
                "gaa": st.column_config.NumberColumn(
                    label="GAA",
                    help="Goals Against Average",
                ),
                "save_pct": st.column_config.NumberColumn(
                    label="Save %",
                    # help="Save %",
                ),
                "shutouts": st.column_config.NumberColumn(
                    label="Shutouts",
                ),
            },
        },
    },
}
