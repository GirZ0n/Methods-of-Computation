from typing import Callable

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sympy import diff, lambdify, parse_expr

from src.common.consts import COLOR, TRANSFORMATIONS
from src.common.methods.numerical_differentiation.first_derivative_finder import FirstDerivativeFinder
from src.common.methods.numerical_differentiation.second_derivative_finder import SecondDerivativeFinder
from src.tasks.task3.subtask2.common.state_var import StateVar


def _table_to_latex(table: pd.DataFrame, precision: int, na_rep: str = 'nan') -> str:
    styler = table.style
    styler.format(
        {
            r"|f'(x_i)_\text{Т} - f'(x_i)_\text{ЧД}|": '{:e}',  # noqa: P103
            r"|f''(x_i)_\text{Т} - f''(x_i)_\text{ЧД}|": '{:e}',  # noqa: P103
        },
        precision=precision,
        na_rep=na_rep,
    )
    return styler.to_latex(column_format='c' * len(table.columns), hrules=True)


def _latex_to_katex(latex_str: str) -> str:
    katex_str = r'\def\arraystretch{1.3}' + latex_str  # noqa: WPS336
    katex_str = katex_str.replace('tabular', 'array')
    katex_str = katex_str.replace('toprule', 'hline')
    katex_str = katex_str.replace('midrule', 'hline')
    katex_str = katex_str.replace('bottomrule', 'hline')
    return katex_str  # noqa: WPS331


def _show_plot(f: Callable, x: pd.Series, y: pd.Series, title: str = ''):
    fig = go.Figure()

    x_range = np.arange(
        start=min(x),
        stop=max(x) + StateVar.STEP.get() / 100,
        step=StateVar.STEP.get() / 100,
    )

    fig.add_scatter(x=x_range, y=f(x_range), name='Производная', marker_color=COLOR.DARK_GRAY.value)
    fig.add_scatter(x=x, y=y, mode='markers', name='Найденные значения производной', marker_color=COLOR.STREAMLIT.value)

    fig.update_layout(
        title_text=title,
        title_x=0.5,
        legend={'orientation': 'h', 'yanchor': 'top', 'xanchor': 'center', 'y': -0.1, 'x': 0.5},
    )

    st.plotly_chart(fig, use_container_width=True)


def show_results(table: pd.DataFrame):
    st.header('Результаты')

    f_expr = parse_expr(StateVar.TEXT_EXPRESSION.get(), transformations=TRANSFORMATIONS)
    df = lambdify('x', diff(f_expr))

    first_derivative_finder = FirstDerivativeFinder()
    first_derivatives = first_derivative_finder.calculate_derivatives_table(
        function_values=table['y'],
        step=StateVar.STEP.get(),
    )

    table[r"f'(x_i)_\text{ЧД}"] = first_derivatives
    table[r"|f'(x_i)_\text{Т} - f'(x_i)_\text{ЧД}|"] = abs(first_derivatives - df(table['x']))

    ddf = lambdify('x', diff(diff(f_expr)))

    second_derivative_finder = SecondDerivativeFinder()
    second_derivatives = second_derivative_finder.calculate_derivatives_table(
        function_values=table['y'],
        step=StateVar.STEP.get(),
    )

    table[r"f''(x_i)_\text{ЧД}"] = second_derivatives
    table[r"|f''(x_i)_\text{Т} - f''(x_i)_\text{ЧД}|"] = abs(second_derivatives - ddf(table['x']))

    table.columns.name = 'i'
    table.rename(columns={'x': 'x_i', 'y': 'f(x_i)'}, inplace=True)

    latex_str = _table_to_latex(table, StateVar.PRECISION.get(), r'\text{\textemdash}')
    st.latex(_latex_to_katex(latex_str))

    left_column, right_column = st.columns(2)

    with left_column:
        _show_plot(df, table['x_i'], first_derivatives, 'Первая производная')

    with right_column:
        _show_plot(ddf, table['x_i'], second_derivatives, 'Вторая производная')
