from enum import Enum

from sympy.parsing.sympy_parser import (
    convert_xor,
    function_exponentiation,
    implicit_application,
    implicit_multiplication,
    split_symbols,
    standard_transformations,
)

TRANSFORMATIONS = standard_transformations + (
    split_symbols,
    implicit_application,
    implicit_multiplication,
    function_exponentiation,
    convert_xor,
)


class COLOR(Enum):
    STREAMLIT = '#FF2B68'
    STREAMLIT_BLUE = '#5E5698'
    LIGHT_GRAY = '#d3d3d3'
