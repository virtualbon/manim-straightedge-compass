"""The physical tools: a straightedge (ruler) and a compass."""

from __future__ import annotations

import numpy as np
from manim import (
    Arc,
    Circle,
    Dot,
    Line,
    Rectangle,
    VGroup,
    DEGREES,
    RIGHT,
    LEFT,
    UP,
    PI,
    TAU,
)

from .geometry import P

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------

RULER_COLOR = "#7FDBFF"
RULER_FILL = "#2E86AB"
COMPASS_COLOR = "#FFB347"
NEEDLE_COLOR = "#C0C0C0"
PENCIL_COLOR = "#FFD166"
CONSTRUCTION_COLOR = "#9BB7D4"
RESULT_COLOR = "#F5F5F5"


# ---------------------------------------------------------------------------
# Straightedge
# ---------------------------------------------------------------------------


class Straightedge(VGroup):
    """A translucent ruler that can be laid down between two points.

    The ruler's long axis is aligned with the local x-axis; use
    :meth:`lay_between` to position it.  Small tick marks suggest a graded
    edge (they are decorative — a mathematical straightedge has no scale).
    """

    def __init__(
        self,
        length: float = 5.0,
        width: float = 0.28,
        *,
        color=RULER_COLOR,
        fill_color=RULER_FILL,
        fill_opacity: float = 0.35,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.length = length
        self.ruler_width = width
        self.body = Rectangle(
            width=length,
            height=width,
            color=color,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            stroke_width=2,
        )
        self.add(self.body)

        # Decorative graded ticks along the upper edge.
        n = 24
        for i in range(n + 1):
            x = -length / 2 + length * i / n
            tick_len = width * (0.55 if i % 5 else 0.9)
            tick = Line(
                x * RIGHT + width / 2 * UP,
                x * RIGHT + (width / 2 - tick_len) * UP,
                color=color,
                stroke_width=1,
            )
            self.add(tick)

        # A centerline marking the actual drawing edge.
        self.edge = Line(
            length / 2 * LEFT,
            length / 2 * RIGHT,
            color=color,
            stroke_width=1,
            stroke_opacity=0.6,
        )
        self.edge.shift(width / 2 * UP)
        self.add(self.edge)

    def lay_between(self, a, b):
        """Move/rotate the ruler so its edge covers the segment ``a -> b``."""
        a, b = P(a), P(b)
        direction = b - a
        angle = np.arctan2(direction[1], direction[0])
        center = (a + b) / 2.0
        # The ruler must be at least as long as the requested segment.
        needed = float(np.linalg.norm(direction))
        if self.length < needed + 0.4:
            self.stretch_to_fit_width(needed + 0.8)
            self.length = needed + 0.8
        self.move_to(center)
        # Rotate directly (set_angle/get_angle are unavailable on a
        # point-less VGroup in modern Manim); the ruler starts horizontal.
        self.rotate(angle, about_point=center)
        # The drawing edge is the ruler's top long edge (y = +ruler_width/2
        # in local coordinates).  Offset the whole ruler by half its width so
        # that this edge — not the ruler's midline — coincides exactly with
        # the segment being drawn.
        perp = np.array([-np.sin(angle), np.cos(angle), 0.0])
        self.shift(-self.ruler_width / 2.0 * perp)
        return self


# ---------------------------------------------------------------------------
# Compass
# ---------------------------------------------------------------------------

# Half opening angle of the compass legs; fixed so the tool keeps a natural
# proportion at every radius.
_HALF_OPENING = 28 * DEGREES


class Compass(VGroup):
    """A pair of compass legs.

    The needle leg stays pinned at ``center`` while the pencil leg points at
    ``pencil`` (a point on the circle).  Both legs have equal length and meet
    at a hinge above the construction.
    """

    def __init__(
        self,
        center,
        pencil,
        *,
        leg_color=COMPASS_COLOR,
        needle_color=NEEDLE_COLOR,
        pencil_color=PENCIL_COLOR,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.center_pt = P(center)
        self.pencil_pt = P(pencil)

        radius = float(np.linalg.norm(self.pencil_pt - self.center_pt))
        leg_length = radius / (2.0 * np.cos(_HALF_OPENING)) if radius > 1e-9 else 1.0

        direction = self.pencil_pt - self.center_pt
        if radius > 1e-9:
            direction = direction / radius
        hinge = self.center_pt + leg_length * self._rot(direction, -_HALF_OPENING)

        self.needle_leg = Line(hinge, self.center_pt, color=leg_color, stroke_width=5)
        self.pencil_leg = Line(hinge, self.pencil_pt, color=leg_color, stroke_width=5)
        self.hinge_dot = Circle(0.06, color=leg_color, fill_opacity=1).move_to(hinge)

        # Needle point and pencil graphite point.
        self.needle = Dot(self.center_pt, radius=0.045, color=needle_color)
        self.pencil_tip = Dot(self.pencil_pt, radius=0.04, color=pencil_color)

        self.add(
            self.needle_leg,
            self.pencil_leg,
            self.hinge_dot,
            self.needle,
            self.pencil_tip,
        )

    @staticmethod
    def _rot(direction: np.ndarray, angle: float) -> np.ndarray:
        c, s = np.cos(angle), np.sin(angle)
        rot = np.array([[c, -s], [s, c]])
        out = np.zeros(3)
        out[:2] = rot @ direction[:2]
        return out

    def set_pencil(self, pencil):
        self.pencil_pt = P(pencil)
        return self


def make_compass_at(center, radius: float, angle: float) -> Compass:
    """Convenience: a compass whose pencil sits at polar position ``angle``."""
    c = P(center)
    pencil = c + radius * np.array([np.cos(angle), np.sin(angle), 0.0])
    return Compass(c, pencil)


def static_arc(center, radius: float, start_angle: float, angle: float, **kwargs) -> Arc:
    """A plain :class:`Arc` with argument order matching the sweep animation."""
    return Arc(
        radius=radius,
        start_angle=start_angle,
        angle=angle,
        arc_center=P(center),
        **kwargs,
    )
