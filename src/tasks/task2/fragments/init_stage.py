import pandas as pd
import streamlit as st
from sympy import parse_expr

from src.common.consts import TRANSFORMATIONS
from src.common.methods.table_of_values_generators.equidistant_generator import EquidistantTableOfValuesGenerator
from src.common.methods.table_of_values_generators.random_generator import RandomTableOfValuesGenerator
from src.common.model.line_segment import LineSegment
from src.common.utils import plot_on_horizontal_axis
from src.tasks.task2.common.state_var import StateVar

GENERATORS_MAP = {
    'Случайные узлы': RandomTableOfValuesGenerator,
    'Равноотстоящие узлы': EquidistantTableOfValuesGenerator,
}


def _get_interpolation_table(
    table: pd.DataFrame,
    *,
    x: float,
    polynomial_degree: int,
    column: str = 'x',
) -> pd.DataFrame:
    return table.sort_values(by=[column], key=lambda current_node: abs(current_node - x))[: polynomial_degree + 1]


def show_init_stage() -> pd.DataFrame:
    st.header('Подготовительный этап')

    generator_name = st.selectbox('Выберите метод генерации узлов:', options=GENERATORS_MAP.keys(), index=1)
    generator_class = GENERATORS_MAP[generator_name]

    if issubclass(generator_class, RandomTableOfValuesGenerator):
        generator = generator_class(StateVar.RANDOM_STATE.get())
    else:
        generator = generator_class()

    table = generator.generate_table(
        expression=parse_expr(StateVar.TEXT_EXPRESSION.get(), transformations=TRANSFORMATIONS),
        line_segment=LineSegment(StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get()),
        number_of_points=StateVar.NUMBER_OF_POINTS.get(),
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

    return table.drop(columns=['abs'])
