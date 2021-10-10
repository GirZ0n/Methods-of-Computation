from typing import Dict, List

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sympy import lambdify, parse_expr

from src.common.config import OUTPUT_PRECISION
from src.common.consts import COLOR, TRANSFORMATIONS
from src.common.methods.interpolators.lagrange_interpolator import LagrangeInterpolator
from src.common.methods.interpolators.newton_interpolator import NewtonInterpolator
from src.common.methods.root_finding.bisection_method import BisectionMethod
from src.common.methods.root_finding.secant_method import SecantMethod
from src.common.methods.root_separation.segment_tabulation import Tabulator
from src.common.model.interpolator import Interpolator
from src.common.model.line_segment import LineSegment
from src.common.model.root_finder import RootFinder
from src.tasks.task3.subtask1.common.state_var import StateVar

INTERPOLATOR_MAP: Dict[str, Interpolator] = {
    'Интерполяция Лагранжа': LagrangeInterpolator(),
    'Интерполяция Ньютона': NewtonInterpolator(),
}

ROOT_FINDER_MAP: Dict[str, RootFinder] = {
    'Метод бисекции': BisectionMethod(),
    'Метод секущих': SecantMethod(),
}


def _get_interpolation_table(
    table: pd.DataFrame,
    *,
    point: float,
    column: str = 'y',
) -> pd.DataFrame:
    interpolation_table = table.sort_values(
        by=[column],
        key=lambda current_node: abs(current_node - point),
    )
    return interpolation_table[: StateVar.POLYNOMIAL_DEGREE.get() + 1].reset_index(drop=True)


def _equation(point: float, interpolator: Interpolator, interpolation_table: pd.DataFrame) -> float:
    return interpolator.get_approximate_value(point, interpolation_table) - StateVar.INTERPOLATION_POINT.get()


def _show_plot(*, f, approximate_f, table: pd.DataFrame, approximate_arguments: List[float]):
    fig = go.Figure()

    x = np.arange(
        min([StateVar.LEFT_BOUNDARY.get(), *approximate_arguments]),
        max([StateVar.RIGHT_BOUNDARY.get(), *approximate_arguments]) + 0.01,
        0.01,
    )

    fig.add_scatter(
        x=x,
        y=f(x),
        name='Искомая функция',
        marker_color=COLOR.LIGHT_GRAY.value,
    )

    fig.add_scatter(
        x=x,
        y=approximate_f(x),
        name='Полученная функция',
        marker_color=COLOR.DARK_GRAY.value,
    )

    fig.add_scatter(
        x=table['x'],
        y=table['y'],
        name='Узлы интерполяции',
        mode='markers',
        marker_color=COLOR.STREAMLIT_BLUE.value,
    )

    fig.add_scatter(
        x=approximate_arguments,
        y=[StateVar.INTERPOLATION_POINT.get() for _ in approximate_arguments],
        name='Приближённое решение',
        mode='markers',
        marker_color=COLOR.STREAMLIT.value,
    )

    fig.update_xaxes(title='x')
    fig.update_yaxes(title='y')

    st.plotly_chart(fig, use_container_width=True)


def show_nonlinear_equation_method(table: pd.DataFrame):
    st.header('Метод решения c помощью нелинейного уравнения')

    interpolator_names = st.multiselect('Выберите интерполяционный метод:', options=INTERPOLATOR_MAP.keys())
    root_finder_names = st.multiselect('Выберите метод нахождения корней:', options=ROOT_FINDER_MAP.keys())
    number_of_parts = int(st.number_input('Количество частей:', value=1000))
    accuracy = float(st.number_input('Точность:', value=1e-8, step=1e-1, format='%e'))

    f = lambdify('x', parse_expr(StateVar.TEXT_EXPRESSION.get(), transformations=TRANSFORMATIONS))
    line_segment = LineSegment(StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get() + 0.01)

    for interpolator_name in interpolator_names:
        interpolator = INTERPOLATOR_MAP[interpolator_name]
        for root_finder_name in root_finder_names:
            root_finder = ROOT_FINDER_MAP[root_finder_name]

            st.subheader(f'{interpolator_name} + {root_finder_name}')

            interpolation_table = _get_interpolation_table(
                table,
                point=StateVar.INTERPOLATION_POINT.get(),
            )

            tabulator = Tabulator(number_of_parts)
            segments = tabulator.separate(
                f=lambda x: _equation(x, interpolator, interpolation_table),
                line_segment=line_segment,
            )

            if not segments:
                st.write('Аргументы не найдены! :cry:')

            arguments = []
            for index, segment in enumerate(segments):
                approximate_argument = root_finder.find(
                    derivatives=[lambda x: _equation(x, interpolator, interpolation_table)],
                    line_segment=segment,
                    accuracy=accuracy,
                )

                arguments.append(approximate_argument)
                st.markdown(f'$$x_{index} = {approximate_argument}$$')
                difference = abs(f(approximate_argument) - StateVar.INTERPOLATION_POINT.get())
                st.markdown(f'$$|f(x_{index}) - y| = {difference:.{OUTPUT_PRECISION}e}$$')

            with st.expander('График:'):
                _show_plot(
                    f=f,
                    approximate_f=(
                        lambda x: _equation(x, interpolator, interpolation_table) + StateVar.INTERPOLATION_POINT.get()
                    ),
                    table=interpolation_table,
                    approximate_arguments=arguments,
                )
