import numpy as np
import pandas as pd
import streamlit as st
from sympy import lambdify, parse_expr

from src.common.consts import TRANSFORMATIONS
from src.tasks.task3.subtask2.common.state_var import StateVar


def _generate_table() -> pd.DataFrame:
    f = lambdify('x', parse_expr(StateVar.TEXT_EXPRESSION.get(), transformations=TRANSFORMATIONS))

    x = np.arange(
        start=StateVar.LEFT_BOUNDARY.get(),
        stop=StateVar.LEFT_BOUNDARY.get() + StateVar.NUMBER_OF_POINTS.get() * StateVar.STEP.get(),
        step=StateVar.STEP.get(),
    )

    return pd.DataFrame.from_dict({'x': x, 'y': f(x)})


def show_init_stage() -> pd.DataFrame:
    st.header('Подготовительный этап')
    table = _generate_table()

    st.dataframe(table.style.format(precision=StateVar.PRECISION.get()))

    return table
