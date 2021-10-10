import sys

import streamlit as st

sys.path.append('')
sys.path.append('../../../..')

from src.tasks.task3.subtask1.fragments.axis_rotation_method import show_axis_rotation_method
from src.tasks.task3.subtask1.fragments.nonlinear_equation_method import show_nonlinear_equation_method
from src.tasks.task3.subtask1.fragments.sidebar import show_sidebar
from src.tasks.task3.subtask1.fragments.init_stage import show_init_stage

METHODS_MAP = {
    'Смена осей': show_axis_rotation_method,
    'Нелинейное уравнения': show_nonlinear_equation_method,
}


def main():
    st.set_page_config(layout='wide')

    st.markdown(
        """
        <h1 style='text-align: center'>
            Задача обратного интерполирования
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='text-align: right'>Вариант 1</div>", unsafe_allow_html=True)

    show_sidebar()
    table = show_init_stage()

    method_names = st.multiselect('Выберите методы:', options=METHODS_MAP.keys())
    for method_name in method_names:
        METHODS_MAP[method_name](table)


if __name__ == '__main__':
    main()
