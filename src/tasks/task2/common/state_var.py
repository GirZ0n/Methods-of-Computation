from enum import Enum, unique
from typing import Any

import streamlit as st


@unique
class StateVar(Enum):
    TEXT_EXPRESSION = 'text_expression'
    LEFT_BOUNDARY = 'left_boundary'
    RIGHT_BOUNDARY = 'right_boundary'
    NUMBER_OF_NODES = 'number_of_nodes'
    POLYNOMIAL_DEGREE = 'polynomial_degree'
    INTERPOLATION_POINT = 'interpolation_point'

    def get(self) -> Any:
        return st.session_state[self.value]

    def set(self, value: Any) -> None:
        st.session_state[self.value] = value
