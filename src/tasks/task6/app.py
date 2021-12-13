import operator
from itertools import cycle, islice

import numpy as np
import pandas as pd
import streamlit as st
from sympy import Symbol, integrate, lambdify, latex, parse_expr

from src.common.consts import TRANSFORMATIONS
from src.common.methods.numerical_integration.gaussian_method import (
    GaussianMethod,
    get_gaussian_coefficients,
    get_gaussian_roots,
)
from src.common.model.line_segment import LineSegment
from src.common.utils import plot_on_horizontal_axis
from src.tasks.task6.common.state_var import StateVar
from src.tasks.task6.fragments.sidebar import show_sidebar


def _calculate_moment(rho, n: int, a: int, b: int) -> float:
    expr = rho * Symbol('x') ** n
    return float(integrate(expr, ('x', a, b)))


def gaussian_method_with_weight(n: int) -> float:
    rho = parse_expr(StateVar.WEIGHT.get(), transformations=TRANSFORMATIONS)
    f_expr = parse_expr(StateVar.FUNCTION.get(), transformations=TRANSFORMATIONS)
    f = lambdify('x', f_expr)

    moments = []
    for i in range(2 * n):  # noqa: WPS440
        moments.append(_calculate_moment(rho, i, StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get()))

    a = []
    for i in range(n):  # noqa: WPS440
        a.append(list(reversed(list(islice(cycle(moments), i, i + n)))))

    b = []
    for i in range(n, 2 * n):  # noqa: WPS440
        b.append(moments[i] * -1)

    polynomial_coefficients = np.linalg.solve(a, b)
    polynomial_coefficients = np.concatenate(([1], polynomial_coefficients))

    polynomial = sum(
        (Symbol('x') ** power * coefficient for power, coefficient in enumerate(reversed(polynomial_coefficients))),
    )

    roots = sorted(np.roots(polynomial_coefficients))

    a = []
    for i in range(n):  # noqa: WPS440
        a.append(list(map(lambda x: operator.pow(x, i), roots)))

    coefficients = np.linalg.solve(a, moments[:n])

    if StateVar.SHOW_COMPUTATIONS.get():
        df = pd.DataFrame(data={'Моменты': moments})
        styler = df.style
        styler.format(precision=StateVar.PRECISION.get())
        st.dataframe(styler)

        st.markdown(fr'Ортогональный многочлен $\omega_n(x) = {latex(polynomial)}$')

        left_column, right_column = st.columns(2)

        with left_column:
            st.markdown('<h5> КФ с весом </h5>', unsafe_allow_html=True)
            df = pd.DataFrame(data={'Корни': roots, 'Коэффициенты': coefficients})
            styler = df.style
            styler.format(precision=StateVar.PRECISION.get())
            st.dataframe(styler)
            st.plotly_chart(
                plot_on_horizontal_axis(
                    df,
                    'Корни',
                    [
                        StateVar.LEFT_BOUNDARY.get(),
                        StateVar.RIGHT_BOUNDARY.get(),
                        (StateVar.LEFT_BOUNDARY.get() + StateVar.RIGHT_BOUNDARY.get()) / 2,
                    ],
                ),
                use_container_width=True,
            )

        with right_column:
            st.markdown('<h5> Составная КФ </h5>', unsafe_allow_html=True)
            segment = LineSegment(-1, 1)
            df = pd.DataFrame(
                data={'Корни': get_gaussian_roots(n, segment), 'Коэффициенты': get_gaussian_coefficients(n, segment)},
            )
            styler = df.style
            styler.format(precision=StateVar.PRECISION.get())
            st.dataframe(styler)
            st.plotly_chart(
                plot_on_horizontal_axis(df, 'Корни', [segment.left, segment.right, segment.midpoint]),
                use_container_width=True,
            )

    return sum(coefficient * f(root) for coefficient, root in zip(coefficients, roots))


def composite_gaussian_method(n: int, rho_f_expr) -> float:
    f = lambdify('x', rho_f_expr)

    line_segment = LineSegment(StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get())
    method = GaussianMethod()

    return sum(
        method.integrate(f=f, segment=segment, n=n) for segment in line_segment.split_into_segments(StateVar.M.get())
    )


def show_results(n: int) -> None:
    rho_f_expr = parse_expr(f'({StateVar.WEIGHT.get()}) * ({StateVar.FUNCTION.get()})', transformations=TRANSFORMATIONS)
    precise = float(integrate(rho_f_expr, ('x', StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get())))

    actual_weight = gaussian_method_with_weight(n)
    actual_composition = composite_gaussian_method(n, rho_f_expr)

    if StateVar.SHOW_PRECISE_SOLUTION.get():
        st.markdown(f'$I = {precise}$')

    left_column, right_column = st.columns(2)

    with left_column:
        st.markdown(fr'$I_\text{{вес}} = {actual_weight}$')
        st.markdown(fr'$I_\text{{скф}} = {actual_composition}$')

    with right_column:
        if StateVar.SHOW_PRECISE_SOLUTION.get():
            st.markdown(fr'$|I_\text{{вес}} - I| = {abs(actual_weight - precise)}$')
            st.markdown(fr'$|I_\text{{скф}} - I| = {abs(actual_composition - precise)}$')


def main():
    show_sidebar()

    st.markdown(
        """
        <h1 style='text-align: center'>
            Приближённое вычисление интегралов при помощи КФ НАСТ
        </h1>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='text-align: right'>Вариант 1</div>", unsafe_allow_html=True)

    nodes = st.multiselect('Количество узлов:', options=range(1, StateVar.MAX_NUMBER_OF_NODES.get() + 1))
    for number_of_nodes in sorted(nodes):
        st.subheader(f'Узлов: {number_of_nodes}')
        show_results(number_of_nodes)


if __name__ == '__main__':
    st.set_page_config(layout='wide')
    main()
