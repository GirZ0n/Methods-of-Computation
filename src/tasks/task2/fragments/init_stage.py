import pandas as pd
import streamlit as st
from sympy import parse_expr

from src.common.consts import TRANSFORMATIONS
from src.common.methods.nodes_generation.equidistant_nodes_generator import EquidistantNodesGenerator
from src.common.methods.nodes_generation.random_nodes_generator import RandomNodesGenerator
from src.common.model.line_segment import LineSegment
from src.common.utils import plot_on_horizontal_axis
from src.tasks.task2.common.state_var import StateVar

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
    generator_class = GENERATORS_MAP[generator_name]

    if issubclass(generator_class, RandomNodesGenerator):
        generator = generator_class(StateVar.RANDOM_STATE.get())
    else:
        generator = generator_class()

    table = generator.generate_table(
        expression=parse_expr(StateVar.TEXT_EXPRESSION.get(), transformations=TRANSFORMATIONS),
        line_segment=LineSegment(StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get()),
        number_of_nodes=StateVar.NUMBER_OF_NODES.get(),
    )

    st.subheader('Узлы')

    st.plotly_chart(
        plot_on_horizontal_axis(table, 'x', extra_points=[StateVar.INTERPOLATION_POINT.get()]),
        use_container_width=True,
    )
    st.dataframe(table.T)

    st.subheader('Узлы интерполяции')
    table = _get_interpolation_table(
        table,
        x=StateVar.INTERPOLATION_POINT.get(),
        polynomial_degree=StateVar.POLYNOMIAL_DEGREE.get(),
    )
    table['abs'] = abs(table['x'] - StateVar.INTERPOLATION_POINT.get())
    table.reset_index(inplace=True, drop=True)
    st.plotly_chart(
        plot_on_horizontal_axis(table, 'x', extra_points=[StateVar.INTERPOLATION_POINT.get()]),
        use_container_width=True,
    )
    st.dataframe(table.T)
