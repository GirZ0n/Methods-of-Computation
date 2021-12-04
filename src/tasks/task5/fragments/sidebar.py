import streamlit as st

from src.tasks.task5.common.state_var import StateVar


def show_sidebar():
    with st.sidebar:
        st.title('Параметры задачи')

        method_name = st.selectbox('Метод:', options=['Гаусса', 'Мелера'])
        StateVar.METHOD_NAME.set(method_name)

        default_function = 'sin(x) / x'
        if method_name != 'Гаусса':
            default_function = 'cos(x)'

        function = st.text_input('f(x):', value=default_function)
        StateVar.FUNCTION.set(function)

        if method_name == 'Гаусса':
            a = st.number_input('A:', value=float(0))
            StateVar.LEFT_BOUNDARY.set(a)
        else:
            st.write('$A = -1$')
            StateVar.LEFT_BOUNDARY.set(-1)

        if method_name == 'Гаусса':
            b = st.number_input('B:', value=float(2))
            StateVar.RIGHT_BOUNDARY.set(b)
        else:
            st.write('$B = 1$')
            StateVar.RIGHT_BOUNDARY.set(1)

        with st.expander('Дополнительные параметры:'):
            precision = int(st.number_input('Точность вывода:', value=12))
            StateVar.PRECISION.set(precision)

            max_number_of_nodes = int(st.number_input('Максимальное количество узлов:', value=8))
            StateVar.MAX_NUMBER_OF_NODES.set(max_number_of_nodes)

            show_table = st.checkbox('Показывать таблицу', value=True)
            StateVar.SHOW_TABLE.set(show_table)

            show_precise_solution = st.checkbox('Показывать точное решение', value=True)
            StateVar.SHOW_PRECISE_SOLUTION.set(show_precise_solution)
