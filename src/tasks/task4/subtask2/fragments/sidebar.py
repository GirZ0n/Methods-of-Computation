import streamlit as st

from src.tasks.task4.subtask2.common.state_var import StateVar


def show_sidebar():
    with st.sidebar:
        st.title('Параметры задачи')

        function = st.text_input('f(x):', value='x^3 + x^2 + 1')
        StateVar.FUNCTION.set(function)

        a = st.number_input('A:', value=float(1))
        StateVar.LEFT_BOUNDARY.set(a)

        b = st.number_input('B:', value=float(3))
        StateVar.RIGHT_BOUNDARY.set(b)

        n = int(st.number_input('Количество частей:', value=3, min_value=1))
        StateVar.NUMBER_OF_SEGMENTS.set(n)
