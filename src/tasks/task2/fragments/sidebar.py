import streamlit as st


def show_sidebar():
    with st.sidebar:
        st.header('Параметры задачи')

        text_expression = st.text_input('Выражение:', value='sin(x) - x^2 / 2')
        st.session_state.text_expression = text_expression

        left_column, right_column = st.columns(2)

        with left_column:
            a = int(st.number_input('A:', value=0))
            st.session_state.left_boundary = a

            number_of_nodes = int(st.number_input('Количество узлов:', value=15))
            st.session_state.number_of_nodes = number_of_nodes

        with right_column:
            b = int(st.number_input('B:', value=1, min_value=1))
            st.session_state.right_boundary = b

            polynomial_degree = int(
                st.number_input(
                    'Степень многочлена:',
                    value=min(7, number_of_nodes - 1),
                    min_value=0,
                    max_value=number_of_nodes - 1,
                ),
            )
            st.session_state.polynomial_degree = polynomial_degree

        x = st.number_input('Введите точку интерполирования x:', value=0.65)
        st.session_state.x = x
