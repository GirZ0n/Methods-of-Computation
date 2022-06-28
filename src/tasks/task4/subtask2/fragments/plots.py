from typing import Callable, List, Literal

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from src.common.config import PLOT_STEP
from src.common.consts import COLOR
from src.common.model.line_segment import LineSegment


def _plot_function(f: Callable, segment: LineSegment) -> go.Figure:
    x_main = np.linspace(segment.left, segment.right, int(segment.length // PLOT_STEP))
    y_main = f(x_main)

    h = (segment.right - segment.left) / 4

    x_left = np.linspace(segment.left - h, segment.left, int(h // PLOT_STEP))
    y_left = f(x_left)

    x_right = np.linspace(segment.right, segment.right + h, int(h // PLOT_STEP))
    y_right = f(x_right)

    fig = go.Figure()
    fig.add_scatter(
        x=x_main,
        y=y_main,
        legendgroup='function',
        name='Исходная функция',
        fill='tozeroy',
        marker_color=COLOR.DARK_GRAY.value,
    )
    fig.add_scatter(
        x=x_left,
        y=y_left,
        legendgroup='function',
        name='Исходная функция',
        marker_color=COLOR.DARK_GRAY.value,
        showlegend=False,
    )
    fig.add_scatter(
        x=x_right,
        y=y_right,
        legendgroup='function',
        name='Исходная функция',
        marker_color=COLOR.DARK_GRAY.value,
        showlegend=False,
    )

    fig.update_xaxes(
        range=[
            min(x_left),
            max(x_right),
        ],
    )

    fig.update_yaxes(
        range=[
            min(min(np.concatenate((y_left, y_main, y_right), axis=None)), 0) - 1,
            max(max(np.concatenate((y_left, y_main, y_right), axis=None)), 0) + 1,
        ],
    )

    return fig


def _plot_points(fig: go.Figure, f: Callable, x: List[float]) -> None:
    fig.add_scatter(
        x=x,
        y=list(map(f, x)),
        mode='markers',
        legendgroup='area',
        hovertemplate='(%{x}, %{y})<extra></extra>',
        showlegend=False,
        marker_color=COLOR.STREAMLIT.value,
    )


def show_polygon(  # noqa: WPS231
    f: Callable,
    segments: List[LineSegment],
    method_type: Literal['left', 'right', 'center', 'trapezoid'],
) -> None:
    min_x = min(segment.left for segment in segments)
    max_x = max(segment.right for segment in segments)

    fig = _plot_function(f, LineSegment(min_x, max_x))

    for index, segment in enumerate(segments):
        if method_type == 'left':
            y_left = f(segment.left)
            y_right = f(segment.left)
        elif method_type == 'right':
            y_left = f(segment.right)
            y_right = f(segment.right)
        elif method_type == 'trapezoid':
            y_left = f(segment.left)
            y_right = f(segment.right)
        else:
            y_left = f(segment.midpoint)
            y_right = f(segment.midpoint)

        x_points = [segment.left, segment.left, segment.right, segment.right]
        y_points = [0, y_left, y_right, 0]
        fig.add_scatter(
            x=x_points,
            y=y_points,
            legendgroup='area',
            name='Приближение',
            fill='toself',
            mode='lines',
            hoverinfo='none',
            showlegend=(index == 0),
            marker_color=COLOR.STREAMLIT_BLUE.value,
        )

    if method_type == 'left':
        points = list(map(lambda s: s.left, segments))
    elif method_type == 'right':
        points = list(map(lambda s: s.right, segments))
    elif method_type == 'trapezoid':
        points = list(map(lambda s: s.left, segments))
        points += list(map(lambda s: s.right, segments))
    else:
        points = list(map(lambda s: s.midpoint, segments))

    _plot_points(fig, f, points)

    fig.update_layout(template='none', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    st.plotly_chart(fig, use_container_width=True)


def show_quadratic_simpson(f: Callable, segments: List[LineSegment]) -> None:
    min_x = min(segment.left for segment in segments)
    max_x = max(segment.right for segment in segments)

    fig = _plot_function(f, LineSegment(min_x, max_x))

    points = []
    for segment in segments:
        points.extend([segment.left, segment.midpoint, segment.right])

    for index, (left, middle, right) in enumerate(zip(points[::3], points[1::3], points[2::3])):
        z = np.polyfit([left, middle, right], [f(left), f(middle), f(right)], 2)
        parabola = np.poly1d(z)
        x = np.linspace(left, right, int((right - left) // PLOT_STEP))
        fig.add_scatter(
            x=x,
            y=parabola(x),
            legendgroup='area',
            marker_color=COLOR.STREAMLIT_BLUE.value,
            fill='tozeroy',
            mode='lines',
            showlegend=(index == 0),
            name='Приближение',
        )
        fig.add_scatter(
            x=[left, left],
            y=[0, f(left)],
            legendgroup='area',
            marker_color=COLOR.STREAMLIT_BLUE.value,
            mode='lines',
            showlegend=False,
            hoverinfo='skip',
        )
        fig.add_scatter(
            x=[right, right],
            y=[0, f(right)],
            legendgroup='area',
            marker_color=COLOR.STREAMLIT_BLUE.value,
            mode='lines',
            showlegend=False,
            hoverinfo='skip',
        )

    _plot_points(fig, f, points)

    fig.update_layout(template='none', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    st.plotly_chart(fig, use_container_width=True)


def show_cubic_simpson(f: Callable, segments: List[LineSegment]) -> None:
    min_x = min(segment.left for segment in segments)
    max_x = max(segment.right for segment in segments)

    fig = _plot_function(f, LineSegment(min_x, max_x))

    points = []
    for segment in segments:
        points.extend(
            [segment.left, segment.left + segment.length / 3, segment.right - segment.length / 3, segment.right],
        )

    for index, (left, middle_left, middle_right, right) in enumerate(  # noqa: WPS352
        zip(points[::4], points[1::4], points[2::4], points[3::4]),
    ):
        z = np.polyfit(
            x=[left, middle_left, middle_right, right],
            y=[f(left), f(middle_left), f(middle_right), f(right)],
            deg=3,
        )
        cubic_parabola = np.poly1d(z)
        x = np.linspace(left, right, int((right - left) // PLOT_STEP))
        fig.add_scatter(
            x=x,
            y=cubic_parabola(x),
            legendgroup='area',
            marker_color=COLOR.STREAMLIT_BLUE.value,
            fill='tozeroy',
            mode='lines',
            showlegend=(index == 0),
            name='Приближение',
        )
        fig.add_scatter(
            x=[left, left],
            y=[0, f(left)],
            legendgroup='area',
            marker_color=COLOR.STREAMLIT_BLUE.value,
            mode='lines',
            showlegend=False,
            hoverinfo='skip',
        )
        fig.add_scatter(
            x=[right, right],
            y=[0, f(right)],
            legendgroup='area',
            marker_color=COLOR.STREAMLIT_BLUE.value,
            mode='lines',
            showlegend=False,
            hoverinfo='skip',
        )

    _plot_points(fig, f, points)

    fig.update_layout(template='none', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    st.plotly_chart(fig, use_container_width=True)
