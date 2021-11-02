import numpy as np
import streamlit as st
from sympy import lambdify, parse_expr

from src.common.consts import TRANSFORMATIONS
from src.common.model.line_segment import LineSegment
from src.tasks.task4.subtask1.common.state_var import StateVar
from src.tasks.task4.subtask1.fragments.plots import show_cubic_simpson, show_polygon, show_quadratic_simpson
from src.tasks.task4.subtask1.fragments.sidebar import show_sidebar


def show_result(precise_solution: float, approximate_solution: float):
    st.markdown(f'$I_{{т}} = {precise_solution}$')
    st.markdown(f'$I_{{п}} = {precise_solution}$')
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

    f = np.vectorize(lambdify('x', parse_expr(StateVar.TEXT_EXPRESSION.get(), transformations=TRANSFORMATIONS)))

    segment = LineSegment(StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get())
    segments = segment.split_into_segments(StateVar.NUMBER_OF_SEGMENTS.get())

    st.header('Приближённые значения')

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader('Формула левых прямоугольников')
        show_result(0, 0)

    with right_column:
        st.subheader('Формула правых прямоугольников')
        show_result(0, 0)

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader('Формула средних прямоугольников')
        show_result(0, 0)

    with right_column:
        st.subheader('Формула трапеций')
        show_result(0, 0)

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader(r'Формула Симпсона $$(\left. 1 \middle/ 3 \right.)$$')
        show_result(0, 0)

    with right_column:
        st.subheader(r'Формула Симпсона $$(\left. 3 \middle/ 8 \right.)$$')
        show_result(0, 0)

    st.header('Визуализация методов')

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
