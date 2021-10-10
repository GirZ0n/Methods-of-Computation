import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sympy import lambdify, parse_expr

from src.common.config import OUTPUT_PRECISION
from src.common.consts import COLOR, TRANSFORMATIONS
from src.common.methods.interpolators.lagrange_interpolator import LagrangeInterpolator
from src.common.methods.interpolators.newton_interpolator import NewtonInterpolator
from src.common.utils import plot_on_horizontal_axis
from src.tasks.task3.subtask1.common.state_var import StateVar

INTERPOLATOR_MAP = {
    'Интерполяция Лагранжа': LagrangeInterpolator(),
    'Интерполяция Ньютона': NewtonInterpolator(),
}


def _get_interpolation_table(
    table: pd.DataFrame,
    *,
    point: float,
    polynomial_degree: int,
    column: str = 'x',
) -> pd.DataFrame:
    return table.sort_values(by=[column], key=lambda current_node: abs(current_node - point))[: polynomial_degree + 1]


def _show_plot(*, f, approximate_f, table: pd.DataFrame, approximate_value: float):
    fig = go.Figure()

    x = np.arange(
        StateVar.LEFT_BOUNDARY.get(),
        StateVar.RIGHT_BOUNDARY.get() + 0.01,
        0.01,
    )
    fig.add_scatter(x=f(x), y=x, name='Искомая обратная функция', marker_color=COLOR.LIGHT_GRAY.value)

    x = np.arange(
        f(StateVar.LEFT_BOUNDARY.get()),
        f(StateVar.RIGHT_BOUNDARY.get()) + 0.01,
        0.01,
    )

    fig.add_scatter(x=x, y=approximate_f(x), name='Полученная обратная функция', marker_color=COLOR.DARK_GRAY.value)

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
        name='Приближённый аргумент',
        mode='markers',
        marker_color=COLOR.STREAMLIT.value,
    )

    fig.update_xaxes(title='y')
    fig.update_yaxes(title='x')

    st.plotly_chart(fig, use_container_width=True)


def show_axis_rotation_method(table: pd.DataFrame):
    st.header('Метод смены осей')

    st.warning('Внимание! Данный метод нельзя использовать с немонотонными функциями!')

    st.subheader('Узлы интерполяции')
    table = _get_interpolation_table(
        table,
        point=StateVar.INTERPOLATION_POINT.get(),
        polynomial_degree=StateVar.POLYNOMIAL_DEGREE.get(),
        column='y',
    )

    table['abs'] = abs(table['y'] - StateVar.INTERPOLATION_POINT.get())
    table.reset_index(inplace=True, drop=True)

    st.plotly_chart(
        plot_on_horizontal_axis(table, 'y', extra_points=[StateVar.INTERPOLATION_POINT.get()]),
        use_container_width=True,
    )

    st.dataframe(table.T)

    table.drop(columns=['abs'])
    table = table.rename(columns={'x': 'y', 'y': 'x'})

    interpolator_names = st.multiselect('Выберите интерполяционный метод:', options=INTERPOLATOR_MAP.keys(), key='arm')
    for interpolator_name in interpolator_names:
        st.subheader(interpolator_name)

        interpolator = INTERPOLATOR_MAP[interpolator_name]

        approximate_value = interpolator.get_approximate_value(StateVar.INTERPOLATION_POINT.get(), table)
        st.markdown(f'$$Q_n(y) = {approximate_value}$$')

        f = lambdify('x', parse_expr(StateVar.TEXT_EXPRESSION.get(), transformations=TRANSFORMATIONS))
        difference = abs(f(approximate_value) - StateVar.INTERPOLATION_POINT.get())
        st.markdown(f'$$|f(Q(y)) - y| = {difference:.{OUTPUT_PRECISION}e}$$')

        with st.expander('График'):
            _show_plot(
                f=f,
                approximate_f=lambda y: interpolator.get_approximate_value(y, table),
                table=table,
                approximate_value=approximate_value,
            )
