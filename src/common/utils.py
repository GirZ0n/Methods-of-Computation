import random
from typing import List, Optional

import pandas as pd
import plotly.graph_objects as go

from src.common.consts import COLOR


def sample_floats(low: float, high: float, k: int = 1) -> List[float]:
    """Return a k-length list of unique random floats in the range of low <= x <= high."""
    seen = set()
    for _ in range(k):
        x = random.uniform(low, high)
        while x in seen:
            x = random.uniform(low, high)
        seen.add(x)

    return list(seen)


def plot_on_horizontal_axis(df: pd.DataFrame, column: str, extra_points: Optional[List[float]] = None) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(height=100, plot_bgcolor='white', showlegend=False, margin={'t': 0, 'b': 0, 'l': 0, 'r': 0})
    fig.update_xaxes(title=None)
    fig.update_yaxes(zeroline=True, showticklabels=False, zerolinecolor=COLOR.LIGHT_GRAY, title=None)

    fig.add_scatter(x=df[column], y=[0 for _ in range(len(df))], mode='markers', marker_color=COLOR.STREAMLIT_BLUE)

    if extra_points is not None:
        fig.add_scatter(x=extra_points, y=[0 for _ in range(len(df))], mode='markers', marker_color=COLOR.STREAMLIT)

    return fig
