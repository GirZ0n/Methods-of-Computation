from math import exp
from typing import Callable, Dict, Type

import numpy as np
import streamlit as st
from sympy import integrate, lambdify
from sympy.abc import x
from sympy.functions import exp

from src.common.methods.numerical_integration.rectangle_methods import (
    LeftRectangleMethod,
    MiddleRectangleMethod,
    RightRectangleMethod,
    TrapezoidalMethod,
)
from src.common.methods.numerical_integration.simpson_methods import (
    FirstSimpsonMethod,
    SecondSimpsonMethod,
)
from src.common.model.line_segment import LineSegment
from src.common.model.numerical_integrator import NumericalIntegrator
from src.tasks.task4.subtask_1.common.state_var import StateVar
from src.tasks.task4.subtask_1.fragments.sidebar import show_sidebar

METHOD_TO_CONSTANT: Dict[Type[NumericalIntegrator], float] = {
    LeftRectangleMethod: 1 / 2,
    RightRectangleMethod: 1 / 2,
    MiddleRectangleMethod: 1 / 24,
    TrapezoidalMethod: 1 / 12,
    FirstSimpsonMethod: 1 / 2880,
    SecondSimpsonMethod: 1 / 6480,
}


def _get_theoretical_error(method: NumericalIntegrator, segment: LineSegment, f: Callable) -> float:
    constant = METHOD_TO_CONSTANT[method.__class__]
    h = segment.length / StateVar.NUMBER_OF_SEGMENTS.get()
    m = f(segment.right)

    return constant * m * segment.length * (h ** (method.accuracy_degree + 1))


def _show_result(precise_solution: float, approximate_solution: float, theoretical_error: float) -> None:
    st.markdown(f'$I_{{точн.}} = {precise_solution}$')
    st.markdown(f'$I_{{прибл.}} = {approximate_solution}$')

    st.markdown(f'$|R_{{теор.}}| = {theoretical_error}$')
    st.markdown(fr'$\left| R_{{факт.}} \right| = {abs(precise_solution - approximate_solution)}$')


def main():
    st.set_page_config(layout='wide')

    st.markdown(
        """
        <h1 style='text-align: center'>
            Сравнение теоретической и фактической погрешности квадратурных формул
        </h1>
        """,
        unsafe_allow_html=True,
    )

    show_sidebar()

    segment = LineSegment(StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get())

    f_expr = exp(x)
    f = np.vectorize(lambdify(x, f_expr))

    precise_solution = float(integrate(f_expr, (x, segment.left, segment.right)))

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader('Формула левых прямоугольников')
        method = LeftRectangleMethod()
        approximate_solution = method.integrate(f=f, segment=segment, n=StateVar.NUMBER_OF_SEGMENTS.get())
        theoretical_error = _get_theoretical_error(method, segment, f)
        _show_result(precise_solution, approximate_solution, theoretical_error)

    with right_column:
        st.subheader('Формула правых прямоугольников')
        method = RightRectangleMethod()
        approximate_solution = method.integrate(f=f, segment=segment, n=StateVar.NUMBER_OF_SEGMENTS.get())
        theoretical_error = _get_theoretical_error(method, segment, f)
        _show_result(precise_solution, approximate_solution, theoretical_error)

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader('Формула средних прямоугольников')
        method = MiddleRectangleMethod()
        approximate_solution = method.integrate(f=f, segment=segment, n=StateVar.NUMBER_OF_SEGMENTS.get())
        theoretical_error = _get_theoretical_error(method, segment, f)
        _show_result(precise_solution, approximate_solution, theoretical_error)

    with right_column:
        st.subheader('Формула трапеций')
        method = TrapezoidalMethod()
        approximate_solution = method.integrate(f=f, segment=segment, n=StateVar.NUMBER_OF_SEGMENTS.get())
        theoretical_error = _get_theoretical_error(method, segment, f)
        _show_result(precise_solution, approximate_solution, theoretical_error)

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader(r'Формула Симпсона $$(\left. 1 \middle/ 3 \right.)$$')
        method = FirstSimpsonMethod()
        approximate_solution = method.integrate(f=f, segment=segment, n=StateVar.NUMBER_OF_SEGMENTS.get())
        theoretical_error = _get_theoretical_error(method, segment, f)
        _show_result(precise_solution, approximate_solution, theoretical_error)

    with right_column:
        st.subheader(r'Формула Симпсона $$(\left. 3 \middle/ 8 \right.)$$')
        method = SecondSimpsonMethod()
        approximate_solution = method.integrate(f=f, segment=segment, n=StateVar.NUMBER_OF_SEGMENTS.get())
        theoretical_error = _get_theoretical_error(method, segment, f)
        _show_result(precise_solution, approximate_solution, theoretical_error)


if __name__ == '__main__':
    main()
