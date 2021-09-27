from sympy.parsing.sympy_parser import (
    convert_xor,
    function_exponentiation,
    implicit_application,
    implicit_multiplication,
    split_symbols,
    standard_transformations,
)

OUTPUT_PRECISION = 10

TRANSFORMATIONS = standard_transformations + (
    split_symbols,
    implicit_application,
    implicit_multiplication,
    function_exponentiation,
    convert_xor,
)

MAIN_COLOR = '#FF2B68'
SECOND_COLOR = '#5E5698'
LIGHT_GRAY = '#d3d3d3'
