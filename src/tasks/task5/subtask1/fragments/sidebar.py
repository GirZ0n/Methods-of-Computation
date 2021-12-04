import streamlit as st

from src.tasks.task5.subtask1.common.state_var import StateVar


def show_sidebar():
    with st.sidebar:
        st.title('Параметры задачи')

        function = st.text_input('f(x):', value='sin(x) / x')
        StateVar.FUNCTION.set(function)

        a = st.number_input('A:', value=float(0))
        StateVar.LEFT_BOUNDARY.set(a)

        b = st.number_input('B:', value=float(2))
        StateVar.RIGHT_BOUNDARY.set(b)

        with st.expander('Дополнительные параметры:'):
            precision = int(st.number_input('Точность вывода:', value=12))
            StateVar.PRECISION.set(precision)

            show_table = st.checkbox('Показывать таблицу', value=True)
            StateVar.SHOW_TABLE.set(show_table)

            show_precise_solution = st.checkbox('Показывать точное решение', value=True)
            StateVar.SHOW_PRECISE_SOLUTION.set(show_precise_solution)
