import streamlit as st

from src.tasks.task2.common.state_var import StateVar


def show_sidebar():
    with st.sidebar:
        st.header('Параметры задачи')

        text_expression = st.text_input('Выражение:', value='sin(x) - x^2 / 2')
        StateVar.TEXT_EXPRESSION.set(text_expression)

        left_column, right_column = st.columns(2)

        with left_column:
            a = int(st.number_input('A:', value=0))
            StateVar.LEFT_BOUNDARY.set(a)

            number_of_points = int(st.number_input('Количество узлов:', value=16, min_value=2))
            StateVar.NUMBER_OF_POINTS.set(number_of_points)

        with right_column:
            b = int(st.number_input('B:', value=1))
            StateVar.RIGHT_BOUNDARY.set(b)

            polynomial_degree = int(
                st.number_input(
                    'Степень многочлена:',
                    value=min(7, number_of_points - 1),
                    min_value=1,
                    max_value=number_of_points - 1,
                ),
            )
            StateVar.POLYNOMIAL_DEGREE.set(polynomial_degree)

        x = st.number_input('Введите точку интерполирования x:', value=0.65)
        StateVar.INTERPOLATION_POINT.set(x)

        with st.expander('Дополнительные параметры'):
            save_random_state = st.checkbox('Сохранить рандомное состояние')

            if not save_random_state:
                StateVar.RANDOM_STATE.set(StateVar.RANDOM_STATE.get(default=0) + 1)
