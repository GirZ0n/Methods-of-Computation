from typing import Type

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sympy import lambdify, parse_expr

from src.common.consts import COLOR, TRANSFORMATIONS
from src.common.model.interpolator import Interpolator
from src.tasks.task2.common.state_var import StateVar


def _show_plot(*, f, approximate_f, table: pd.DataFrame, approximate_value: float):
    fig = go.Figure()

    x = np.arange(
        min(StateVar.LEFT_BOUNDARY.get(), StateVar.INTERPOLATION_POINT.get()) - 1,
        max(StateVar.RIGHT_BOUNDARY.get(), StateVar.INTERPOLATION_POINT.get()) + 1,
        0.01,
    )
    fig.add_scatter(x=x, y=f(x), name='Искомая функция', marker_color=COLOR.LIGHT_GRAY.value)

    fig.add_scatter(x=x, y=approximate_f(x), name='Полученная функция', marker_color=COLOR.DARK_GRAY.value)

    fig.add_scatter(
        x=table['x'],
        y=table['y'],
        name='Узлы интерполяции',
        mode='markers',
        marker_color=COLOR.STREAMLIT_BLUE.value,
    )

    fig.add_scatter(
        x=[StateVar.INTERPOLATION_POINT.get()],
        y=[approximate_value],
        name='Приближённое решение',
        mode='markers',
        marker_color=COLOR.STREAMLIT.value,
    )

    st.plotly_chart(fig, use_container_width=True)


def show_interpolation_results(
    *,
    interpolator_class: Type[Interpolator],
    table: pd.DataFrame,
    interpolator_name: str,
    interpolator_symbol: str,
):
    st.header(interpolator_name)

    interpolator = interpolator_class()

    approximate_value = interpolator.get_approximate_value(StateVar.INTERPOLATION_POINT.get(), table)
    st.markdown(f'$$P_n^{interpolator_symbol}(x) = {approximate_value}$$')

    f = lambdify('x', parse_expr(StateVar.TEXT_EXPRESSION.get(), transformations=TRANSFORMATIONS))
    difference = abs(approximate_value - f(StateVar.INTERPOLATION_POINT.get()))
    st.markdown(f'$$|f(x) - P_n^{interpolator_symbol}(x)| = {difference:e}$$')

    with st.expander('График'):
        _show_plot(
            f=f,
            approximate_f=lambda x: interpolator.get_approximate_value(x, table),
            table=table,
            approximate_value=approximate_value,
        )
