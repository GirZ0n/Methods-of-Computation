import pandas as pd
import streamlit as st
from sympy import lambdify, parse_expr

from src.common.consts import TRANSFORMATIONS
from src.common.methods.table_of_values_generators.equidistant_generator import EquidistantTableOfValuesGenerator
from src.common.methods.table_of_values_generators.random_generator import RandomTableOfValuesGenerator
from src.common.model.line_segment import LineSegment
from src.common.utils import plot_on_horizontal_axis
from src.tasks.task3.subtask1.common.state_var import StateVar

GENERATORS_MAP = {
    'Случайные узлы': RandomTableOfValuesGenerator,
    'Равноотстоящие узлы': EquidistantTableOfValuesGenerator,
}


def show_init_stage() -> pd.DataFrame:
    st.header('Подготовительный этап')

    generator_name = st.selectbox('Выберите метод генерации узлов:', options=GENERATORS_MAP.keys(), index=1)
    generator_class = GENERATORS_MAP[generator_name]

    if issubclass(generator_class, RandomTableOfValuesGenerator):
        generator = generator_class(StateVar.RANDOM_STATE.get())
    else:
        generator = generator_class()

    f = lambdify('x', parse_expr(StateVar.TEXT_EXPRESSION.get(), transformations=TRANSFORMATIONS))

    table = generator.generate_table(
        f=f,
        line_segment=LineSegment(StateVar.LEFT_BOUNDARY.get(), StateVar.RIGHT_BOUNDARY.get()),
        number_of_points=StateVar.NUMBER_OF_POINTS.get(),
    )

    st.subheader('Узлы')

    st.plotly_chart(
        plot_on_horizontal_axis(table, 'y', extra_points=[StateVar.INTERPOLATION_POINT.get()]),
        use_container_width=True,
    )

    st.dataframe(table.sort_values(by=['y']).reset_index(drop=True).T)

    return table
