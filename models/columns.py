from dataclasses import dataclass
from typing import Callable, Union

import streamlit as st


@dataclass
class StTableColumnConfig:
    fn: Union[
        st.column_config.NumberColumn,
        st.column_config.TextColumn,
        st.column_config.ImageColumn,
    ]
    label: str
    help: str | None = None
    width: str | None = None


@dataclass
class ColumnConfig:
    name: str
    is_tab: bool
    st_table_config: StTableColumnConfig
    precision: int | None = None
    is_sorted_ascending: bool = False

    def get_callable_st_table_config(self) -> Callable:
        st_table_config = self.st_table_config.__dict__.copy()
        col_fn = st_table_config.pop("fn")
        return col_fn(**st_table_config)
