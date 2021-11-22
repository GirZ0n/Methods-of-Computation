import sys
from typing import Callable

import numpy as np
import streamlit as st
from sympy import integrate, lambdify, parse_expr

sys.path.append('')
sys.path.append('../../../..')

from src.common.consts import TRANSFORMATIONS
from src.common.methods.numerical_integration.rectangle_methods import (
    OptimizedLeftRectangleMethod,
    OptimizedMiddleRectangleMethod,
    OptimizedRightRectangleMethod,
    OptimizedTrapezoidalMethod,
)
from src.common.methods.numerical_integration.simpson_methods import (
    OptimizedFirstSimpsonMethod,
    SecondSimpsonMethod,
)
from src.common.model.line_segment import LineSegment
from src.tasks.task4.subtask_2.common.state_var import StateVar
from src.tasks.task4.subtask_2.fragments.plots import show_cubic_simpson, show_polygon, show_quadratic_simpson
from src.tasks.task4.subtask_2.fragments.sidebar import show_sidebar


def _show_result(precise_solution: float, approximate_solution: float):
    st.markdown(f'$I_{{точн.}} = {precise_solution}$')
    st.markdown(f'$I_{{прибл.}} = {approximate_solution}$')
    st.markdown(fr'$\left| I_{{точн.}} - I_{{прибл.}} \right| = {abs(precise_solution - approximate_solution)}$')


def _calculate_boundary_sum(f: Callable, segment: LineSegment) -> float:
    return f(segment.left) + f(segment.right)


def _calculate_inner_sum(f: Callable, segment: LineSegment) -> float:
    points = segment.split_into_points(StateVar.NUMBER_OF_SEGMENTS.get())
    points.pop(0)
    points.pop(-1)

    return sum(f(point) for point in points)


def _calculate_middle_sum(f: Callable, segment: LineSegment) -> float:
    segments = segment.split_into_segments(StateVar.NUMBER_OF_SEGMENTS.get())
    return sum(f(curr_segment.midpoint) for curr_segment in segments)


def show_quadrature_formulas() -> None:
    st.markdown(
        """
        <h1 style='text-align: center'>
            Приближённое вычисление интеграла по квадратурным формулам
        </h1>
        """,
        unsafe_allow_html=True,
    )

    show_sidebar()

    f_expression = parse_expr(StateVar.FUNCTION.get(), transformations=TRANSFORMATIONS)
    f = np.vectorize(lambdify('x', f_expression))
    precise_solution = float(
        integrate(f_expression, ('x', StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get())),
    )

    segment = LineSegment(StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get())

    boundary_sum = _calculate_boundary_sum(f, segment)
    inner_sum = _calculate_inner_sum(f, segment)
    middle_sum = _calculate_middle_sum(f, segment)

    st.header('Приближённые значения')

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader('Формула левых прямоугольников')
        method = OptimizedLeftRectangleMethod()
        approximate_solution = method.integrate(
            f=f,
            segment=segment,
            n=StateVar.NUMBER_OF_SEGMENTS.get(),
            inner_sum=inner_sum,
        )
        _show_result(precise_solution, approximate_solution)

    with right_column:
        st.subheader('Формула правых прямоугольников')
        method = OptimizedRightRectangleMethod()
        approximate_solution = method.integrate(
            f=f,
            segment=segment,
            n=StateVar.NUMBER_OF_SEGMENTS.get(),
            inner_sum=inner_sum,
        )
        _show_result(precise_solution, approximate_solution)

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader('Формула средних прямоугольников')
        method = OptimizedMiddleRectangleMethod()
        approximate_solution = method.integrate(
            f=f,
            segment=segment,
            n=StateVar.NUMBER_OF_SEGMENTS.get(),
            middle_sum=middle_sum,
        )
        _show_result(precise_solution, approximate_solution)

    with right_column:
        st.subheader('Формула трапеций')
        method = OptimizedTrapezoidalMethod()
        approximate_solution = method.integrate(
            f=f,
            segment=segment,
            n=StateVar.NUMBER_OF_SEGMENTS.get(),
            boundary_sum=boundary_sum,
            inner_sum=inner_sum,
        )
        _show_result(precise_solution, approximate_solution)

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader(r'Формула Симпсона $$(\left. 1 \middle/ 3 \right.)$$')
        method = OptimizedFirstSimpsonMethod()
        approximate_solution = method.integrate(
            f=f,
            segment=segment,
            n=StateVar.NUMBER_OF_SEGMENTS.get(),
            inner_sum=inner_sum,
            boundary_sum=boundary_sum,
            middle_sum=middle_sum,
        )
        _show_result(precise_solution, approximate_solution)

    with right_column:
        st.subheader(r'Формула Симпсона $$(\left. 3 \middle/ 8 \right.)$$')
        method = SecondSimpsonMethod()
        approximate_solution = method.integrate(f=f, segment=segment, n=StateVar.NUMBER_OF_SEGMENTS.get())
        _show_result(precise_solution, approximate_solution)

    st.header('Визуализация методов')

    if StateVar.NUMBER_OF_SEGMENTS.get() > 50:
        st.warning('Количество частей слишком велико для визуализации (максимум: 50)')
    elif segment.length > 100:
        st.warning('Отрезок слишком длинный для визуализации (максимум: 100).')
    else:
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


if __name__ == '__main__':
    st.set_page_config(layout='wide')
    show_quadrature_formulas()
