from typing import Callable

import numpy as np
import streamlit as st
from sympy import integrate, lambdify, parse_expr

from src.common.consts import TRANSFORMATIONS
from src.common.methods.numerical_integration.rectangle_methods import (
    OptimizedLeftRectangleMethod,
    OptimizedMiddleRectangleMethod,
    OptimizedRightRectangleMethod,
    OptimizedTrapezoidalMethod,
)
from src.common.methods.numerical_integration.simpson_methods import OptimizedFirstSimpsonMethod, SecondSimpsonMethod
from src.common.model.line_segment import LineSegment
from src.tasks.task4.subtask_3.common.state_var import StateVar
from src.tasks.task4.subtask_3.fragments.sidebar import show_sidebar


def _show_result(precise_solution: float, approximate_solution: float, approximate_solution_lx: float, r: int):
    st.markdown(f'$J = {precise_solution}$')
    st.markdown(f'$J(h) = {approximate_solution}$')
    st.markdown(f'$J(h/l) = {approximate_solution_lx}$')

    l = StateVar.MULTIPLIER.get()  # noqa: E741
    refined_solution = (l ** r * approximate_solution_lx - approximate_solution) / (l ** r - 1)

    st.markdown(rf'$\overline{{J}} = {refined_solution}$')

    st.markdown(fr'$\left| J - J(h) \right| = {abs(precise_solution - approximate_solution)}$')
    st.markdown(fr'$\left| J - J(h/l) \right| = {abs(precise_solution - approximate_solution_lx)}$')
    st.markdown(fr'$\left| J - \overline{{J}} \right| = {abs(precise_solution - refined_solution)}$')


def _calculate_boundary_sum(f: Callable, segment: LineSegment) -> float:
    return f(segment.left) + f(segment.right)


def _calculate_inner_sum(f: Callable, segment: LineSegment, n: int) -> float:
    points = segment.split_into_points(n)
    points.pop(0)
    points.pop(-1)

    return sum(f(point) for point in points)


def _calculate_middle_sum(f: Callable, segment: LineSegment, n: int) -> float:
    segments = segment.split_into_segments(n)
    return sum(f(curr_segment.midpoint) for curr_segment in segments)


def main():
    st.set_page_config(layout='wide')

    st.markdown(
        """
        <h1 style='text-align: center'>
            Принцип Рунге
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
    inner_sum = _calculate_inner_sum(f, segment, StateVar.NUMBER_OF_SEGMENTS.get())
    middle_sum = _calculate_middle_sum(f, segment, StateVar.NUMBER_OF_SEGMENTS.get())

    boundary_sum_lx = _calculate_boundary_sum(f, segment)
    inner_sum_lx = _calculate_inner_sum(f, segment, StateVar.NUMBER_OF_SEGMENTS.get() * StateVar.MULTIPLIER.get())
    middle_sum_lx = _calculate_middle_sum(f, segment, StateVar.NUMBER_OF_SEGMENTS.get() * StateVar.MULTIPLIER.get())

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
        approximate_solution_lx = method.integrate(
            f=f,
            segment=segment,
            n=(StateVar.NUMBER_OF_SEGMENTS.get() * StateVar.MULTIPLIER.get()),
            inner_sum=inner_sum_lx,
        )
        _show_result(precise_solution, approximate_solution, approximate_solution_lx, method.accuracy_degree + 1)

    with right_column:
        st.subheader('Формула правых прямоугольников')
        method = OptimizedRightRectangleMethod()
        approximate_solution = method.integrate(
            f=f,
            segment=segment,
            n=StateVar.NUMBER_OF_SEGMENTS.get(),
            inner_sum=inner_sum,
        )
        approximate_solution_lx = method.integrate(
            f=f,
            segment=segment,
            n=StateVar.NUMBER_OF_SEGMENTS.get() * StateVar.MULTIPLIER.get(),
            inner_sum=inner_sum_lx,
        )
        _show_result(precise_solution, approximate_solution, approximate_solution_lx, method.accuracy_degree + 1)

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
        approximate_solution_lx = method.integrate(
            f=f,
            segment=segment,
            n=StateVar.NUMBER_OF_SEGMENTS.get() * StateVar.MULTIPLIER.get(),
            middle_sum=middle_sum_lx,
        )
        _show_result(precise_solution, approximate_solution, approximate_solution_lx, method.accuracy_degree + 1)

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
        approximate_solution_lx = method.integrate(
            f=f,
            segment=segment,
            n=StateVar.NUMBER_OF_SEGMENTS.get() * StateVar.MULTIPLIER.get(),
            boundary_sum=boundary_sum_lx,
            inner_sum=inner_sum_lx,
        )
        _show_result(precise_solution, approximate_solution, approximate_solution_lx, method.accuracy_degree + 1)

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
        approximate_solution_lx = method.integrate(
            f=f,
            segment=segment,
            n=StateVar.NUMBER_OF_SEGMENTS.get() * StateVar.MULTIPLIER.get(),
            inner_sum=inner_sum_lx,
            boundary_sum=boundary_sum_lx,
            middle_sum=middle_sum_lx,
        )
        _show_result(precise_solution, approximate_solution, approximate_solution_lx, method.accuracy_degree + 1)

    with right_column:
        st.subheader(r'Формула Симпсона $$(\left. 3 \middle/ 8 \right.)$$')
        method = SecondSimpsonMethod()
        approximate_solution = method.integrate(f=f, segment=segment, n=StateVar.NUMBER_OF_SEGMENTS.get())
        approximate_solution_lx = method.integrate(
            f=f,
            segment=segment,
            n=StateVar.NUMBER_OF_SEGMENTS.get() * StateVar.MULTIPLIER.get(),
        )
        _show_result(precise_solution, approximate_solution, approximate_solution_lx, method.accuracy_degree + 1)


if __name__ == '__main__':
    main()
