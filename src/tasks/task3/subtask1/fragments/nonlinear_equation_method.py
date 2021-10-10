from typing import Dict, Type

import numpy as np
import pandas as pd
import streamlit as st
from sympy import lambdify, parse_expr

from src.common.consts import TRANSFORMATIONS
from src.common.methods.interpolators.lagrange_interpolator import LagrangeInterpolator
from src.common.methods.interpolators.newton_interpolator import NewtonInterpolator
from src.common.methods.root_finding.bisection_method import BisectionMethod
from src.common.methods.root_finding.secant_method import SecantMethod
from src.common.methods.root_separation.segment_tabulation import Tabulator
from src.common.model.interpolator import Interpolator
from src.common.model.line_segment import LineSegment
from src.common.model.root_finder import RootFinder
from src.tasks.task2.fragments.interpolation import show_interpolation_results
from src.tasks.task3.subtask1.common.state_var import StateVar
import plotly.express as px


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
    polynomial_degree: int,
    column: str = 'x',
) -> pd.DataFrame:
    return table.sort_values(by=[column], key=lambda current_node: abs(current_node - point))[: polynomial_degree + 1]


def _equation(x: float, interpolator: Interpolator, table: pd.DataFrame) -> float:
    # f = lambdify('x', parse_expr(StateVar.TEXT_EXPRESSION.get(), transformations=TRANSFORMATIONS))
    # print(x)
    # return f(x) - StateVar.INTERPOLATION_POINT.get()
    interpolation_table = _get_interpolation_table(table, point=x, polynomial_degree=StateVar.POLYNOMIAL_DEGREE.get(), column='y')
    # st.dataframe(interpolation_table)
    # st.plotly_chart(px.scatter(x=interpolation_table['x'], y=interpolation_table['y']))
    return interpolator.get_approximate_value(x, interpolation_table) - StateVar.INTERPOLATION_POINT.get()


def show_nonlinear_equation_method(table: pd.DataFrame):
    st.header('Метод решения c помощью нелинейного уравнения')

    interpolator_names = st.multiselect(
        'Выберите интерполяционный метод:',
        options=INTERPOLATOR_MAP.keys(),
        default=['Интерполяция Лагранжа'],
    )
    root_finder_names = st.multiselect(
        'Выберите метод нахождения корней:',
        options=ROOT_FINDER_MAP.keys(),
        default=['Метод бисекции'],
    )
    # number_of_parts = int(st.number_input('Количество частей:', value=1000))
    # accuracy = float(st.number_input('Точность:', value=1e-8, step=1e-1, format='%e'))
    number_of_parts = 1000
    accuracy = 1e-8

    line_segment = LineSegment(StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get() + 0.01)

    for interpolator_name in interpolator_names:
        interpolator = INTERPOLATOR_MAP[interpolator_name]
        for root_finder_name in root_finder_names:
            root_finder = ROOT_FINDER_MAP[root_finder_name]

            st.subheader(f'{interpolator_name} + {root_finder_name}')

            tabulator = Tabulator(number_of_parts)
            segments = tabulator.separate(f=lambda x: _equation(x, interpolator, table), line_segment=line_segment)
            st.write(segments)

            # x = float(st.number_input('qwe'))
            # st.write(x)
            # interpolation_table = _get_interpolation_table(
            #     table,
            #     point=x,
            #     polynomial_degree=StateVar.POLYNOMIAL_DEGREE.get(),
            # )
            # st.write(interpolation_table.dtypes.tolist())
            # st.write(interpolation_table)
            # st.write(interpolator().get_approximate_value(x, table))
            #
            # show_interpolation_results(
            #     interpolator_class=interpolator,
            #     table=interpolation_table,
            #     interpolator_name='L',
            #     interpolator_symbol='L',
            # )
            #
            # x = np.arange(line_segment.left, line_segment.right, 0.01)
            # fig = px.scatter(x=x, y=[interpolator().get_approximate_value(elem, interpolation_table) for elem in x])
            # st.plotly_chart(fig)

            for index, segment in enumerate(segments):
                approximate_argument = root_finder.find(
                    derivatives=[lambda x: _equation(x, interpolator, table)],
                    line_segment=segment,
                    accuracy=accuracy,
                )

                st.write(approximate_argument)
