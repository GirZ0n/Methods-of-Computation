import sys
from typing import List

import streamlit as st
from sympy import parse_expr
from sympy.parsing.sympy_parser import (
    convert_xor,
    function_exponentiation,
    implicit_application,
    implicit_multiplication,
    split_symbols,
    standard_transformations,
)

sys.path.append('')
sys.path.append('../../..')

from src.common.config import OUTPUT_PRECISION
from src.common.methods.root_separation.segment_tabulation import Tabulator
from src.common.model.line_segment import LineSegment
from src.tasks.task1.main import METHOD_NAME_TO_ROOT_FINDER

TRANSFORMATIONS = standard_transformations + (
    split_symbols,
    implicit_application,
    implicit_multiplication,
    function_exponentiation,
    convert_xor,
)


def root_separation(*, number_of_parts: int, expression, line_segment: LineSegment) -> List[LineSegment]:
    tabulator = Tabulator(number_of_parts)
    segments = tabulator.separate(expression=expression, line_segment=line_segment)

    for index, segment in enumerate(segments):
        st.markdown(f'{index + 1}. ${segment}$')

    return segments


def root_find(*, segments: List[LineSegment], method_name: str, expression, accuracy: float):
    root_finder = METHOD_NAME_TO_ROOT_FINDER[method_name]

    for number, segment in enumerate(segments, start=1):
        root_finder.find(expression=expression, line_segment=segment, accuracy=accuracy)
        stats = root_finder.stats

        st.subheader(f'Отрезок №{number}')

        st.markdown(
            f"""
            - Отрезок: ${stats.line_segment}$<br/>
            - Начальное приближение: ${stats.round_initial_approximation()}$<br/>
            - Количество шагов: ${stats.number_of_steps}$<br/>
            - $x_m = {round(stats.approximate_solution, OUTPUT_PRECISION)}$<br/>
            - $|x_m - x_{{m-1}}| = {round(stats.error, OUTPUT_PRECISION)}$<br/>
            - $|f(x_m)| = {round(stats.residual, OUTPUT_PRECISION)}$<br/>
            """,
            unsafe_allow_html=True,
        )


def app():
    with st.sidebar:
        st.header('Параметры')

        text_expression = st.text_input('Выражение:', value='x - 10 * sin(x)')

        left_column, right_column = st.columns(2)

        with left_column:
            a = st.number_input('A:', value=-5)

        with right_column:
            b = st.number_input('B:', value=3)

        accuracy = st.number_input('Точность:', value=10 ** -6, format='%e')

        number_of_parts = st.number_input('Количество частей:', value=1000)

    expression = parse_expr(text_expression)
    line_segment = LineSegment(a, b)

    st.title('Численные методы решения нелинейных уравнений')

    method_name = st.selectbox('Метод:', options=METHOD_NAME_TO_ROOT_FINDER.keys())

    st.subheader('Отделение корней')
    segments = root_separation(number_of_parts=number_of_parts, expression=expression, line_segment=line_segment)

    # st.subheader('Уточнение корней')
    root_find(segments=segments, method_name=method_name, accuracy=accuracy, expression=expression)


if __name__ == '__main__':
    app()
