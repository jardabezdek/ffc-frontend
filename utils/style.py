"""Utils funtion for stremlit app styling."""

import math
from datetime import timedelta
from pathlib import Path

import pandas as pd
import streamlit as st
import toml

from utils.columns import get_column_config, get_precision_config

PAGES_CONFIG_PATH = Path(__file__).resolve().parent.parent / ".streamlit" / "pages.toml"


def style_page(file_path: Path) -> None:
    """Style a page based on the provided file path.

    Parameters:
    -----------
    file_path : Path
        The path to the file corresponding to the Streamlit page.

    Returns:
    --------
    None

    Notes:
    ------
    This function loads a configuration file containing details about different pages
    and their respective configurations. It fetches the configuration for the provided
    file path and uses it to set the page title, icon, and layout using Streamlit's
    set_page_config method. Additionally, it adds a title to the page combining the
    icon and the title fetched from the configuration.
    """
    # load page config
    page_config = next(
        item for item in toml.load(PAGES_CONFIG_PATH).get("pages") if file_path.as_posix().endswith(item.get("path"))
    )

    # configure page
    page_title = page_config.get("name")
    page_icon = page_config.get("icon")

    st.set_page_config(
        page_title=f"FFC | {page_title}",
        page_icon="🏒",
        # layout="wide",
        layout="centered",
    )

    # add page title
    st.write(f"# {page_icon} {page_title}")


def style_standings_df(df: pd.DataFrame, theme: dict) -> None:
    """Style standings data frame.

    Parameters:
    -----------
    df : pd.DataFrame
        Data frame with standings.
    theme : dict
        Dictionary containing theme metadata.

    Returns:
    --------
    None
    """
    column_config = get_column_config(page="standings", section="standings")
    precision_config = get_precision_config(page="standings", section="standings")

    df = add_rank_to_index(df=df)

    # style data
    st.dataframe(
        data=(
            df.style
            # set background color of points column
            .map(lambda _: get_highlighted_column_color(theme=theme), subset=["points"])
            # set text color of goals difference column
            .map(lambda x: "color: red;" if x < 0 else "color: green;", subset=["goals_diff"])
            # set precision
            .format(precision=1, subset=precision_config[1])
            .format(precision=2, subset=precision_config[2])
            .format(precision=3, subset=precision_config[3])
        ),
        column_order=column_config.keys(),
        column_config=column_config,
        # display dataframe in full (35 pixel is row height, 3 pixels is borders height)
        height=(len(df) + 1) * 35 + 3,
    )


def style_leaders_df(
    df: pd.DataFrame,
    col_name: str,
    section_name: str,
    theme: dict,
    batch: int = 50,
    is_skaters_section: bool = True,
) -> None:
    """Style and paginate a stat leaders data frame.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the data to be styled and paginated.
    col_name : str
        The name of the column to be highlighted with a background color.
    section_name : str
        The name of the section.
    theme : dict
        Dictionary containing theme metadata.
    batch : int, optional
        The number of rows per page for pagination (default is 50).
    is_skaters_section : bool, optional
        A flag indicating if the section is for skaters or goalies (default is True).

    Returns
    -------
    None
    """
    section = "skaters" if is_skaters_section else "goalies"
    column_config = get_column_config(page="stat_leaders", section=section)
    precision_config = get_precision_config(page="stat_leaders", section=section)

    df = add_rank_to_index(df=df)

    # paginate data
    pagination, current_page = paginate_df(
        df=df,
        batch=batch,
        col_name=col_name,
        section_name=section_name,
    )
    pages = split_df(df=df, batch=batch)

    # style data
    pagination.dataframe(
        data=(
            pages[current_page - 1]
            .style
            # set background color of stat column
            .map(lambda _: get_highlighted_column_color(theme=theme), subset=[col_name])
            # set text color of +/- column
            .map(lambda x: "color: red;" if x < 0 else "color: green;", subset=["plus_minus"])
            # set precision
            .format(precision=1, subset=precision_config[1])
            .format(precision=2, subset=precision_config[2])
            .format(precision=3, subset=precision_config[3])
        ),
        column_order=column_config.keys(),
        column_config=column_config,
        use_container_width=True,
    )


def get_highlighted_column_color(theme: dict) -> str:
    """Return the background color for a highlighted column based on the provided theme.

    Parameters
    ----------
    theme : dict
        A dictionary containing theme metadata.

    Returns
    -------
    str
    """
    if theme:
        base = theme.get("base")

        if base == "light":
            return "background-color: #f5f5f7;"

        if base == "dark":
            return "background-color: #313131;"

    return ""


def add_rank_to_index(df: pd.DataFrame) -> pd.DataFrame:
    """Add a rank column to the DataFrame index, and set rank as an index.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame to which the rank index will be added.

    Returns
    -------
    pd.DataFrame
    """
    return df.reset_index(drop=True).assign(rank=lambda x: x.index + 1).set_index(["rank"])


def paginate_df(
    df: pd.DataFrame,
    batch: int,
    col_name: str,
    section_name: str,
) -> tuple[st.container, int]:
    """Paginate a data frame for display purposes and create a pagination interface.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to paginate.
    batch : int
        The number of rows per page.
    col_name : str
        The name of the column used for pagination identification.
    section_name : str
        The name of the section used for pagination identification.

    Returns
    -------
    tuple[st.container, int]
    """
    pagination = st.container()
    bottom_menu = st.columns(5)

    with bottom_menu[4]:
        total_pages = math.ceil(len(df) / batch)
        current_page = st.number_input(
            label="Page",
            min_value=1,
            max_value=total_pages,
            step=1,
            key=f"current_page_{section_name}_{col_name}",
            label_visibility="collapsed",
        )
    with bottom_menu[0]:
        st.markdown(
            body=(f"""<p style="text-align:left;"> Page <b>{current_page}</b> of <b>{total_pages}</b></p>"""),
            unsafe_allow_html=True,
        )

    return pagination, current_page


@st.cache_data(ttl=timedelta(minutes=10), show_spinner=False)
def split_df(df: pd.DataFrame, batch: int) -> list:
    """Split a data frame into a list of smaller data frames of a specified batch size.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to split into batches.
    batch : int
        The number of rows per batch.

    Returns
    -------
    list
    """
    return [df.loc[i : i + batch - 1, :] for i in range(0, len(df), batch)]


def add_footer() -> str:
    """Add a footer to the page.

    Returns
    -------
    str
    """
    st.write(
        """
        ---
        Built with ❤️ by [Jaroslav Bezdek](https://jaroslavbezdek.com)
        """
    )
