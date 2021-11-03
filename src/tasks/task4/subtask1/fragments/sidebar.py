import streamlit as st

from src.tasks.task4.subtask1.common.state_var import StateVar


def show_sidebar():
    with st.sidebar:
        st.title('Параметры задачи')

        text_expression = st.text_input('Выражение:', value='x^3 + x^2 + 1')
        StateVar.TEXT_EXPRESSION.set(text_expression)

        a = st.number_input('A:', value=float(1))
        StateVar.LEFT_BOUNDARY.set(a)

        b = st.number_input('B:', value=float(3))
        StateVar.RIGHT_BOUNDARY.set(b)

        n = int(st.number_input('Количество частей:', value=3, min_value=1))
        StateVar.NUMBER_OF_SEGMENTS.set(n)
