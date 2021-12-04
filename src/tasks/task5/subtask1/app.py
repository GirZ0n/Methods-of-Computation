import pandas as pd
import streamlit as st
from sympy import integrate, lambdify, parse_expr

from src.common.consts import TRANSFORMATIONS
from src.common.methods.numerical_integration.gaussian_method import GaussianMethod, get_coefficients, get_roots
from src.common.model.line_segment import LineSegment
from src.tasks.task5.subtask1.common.state_var import StateVar
from src.tasks.task5.subtask1.fragments.sidebar import show_sidebar

MAXIMUM_NUMBER_OF_NODES = 8


def _table_to_latex(table: pd.DataFrame, precision: int) -> str:
    styler = table.style
    styler.format(precision=precision)
    return styler.to_latex(column_format='c' * len(table.columns), hrules=True)


def _latex_to_katex(latex_str: str) -> str:
    katex_str = r'\def\arraystretch{1.3}' + latex_str  # noqa: WPS336
    katex_str = katex_str.replace('tabular', 'array')
    katex_str = katex_str.replace('toprule', 'hline')
    katex_str = katex_str.replace('midrule', 'hline')
    katex_str = katex_str.replace('bottomrule', 'hline')
    return katex_str  # noqa: WPS331


def _show_results(number_of_nodes: int) -> None:
    st.subheader(f'Узлов: {number_of_nodes}')

    segment = LineSegment(StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get())

    roots = get_roots(number_of_nodes, segment)
    coefficients = get_coefficients(number_of_nodes, segment)

    if StateVar.SHOW_TABLE.get():
        df = pd.DataFrame({'Корни': roots, 'Коэффициенты': coefficients})
        precision = StateVar.PRECISION.get()

        styler = df.style
        styler.format(precision=precision)

        st.dataframe(styler)

        st.write(fr'$\sum\limits_{{k = 0}}^{{{number_of_nodes - 1}}} a_k = {sum(coefficients)} = B - A$')

    f_expression = parse_expr(StateVar.FUNCTION.get(), transformations=TRANSFORMATIONS)
    f = lambdify('x', f_expression)
    precise_solution = float(
        integrate(f_expression, ('x', StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get())),
    )

    method = GaussianMethod()
    approximate_solution = method.integrate(
        f=f,
        segment=LineSegment(StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get()),
        n=number_of_nodes,
    )

    precise_container = st.empty()
    st.markdown(f'$I_{{прибл.}} = {approximate_solution}$')
    error_container = st.empty()

    if StateVar.SHOW_PRECISE_SOLUTION.get():
        precise_container.markdown(f'$I_{{точн.}} = {precise_solution}$')
        error_container.markdown(
            fr'$\left| I_{{точн.}} - I_{{прибл.}} \right| = {abs(precise_solution - approximate_solution)}$',
        )


def main() -> None:
    st.markdown(
        """
        <h1 style='text-align: center'>
            КФ Гаусса, ее узлы и коэффициенты. </br>
            Вычисление интегралов при помощи КФ Гаусса
        </h1>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='text-align: right'>Вариант 1</div>", unsafe_allow_html=True)

    show_sidebar()

    nodes = st.multiselect('Количество узлов:', options=range(1, MAXIMUM_NUMBER_OF_NODES + 1), default=[2, 5, 6, 8])

    for number_of_nodes in nodes:
        _show_results(number_of_nodes)


if __name__ == '__main__':
    st.set_page_config(layout='wide')
    main()
