import sys

import streamlit as st

sys.path.append('')
sys.path.append('../../../..')

from src.tasks.task3.subtask2.fragments.init_stage import show_init_stage
from src.tasks.task3.subtask2.fragments.results import show_results
from src.tasks.task3.subtask2.fragments.sidebar import show_sidebar


def main():
    st.set_page_config(layout='wide')

    st.markdown(
        """
        <h1 style='text-align: center'>
            Нахождение производных таблично-заданной функции по формулам численного дифференцирования
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='text-align: right'>Вариант 1</div>", unsafe_allow_html=True)

    show_sidebar()
    table = show_init_stage()
    show_results(table)


if __name__ == '__main__':
    main()
