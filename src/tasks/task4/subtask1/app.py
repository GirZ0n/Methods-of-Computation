import numpy as np
import streamlit as st
from sympy import lambdify, latex, parse_expr

from src.common.consts import TRANSFORMATIONS
from src.common.model.line_segment import LineSegment
from src.tasks.task4.subtask1.common.state_var import StateVar
from src.tasks.task4.subtask1.fragments.plots import show_cubic_simpson, show_polygon, show_quadratic_simpson
from src.tasks.task4.subtask1.fragments.sidebar import show_sidebar


def show_result(precise_solution: float, approximate_solution: float):
    # st.markdown(
    #     fr"""
    #     $\underbrace{{ \int_b^a f(x) dx }}_{{ I_p }}
    #     \approx \underbrace{{ \vphantom{{ \int_b^a f(x) }} {approximate_solution} }}_{{ I_a }}$
    #     """
    # )

    st.markdown(fr'$\displaystyle I_p = {precise_solution} = \int_{{{StateVar.LEFT_BOUNDARY.get()}}}^{{{StateVar.RIGHT_BOUNDARY.get()}}} f(x) dx \approx {approximate_solution} = I_a$')
    st.markdown(fr"$\left| I_p - I_a \right| = {abs(precise_solution - approximate_solution)}$")


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
        st.subheader('Метод левых прямоугольников')
        show_result(0, 0)

    with right_column:
        st.subheader('Метод правых прямоугольников')
        show_result(0, 0)

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader('Метод средних прямоугольников')
        show_result(0, 0)

    with right_column:
        st.subheader('Метод трапеций')
        show_result(0, 0)

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader(r'Метод Симпсона $$(\left. 1 \middle/ 3 \right.)$$')
        show_result(0, 0)

    with right_column:
        st.subheader(r'Метод Симпсона $$(\left. 3 \middle/ 8 \right.)$$')
        show_result(0, 0)

    st.header('Визуализация методов')

    st.subheader('Метод левых прямоугольников')
    show_polygon(f, segments, 'left')

    st.subheader('Метод правых прямоугольников')
    show_polygon(f, segments, 'right')

    st.subheader('Метод средних прямоугольников')
    show_polygon(f, segments, 'center')

    st.subheader('Метод трапеций')
    show_polygon(f, segments, 'trapezoid')

    st.subheader(r'Метод Симпсона $$(\left. 1 \middle/ 3 \right.)$$')
    show_quadratic_simpson(f, segments)

    st.subheader(r'Метод Симпсона $$(\left. 3 \middle/ 8 \right.)$$')
    show_cubic_simpson(f, segments)
