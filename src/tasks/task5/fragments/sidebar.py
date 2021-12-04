import streamlit as st

from src.tasks.task5.common.state_var import StateVar


def show_sidebar():
    with st.sidebar:
        st.title('Параметры задачи')

        method_name = st.selectbox('Метод:', options=['Гаусса', 'Мелера'])
        StateVar.METHOD_NAME.set(method_name)

        if method_name == 'Гаусса':
            default_function = 'sin(x) / x'
            default_a = 0
            default_b = 2
        else:
            default_function = 'cos(x)'
            default_a = -1
            default_b = 1

        function = st.text_input('f(x):', value=default_function)
        StateVar.FUNCTION.set(function)

        a = st.number_input('A:', value=float(default_a))
        StateVar.LEFT_BOUNDARY.set(a)

        b = st.number_input('B:', value=float(default_b))
        StateVar.RIGHT_BOUNDARY.set(b)

        with st.expander('Дополнительные параметры:'):
            precision = int(st.number_input('Точность вывода:', value=12))
            StateVar.PRECISION.set(precision)

            max_number_of_nodes = int(st.number_input('Максимальное количество узлов:', value=8))
            StateVar.MAX_NUMBER_OF_NODES.set(max_number_of_nodes)

            show_table = st.checkbox('Показывать таблицу', value=True)
            StateVar.SHOW_TABLE.set(show_table)

            show_precise_solution = st.checkbox('Показывать точное решение', value=True)
            StateVar.SHOW_PRECISE_SOLUTION.set(show_precise_solution)
