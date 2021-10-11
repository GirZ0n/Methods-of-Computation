from enum import Enum, unique
from typing import Any, Optional

import streamlit as st


@unique
class StateVar(Enum):
    TEXT_EXPRESSION = 'text_expression'
    LEFT_BOUNDARY = 'left_boundary'
    NUMBER_OF_POINTS = 'number_of_points'
    STEP = 'step'
    PRECISION = 'precision'

    def get(self, *, default: Optional[Any] = None) -> Optional[Any]:
        return st.session_state.get(self.value, default)

    def set(self, value: Any) -> None:
        st.session_state[self.value] = value
