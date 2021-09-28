from enum import Enum, unique
from typing import Any, Optional

import streamlit as st


@unique
class StateVar(Enum):
    TEXT_EXPRESSION = 'text_expression'
    LEFT_BOUNDARY = 'left_boundary'
    RIGHT_BOUNDARY = 'right_boundary'
    NUMBER_OF_POINTS = 'number_of_points'
    POLYNOMIAL_DEGREE = 'polynomial_degree'
    INTERPOLATION_POINT = 'interpolation_point'
    RANDOM_STATE = 'random_state'

    def get(self, *, default: Optional[Any] = None) -> Optional[Any]:
        return st.session_state.get(self.value, default)

    def set(self, value: Any) -> None:
        st.session_state[self.value] = value
