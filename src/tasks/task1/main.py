from typing import List

from sympy import diff, lambdify, parse_expr

from src.common.methods.root_finding.bisection_method import BisectionMethod
from src.common.methods.root_finding.newton_method import ModifiedNewtonMethod, NewtonMethod
from src.common.methods.root_finding.secant_method import SecantMethod
from src.common.methods.root_separation.segment_tabulation import Tabulator
from src.common.model.line_segment import LineSegment

LINE_SEGMENT = LineSegment(-5, 3)

F = parse_expr('x - 10 * sin(x)')

ACCURACY = 10 ** -6
N = 1000

METHOD_NAME_TO_ROOT_FINDER = {
    'Метод бисекции': BisectionMethod(),
    'Метод Ньютона': NewtonMethod(),
    'Модифицированный метод Ньютона': ModifiedNewtonMethod(),
    'Метод секущих': SecantMethod(),
}


def print_params():
    print(f'Line segment: {LINE_SEGMENT}\n')

    df = diff(F)
    print(f'f  = {F}')
    print(f'{df = }\n')

    print(f'ε = {ACCURACY}')
    print(f'{N = }\n')


def separate_roots() -> List[LineSegment]:
    tabulator = Tabulator(N)

    f = lambdify('x', F)
    segments = tabulator.separate(f=f, line_segment=LINE_SEGMENT)

    for index, segment in enumerate(segments):
        print(f'{index + 1}. {segment}')

    return segments


def print_header(text: str):
    print(f'\033[95m\033[1m{text}\033[0m')


def main():
    print_header('ЧИСЛЕННЫЕ МЕТОДЫ РЕШЕНИЯ НЕЛИНЕЙНЫХ УРАВНЕНИЙ\n')

    print_header('Исходные параметры:')
    print_params()

    print_header('Найденные отрезки:')
    segments = separate_roots()
    print(f'Всего найдено: {len(segments)}\n')

    for method_name, root_finder in METHOD_NAME_TO_ROOT_FINDER.items():
        print_header(method_name)

        f = lambdify('x', F)
        df = lambdify('x', diff(F))

        for segment in segments:
            root_finder.find(derivatives=[f, df], line_segment=segment, accuracy=ACCURACY)
            print(root_finder.stats, '\n')


if __name__ == '__main__':
    main()
