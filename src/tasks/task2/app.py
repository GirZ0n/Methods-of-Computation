import sys

sys.path.append('')
sys.path.append('../../..')

from src.common.methods.interpolators.newton_interpolator import NewtonInterpolator
from src.common.methods.interpolators.lagrange_interpolator import LagrangeInterpolator
from src.tasks.task2.fragments.interpolation import show_interpolation_results
from src.tasks.task2.fragments.sidebar import show_sidebar
from src.tasks.task2.fragments.init_stage import show_init_stage

import streamlit as st


def main():
    st.set_page_config(layout='wide')

    st.markdown(
        """
        <h1 style='text-align: center'>
            Задача алгебраического интерполирования <br/><br/>
            Интерполяционный многочлен в форме Ньютона и в форме Лагранжа
        </h1>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='text-align: right'>Вариант 1</div>", unsafe_allow_html=True)

    show_sidebar()
    table = show_init_stage()
    show_interpolation_results(
        interpolator_class=LagrangeInterpolator,
        table=table,
        interpolator_name='Интерполяция Лагранжа',
        interpolator_symbol='L',
    )
    show_interpolation_results(
        interpolator_class=NewtonInterpolator,
        table=table,
        interpolator_name='Интерполяция Ньютона',
        interpolator_symbol='N',
    )


if __name__ == '__main__':
    main()
