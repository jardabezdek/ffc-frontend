import streamlit as st

from models.columns import ColumnConfig, StTableColumnConfig

config = {
    "standings": {
        "standings": [
            ColumnConfig(
                name="rank",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="Rank",
                    help="Rank",
                ),
            ),
            ColumnConfig(
                name="team_logo_url",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.ImageColumn,
                    label="Team",
                    width="small",
                ),
            ),
            ColumnConfig(
                name="team_full_name",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.TextColumn,
                    label=" ",
                    width="medium",
                ),
            ),
            ColumnConfig(
                name="games_played",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="GP",
                    help="Games played",
                ),
            ),
            ColumnConfig(
                name="wins",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="W",
                    help="Wins (worth two points)",
                ),
            ),
            ColumnConfig(
                name="losses",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="L",
                    help="Losses (worth zero points)",
                ),
            ),
            ColumnConfig(
                name="ots",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="OT",
                    help="OT/Shootout losses (worth one point)",
                ),
            ),
            ColumnConfig(
                name="points",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="PTS",
                    help="Points",
                ),
            ),
            ColumnConfig(
                name="points_pct",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="P %",
                    help="Points Percentage",
                ),
                precision=1,
            ),
            ColumnConfig(
                name="wins_reg",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="RW",
                    help="Regulation Wins",
                ),
            ),
            ColumnConfig(
                name="wins_reg_ot",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="ROW",
                    help="Regulation plus Overtime Wins",
                ),
            ),
            ColumnConfig(
                name="goals_for",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="GF",
                    help="Goals For",
                ),
            ),
            ColumnConfig(
                name="goals_against",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="GA",
                    help="Goals Against",
                ),
            ),
            ColumnConfig(
                name="goals_diff",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="DIFF",
                    help="Goal Differential",
                ),
            ),
            ColumnConfig(
                name="record_home",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.TextColumn,
                    label="HOME",
                    help="Home Record",
                ),
            ),
            ColumnConfig(
                name="record_away",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.TextColumn,
                    label="AWAY",
                    help="Away Record",
                ),
            ),
            ColumnConfig(
                name="record_so",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.TextColumn,
                    label="S/O",
                    help="Record in games decided by Shootout",
                ),
            ),
            ColumnConfig(
                name="record_last_10",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.TextColumn,
                    label="L10",
                    help="Record in last ten games",
                ),
            ),
        ],
    },
    "stat_leaders": {
        "skaters": [
            ColumnConfig(
                name="headshot_url",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.ImageColumn,
                    label="Photo",
                    width="small",
                ),
            ),
            ColumnConfig(
                name="full_name",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.TextColumn,
                    label="Name",
                    width="medium",
                ),
            ),
            ColumnConfig(
                name="team_abbrev_name",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.TextColumn,
                    label="Team",
                    width="small",
                ),
            ),
            ColumnConfig(
                name="position_code",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.TextColumn,
                    label="Position",
                    width="small",
                ),
            ),
            ColumnConfig(
                name="games_played",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="GP",
                    help="Games Played",
                ),
            ),
            ColumnConfig(
                name="toi_minutes",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="TOI",
                    help="Time On Ice Minutes",
                ),
            ),
            ColumnConfig(
                name="points",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="PTS",
                    help="Points",
                ),
            ),
            ColumnConfig(
                name="goals",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="G",
                    help="Goals",
                ),
            ),
            ColumnConfig(
                name="assists",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="A",
                    help="Assists",
                ),
            ),
            ColumnConfig(
                name="plus_minus",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="+/-",
                    help="Plus-Minus",
                ),
            ),
            ColumnConfig(
                name="even_strength_points",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="ESP",
                    help="Even Strength Points",
                ),
            ),
            ColumnConfig(
                name="even_strength_goals",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="ESG",
                    help="Even Strength Goals",
                ),
            ),
            ColumnConfig(
                name="power_play_points",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="PPP",
                    help="Power Play Points",
                ),
            ),
            ColumnConfig(
                name="power_play_goals",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="PPG",
                    help="Power Play Goals",
                ),
            ),
            ColumnConfig(
                name="shorthanded_points",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="SHP",
                    help="Shorthanded Points",
                ),
            ),
            ColumnConfig(
                name="shorthanded_goals",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="SHG",
                    help="Shorthanded Goals",
                ),
            ),
            ColumnConfig(
                name="ot_goals",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="OTG",
                    help="Overtime Goals",
                ),
            ),
            ColumnConfig(
                name="game_winning_goals",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="GWG",
                    help="Game Winning Goals",
                ),
            ),
            ColumnConfig(
                name="shots",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="Shots",
                    help="Shots",
                ),
            ),
            ColumnConfig(
                name="shoot_pct",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="Shoot %",
                    help="Shooting Percentage",
                ),
                precision=1,
            ),
            ColumnConfig(
                name="pim",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="PIM",
                    help="Penalty Minutes",
                ),
            ),
        ],
        "goalies": [
            ColumnConfig(
                name="headshot_url",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.ImageColumn,
                    label="Photo",
                    width="small",
                ),
            ),
            ColumnConfig(
                name="full_name",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.TextColumn,
                    label="Name",
                    width="medium",
                ),
            ),
            ColumnConfig(
                name="team_abbrev_name",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.TextColumn,
                    label="Team",
                    width="small",
                ),
            ),
            ColumnConfig(
                name="games_played",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="GP",
                    help="Games Played",
                ),
            ),
            ColumnConfig(
                name="toi_minutes",
                is_tab=False,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="TOI",
                    help="Time On Ice Minutes",
                ),
            ),
            ColumnConfig(
                name="gaa",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="GAA",
                    help="Goals Against Average",
                ),
                precision=2,
                is_sorted_ascending=True,
            ),
            ColumnConfig(
                name="save_pct",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="Save %",
                    help="Save Percentage",
                ),
                precision=1,
            ),
            ColumnConfig(
                name="shutouts",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="SO",
                    help="Shutouts",
                ),
            ),
            ColumnConfig(
                name="goals_against",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="GA",
                    help="Goals Against",
                ),
                is_sorted_ascending=True,
            ),
            ColumnConfig(
                name="xg_against",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="xGA",
                    help="Expected Goals Against",
                ),
                precision=1,
                is_sorted_ascending=True,
            ),
            ColumnConfig(
                name="saved_goals_above_expected",
                is_tab=True,
                st_table_config=StTableColumnConfig(
                    fn=st.column_config.NumberColumn,
                    label="SGAE",
                    help="Saved Goals Above Expected",
                ),
                precision=1,
            ),
        ],
    },
}
