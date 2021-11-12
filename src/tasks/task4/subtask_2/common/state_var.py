from enum import Enum, unique
from typing import Any, Optional

import streamlit as st


@unique
class StateVar(Enum):
    FUNCTION = 'function'
    WEIGHT_FUNCTION = 'weight_function'
    LEFT_BOUNDARY = 'left_boundary'
    RIGHT_BOUNDARY = 'right_boundary'
    NUMBER_OF_SEGMENTS = 'number_of_segments'

    def get(self, *, default: Optional[Any] = None) -> Optional[Any]:
        return st.session_state.get(self.value, default)

    def set(self, value: Any) -> None:
        st.session_state[self.value] = value
