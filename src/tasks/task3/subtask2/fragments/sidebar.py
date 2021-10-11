import streamlit as st

from src.tasks.task3.subtask2.common.state_var import StateVar


def show_sidebar():
    with st.sidebar:
        text_expression = st.text_input('Выражение:', value='exp(3x)')
        StateVar.TEXT_EXPRESSION.set(text_expression)

        left_boundary = st.number_input('Начало отрезка:', value=0)
        StateVar.LEFT_BOUNDARY.set(left_boundary)

        number_of_points = int(st.number_input('Количество значений:', value=8, min_value=3))
        StateVar.NUMBER_OF_POINTS.set(number_of_points)

        step = st.number_input('Шаг:', value=1e-4, step=1e-1, format='%e')
        StateVar.STEP.set(step)

        with st.expander('Дополнительные параметры'):
            precision = int(st.number_input('Точность вывода:', value=10, min_value=0))
            StateVar.PRECISION.set(precision)
