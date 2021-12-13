import streamlit as st

from src.tasks.task6.common.state_var import StateVar


def show_sidebar():
    with st.sidebar:
        st.title('Параметры задачи')

        function = st.text_input('f(x):', value='sin(x)')
        StateVar.FUNCTION.set(function)

        weight = st.text_input('ρ(x):', value='sqrt(x)')
        StateVar.WEIGHT.set(weight)

        a = st.number_input('A:', value=float(0))
        StateVar.LEFT_BOUNDARY.set(a)

        b = st.number_input('B:', value=float(1))
        StateVar.RIGHT_BOUNDARY.set(b)

        m = int(st.number_input('m:', value=10, help='Число промежутков деления'))
        StateVar.M.set(m)

        with st.expander('Дополнительные параметры:'):
            precision = int(st.number_input('Точность вывода:', value=12))
            StateVar.PRECISION.set(precision)

            max_number_of_nodes = int(st.number_input('Максимальное количество узлов:', value=8))
            StateVar.MAX_NUMBER_OF_NODES.set(max_number_of_nodes)

            show_computations = st.checkbox('Показывать вычисления', value=True)
            StateVar.SHOW_COMPUTATIONS.set(show_computations)

            show_precise_solution = st.checkbox('Показывать точное решение', value=True)
            StateVar.SHOW_PRECISE_SOLUTION.set(show_precise_solution)
