import pandas as pd
import streamlit as st
from sympy import parse_expr

from src.common.config import TRANSFORMATIONS
from src.common.methods.nodes_generation.equidistant_nodes_generator import EquidistantNodesGenerator
from src.common.methods.nodes_generation.random_nodes_generator import RandomNodesGenerator
from src.common.model.line_segment import LineSegment
from src.common.utils import plot_on_horizontal_axis

GENERATORS_MAP = {
    'Случайные узлы': RandomNodesGenerator,
    'Равноотстоящие узлы': EquidistantNodesGenerator,
}


def _get_interpolation_table(
    table: pd.DataFrame,
    *,
    x: float,
    polynomial_degree: int,
    column: str = 'x',
) -> pd.DataFrame:
    return table.sort_values(by=[column], key=lambda current_node: abs(current_node - x))[: polynomial_degree + 1]


def show_init_stage():
    st.header('Подготовительный этап')

    generator_name = st.selectbox('Выберите метод генерации узлов:', options=GENERATORS_MAP.keys(), index=1)
    generator = GENERATORS_MAP[generator_name]()

    table = generator.generate_table(
        expression=parse_expr(st.session_state.text_expression, transformations=TRANSFORMATIONS),
        line_segment=LineSegment(st.session_state.left_boundary, st.session_state.right_boundary),
        number_of_nodes=st.session_state.number_of_nodes,
    )

    st.subheader('Узлы')

    st.plotly_chart(plot_on_horizontal_axis(table, 'x', extra_points=[st.session_state.x]), use_container_width=True)
    st.dataframe(table.T)

    st.subheader('Узлы интерполяции')
    table = _get_interpolation_table(
        table,
        x=st.session_state.x,
        polynomial_degree=st.session_state.polynomial_degree,
    )
    table['abs'] = abs(table['x'] - st.session_state.x)
    table.reset_index(inplace=True, drop=True)
    st.plotly_chart(plot_on_horizontal_axis(table, 'x', extra_points=[st.session_state.x]), use_container_width=True)
    st.dataframe(table.T)
