from enum import Enum, unique
from typing import Any, Optional

import streamlit as st


@unique
class StateVar(Enum):
    FUNCTION = 'function'
    LEFT_BOUNDARY = 'left_boundary'
    RIGHT_BOUNDARY = 'right_boundary'
    PRECISION = 'precision'
    SHOW_TABLE = 'show_table'
    SHOW_PRECISE_SOLUTION = 'show_precise_solution'

    def get(self, *, default: Optional[Any] = None) -> Optional[Any]:
        return st.session_state.get(self.value, default)

    def set(self, value: Any) -> None:
        st.session_state[self.value] = value
