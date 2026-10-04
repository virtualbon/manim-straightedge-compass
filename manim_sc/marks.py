"""Marked points used in straightedge-and-compass constructions."""

from __future__ import annotations

import numpy as np
from manim import Dot, Text, VGroup, DOWN

from .geometry import P


class MarkedPoint(VGroup):
    """A small dot with an optional text label.

    Parameters
    ----------
    position
        Location of the point (anything accepted by :func:`geometry.P`).
    label
        Optional label rendered with :class:`manim.Text` (no LaTeX required).
    label_buff
        Distance between the dot and the label.
    label_dir
        Direction in which the label is placed relative to the dot.
    """

    def __init__(
        self,
        position,
        label: str | None = None,
        *,
        radius: float = 0.045,
        color="#E84A5F",
        label_buff: float = 0.12,
        label_dir=DOWN,
        font_size: int = 26,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.pt: np.ndarray = P(position)
        self.dot = Dot(self.pt, radius=radius, color=color)
        self.add(self.dot)
        if label is not None:
            self.label = Text(label, font_size=font_size, color="#F5F5F5")
            self.label.next_to(self.dot, label_dir, buff=label_buff)
            self.add(self.label)
        else:
            self.label = None

    def get_position(self) -> np.ndarray:
        return self.pt

    # Allows ``np.asarray(marked_point)`` to yield the geometric location, so
    # Manim calls such as ``move_to(marked_point)`` work naturally.
    def __array__(self, dtype=None):
        return np.asarray(self.pt, dtype=dtype)
