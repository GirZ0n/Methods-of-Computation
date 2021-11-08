import sys

import numpy as np
import streamlit as st
from sympy import integrate, lambdify, parse_expr

sys.path.append('')
sys.path.append('../../..')

from src.common.consts import TRANSFORMATIONS
from src.common.methods.numerical_integration.rectangle_methods import (
    LeftRectangleMethod,
    MiddleRectangleMethod,
    RightRectangleMethod,
    TrapezoidalMethod,
)
from src.common.methods.numerical_integration.simpson_methods import FirstSimpsonMethod, SecondSimpsonMethod
from src.common.model.line_segment import LineSegment
from src.tasks.task4.subtask1.common.state_var import StateVar
from src.tasks.task4.subtask1.fragments.plots import show_cubic_simpson, show_polygon, show_quadratic_simpson
from src.tasks.task4.subtask1.fragments.sidebar import show_sidebar


def show_result(precise_solution: float, approximate_solution: float):
    st.markdown(f'$I_{{т}} = {precise_solution}$')
    st.markdown(f'$I_{{п}} = {approximate_solution}$')
    st.markdown(fr'$\left| I_{{т}} - I_{{п}} \right| = {abs(precise_solution - approximate_solution)}$')


if __name__ == '__main__':
    st.set_page_config(layout='wide')

    st.markdown(
        """
        <h1 style='text-align: center'>
            Приближённое вычисление интеграла по квадратурным формулам
        </h1>
        """,
        unsafe_allow_html=True,
    )

    show_sidebar()

    f_expression = parse_expr(StateVar.TEXT_EXPRESSION.get(), transformations=TRANSFORMATIONS)
    f = np.vectorize(lambdify('x', f_expression))
    precise_solution = integrate(f_expression, ('x', StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get()))
    precise_solution = precise_solution.evalf()

    segment = LineSegment(StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get())

    st.header('Приближённые значения')

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader('Формула левых прямоугольников')
        method = LeftRectangleMethod()
        approximate_solution = method.integrate(f=f, segment=segment, n=StateVar.NUMBER_OF_SEGMENTS.get())
        show_result(precise_solution, approximate_solution)

    with right_column:
        st.subheader('Формула правых прямоугольников')
        method = RightRectangleMethod()
        approximate_solution = method.integrate(f=f, segment=segment, n=StateVar.NUMBER_OF_SEGMENTS.get())
        show_result(precise_solution, approximate_solution)

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader('Формула средних прямоугольников')
        method = MiddleRectangleMethod()
        approximate_solution = method.integrate(f=f, segment=segment, n=StateVar.NUMBER_OF_SEGMENTS.get())
        show_result(precise_solution, approximate_solution)

    with right_column:
        st.subheader('Формула трапеций')
        method = TrapezoidalMethod()
        approximate_solution = method.integrate(f=f, segment=segment, n=StateVar.NUMBER_OF_SEGMENTS.get())
        show_result(precise_solution, approximate_solution)

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader(r'Формула Симпсона $$(\left. 1 \middle/ 3 \right.)$$')
        method = FirstSimpsonMethod()
        approximate_solution = method.integrate(f=f, segment=segment, n=StateVar.NUMBER_OF_SEGMENTS.get())
        show_result(precise_solution, approximate_solution)

    with right_column:
        st.subheader(r'Формула Симпсона $$(\left. 3 \middle/ 8 \right.)$$')
        method = SecondSimpsonMethod()
        approximate_solution = method.integrate(f=f, segment=segment, n=StateVar.NUMBER_OF_SEGMENTS.get())
        show_result(precise_solution, approximate_solution)

    st.header('Визуализация методов')

    segments = segment.split_into_segments(StateVar.NUMBER_OF_SEGMENTS.get())

    st.subheader('Формула левых прямоугольников')
    show_polygon(f, segments, 'left')

    st.subheader('Формула правых прямоугольников')
    show_polygon(f, segments, 'right')

    st.subheader('Формула средних прямоугольников')
    show_polygon(f, segments, 'center')

    st.subheader('Формула трапеций')
    show_polygon(f, segments, 'trapezoid')

    st.subheader(r'Формула Симпсона $$(\left. 1 \middle/ 3 \right.)$$')
    show_quadratic_simpson(f, segments)

    st.subheader(r'Формула Симпсона $$(\left. 3 \middle/ 8 \right.)$$')
    show_cubic_simpson(f, segments)
