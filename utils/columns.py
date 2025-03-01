from collections import defaultdict
from typing import Dict, List

from configs.columns import config as COLUMNS_CONFIG


def get_column_config(page: str, section: str) -> dict:
    """Get the columns configuration for a given page and section.

    Parameters:
    -----------
    page : str
        The page to get the columns configuration for.
    section : str
        The section to get the columns configuration for.

    Returns:
    --------
    dict
        The columns configuration for the given page and section.
    """
    section_columns = COLUMNS_CONFIG[page][section]
    return {col_config.name: col_config.get_callable_st_table_config() for col_config in section_columns}


def get_tab_config(page: str, section: str) -> list:
    """Get the tab configuration for a given page and section.

    Parameters:
    -----------
    page : str
        The page to get the tab configuration for.
    section : str
        The section to get the tab configuration for.

    Returns:
    --------
    list
    """
    section_columns = COLUMNS_CONFIG[page][section]
    return [col_config for col_config in section_columns if col_config.is_tab]


def get_precision_config(page: str, section: str) -> Dict[int, List[str]]:
    """Get the precision configuration for a given page and section.

    Parameters:
    -----------
    page : str
        The page to get the precision configuration for.
    section : str
        The section to get the precision configuration for.

    Returns:
    --------
    Dict[int, List[str]]
    """
    section_columns = COLUMNS_CONFIG[page][section]
    precision_config = defaultdict(list)

    for col_config in section_columns:
        if col_config.precision:
            precision_config[col_config.precision].append(col_config.name)

    return precision_config
