import sys
from typing import Callable, List

import pandas as pd
import streamlit as st
from sympy import integrate, lambdify, parse_expr

sys.path.append('')
sys.path.append('../../..')

from src.common.utils import plot_on_horizontal_axis
from src.common.consts import TRANSFORMATIONS
from src.common.methods.numerical_integration.gaussian_method import (
    GaussianMethod,
    get_gaussian_coefficients,
    get_gaussian_roots,
)
from src.common.methods.numerical_integration.mohler_method import (
    MohlerMethod,
    get_mohler_coefficients,
    get_mohler_roots,
)
from src.common.model.line_segment import LineSegment
from src.common.model.numerical_integrator import NumericalIntegrator
from src.tasks.task5.common.state_var import StateVar
from src.tasks.task5.fragments.sidebar import show_sidebar


_AXIS_THRESHOLD = 4


def _show_results(
    f: Callable,
    precise_solution: float,
    number_of_nodes: int,
    roots: List[float],
    coefficients: List[float],
    method: NumericalIntegrator,
) -> None:
    st.subheader(f'Узлов: {number_of_nodes}')

    segment = LineSegment(StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get())

    if StateVar.SHOW_TABLE.get():
        left_column, right_column = st.columns(2)

        df = pd.DataFrame({'Корни': roots, 'Коэффициенты': coefficients})

        with left_column:
            precision = StateVar.PRECISION.get()

            styler = df.style
            styler.format(precision=precision)

            st.dataframe(styler)

        with right_column:
            st.latex(fr'\sum\limits_{{k = 0}}^{{{number_of_nodes - 1}}} a_k = {sum(coefficients)}')
            if number_of_nodes > _AXIS_THRESHOLD:
                st.plotly_chart(
                    plot_on_horizontal_axis(df, 'Корни', [segment.left, segment.right, segment.midpoint]),
                    use_container_width=True,
                )

        if number_of_nodes <= _AXIS_THRESHOLD:
            st.plotly_chart(
                plot_on_horizontal_axis(df, 'Корни', [segment.left, segment.right, segment.midpoint]),
                use_container_width=True,
            )

    approximate_solution = method.integrate(f=f, segment=segment, n=number_of_nodes)

    precise_container = st.empty()
    st.markdown(f'$I_{{прибл.}} = {approximate_solution}$')
    error_container = st.empty()

    if StateVar.SHOW_PRECISE_SOLUTION.get():
        precise_container.markdown(f'$I_{{точн.}} = {precise_solution}$')
        error_container.markdown(
            fr'$\left| I_{{точн.}} - I_{{прибл.}} \right| = {abs(precise_solution - approximate_solution)}$',
        )


def show_gaussian_method() -> None:
    nodes = st.multiselect(
        'Количество узлов:',
        options=range(1, StateVar.MAX_NUMBER_OF_NODES.get() + 1),
    )

    segment = LineSegment(StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get())

    f_expression = parse_expr(StateVar.FUNCTION.get(), transformations=TRANSFORMATIONS)
    f = lambdify('x', f_expression)

    precise_solution = float(
        integrate(f_expression, ('x', StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get())),
    )

    method = GaussianMethod()
    for number_of_nodes in sorted(nodes):
        roots = get_gaussian_roots(number_of_nodes, segment)
        coefficients = get_gaussian_coefficients(number_of_nodes, segment)
        _show_results(f, precise_solution, number_of_nodes, roots, coefficients, method)


def show_mohler_method() -> None:
    nodes = st.multiselect(
        'Количество узлов:',
        options=range(1, StateVar.MAX_NUMBER_OF_NODES.get() + 1),
    )

    f_expression = parse_expr(StateVar.FUNCTION.get(), transformations=TRANSFORMATIONS)
    f = lambdify('x', f_expression)

    f_expression_with_weight = parse_expr(
        f'({StateVar.FUNCTION.get()}) / sqrt(1 - x^2)',
        transformations=TRANSFORMATIONS,
    )
    precise_solution = float(
        integrate(f_expression_with_weight, ('x', StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get())),
    )

    method = MohlerMethod()
    for number_of_nodes in sorted(nodes):
        roots = get_mohler_roots(number_of_nodes)
        coefficients = get_mohler_coefficients(number_of_nodes)
        _show_results(f, precise_solution, number_of_nodes, roots, coefficients, method)


def main() -> None:
    show_sidebar()

    st.markdown(
        f"""
        <h1 style='text-align: center'>
            Вычисление интегралов при помощи КФ {StateVar.METHOD_NAME.get()}.
        </h1>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='text-align: right'>Вариант 1</div>", unsafe_allow_html=True)

    if StateVar.METHOD_NAME.get() == 'Гаусса':
        show_gaussian_method()
    else:
        show_mohler_method()


if __name__ == '__main__':
    st.set_page_config(layout='wide')
    main()
