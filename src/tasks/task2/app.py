import sys

sys.path.append('')
sys.path.append('../../..')

from src.tasks.task2.fragments.sidebar import show_sidebar

from src.tasks.task2.fragments.init_stage import show_init_stage

import streamlit as st


def main():
    st.set_page_config(layout='wide')

    st.markdown(
        """
        <h1 style='text-align: center'>
            Задача алгебраического интерполирования <br/><br/>
            Интерполяционный многочлен <br/>
            в форме Ньютона и в форме Лагранжа
        </h1>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='text-align: right'>Вариант 1</div>", unsafe_allow_html=True)

    show_sidebar()
    show_init_stage()


if __name__ == '__main__':
    main()
