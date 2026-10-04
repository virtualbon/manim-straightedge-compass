"""Scene base class providing the straightedge-and-compass animation API."""

from __future__ import annotations

import numpy as np
from manim import (
    Scene,
    Line,
    Circle,
    Arc,
    FadeIn,
    FadeOut,
    Create,
    GrowFromCenter,
    Group,
    always_redraw,
    ValueTracker,
    DashedVMobject,
    TAU,
    PI,
)

from . import geometry as geo
from .marks import MarkedPoint
from .tools import (
    Straightedge,
    Compass,
    make_compass_at,
    static_arc,
    RULER_COLOR,
    COMPASS_COLOR,
    CONSTRUCTION_COLOR,
    RESULT_COLOR,
)


class StraightedgeCompassScene(Scene):
    """A :class:`~manim.Scene` extended with ruler-and-compass operations.

    Geometric primitives
    ---------------------
    add_point
        Place and label a point.
    draw_segment / draw_line
        Lay the straightedge and draw a segment / extended line.
    draw_circle / draw_arc
        Sweep the compass to leave a circle or arc.

    Intersections
    -------------
    intersections_of / mark_intersection
        Solve line-line, line-circle and circle-circle intersections.

    Construction helpers
    --------------------
    fade_construction
        Fade out auxiliary construction objects all at once.
    """

    # Timing ---------------------------------------------------------------
    ruler_settle_time: float = 0.7
    ruler_draw_time: float = 1.1
    compass_appear_time: float = 0.45
    compass_angular_speed: float = 2.6  # seconds per full turn
    point_grow_time: float = 0.35

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.construction_mobjects = Group()
        self.add(self.construction_mobjects)

    # ------------------------------------------------------------------ #
    # Points
    # ------------------------------------------------------------------ #

    def add_point(self, position, label: str | None = None, *, animate=True, **kwargs):
        """Place a :class:`MarkedPoint` (grows in by default)."""
        pt = MarkedPoint(position, label, **kwargs)
        if animate:
            self.play(GrowFromCenter(pt), run_time=self.point_grow_time)
        else:
            self.add(pt)
        return pt

    # ------------------------------------------------------------------ #
    # Straightedge
    # ------------------------------------------------------------------ #

    def _lay_ruler(self, a, b, run_time):
        ruler = Straightedge()
        a, b = geo.P(a), geo.P(b)
        angle = np.arctan2((b - a)[1], (b - a)[0])
        # Start resting parallel to the segment, offset to one side.
        perp = np.array([-np.sin(angle), np.cos(angle), 0.0])
        ruler.lay_between(a, b)
        ruler.shift(2.2 * perp)
        self.play(FadeIn(ruler, shift=-0.6 * perp), run_time=0.4)
        self.play(ruler.animate.shift(-2.2 * perp), run_time=run_time)
        return ruler

    def draw_segment(self, a, b, *, color=RESULT_COLOR, stroke_width=3,
                     run_time=None, construction=False, **kwargs):
        """Lay the straightedge along ``a -> b`` and draw the segment."""
        a, b = geo.P(a), geo.P(b)
        ruler = self._lay_ruler(a, b, self.ruler_settle_time)
        line = Line(a, b, color=color, stroke_width=stroke_width, **kwargs)
        line._sc_geom = ("line", np.array(a), np.array(b))
        self.play(Create(line), run_time=run_time or self.ruler_draw_time)
        self.play(FadeOut(ruler), run_time=0.3)
        if construction:
            # Create() added the line at scene top level; move it into the
            # construction group instead, so it lives in exactly one place.
            if line in self.mobjects:
                self.remove(line)
            self.construction_mobjects.add(line)
        return line

    def draw_line(self, a, b, *, extend: float = 1.0, color=RESULT_COLOR,
                  stroke_width=2, construction=False, **kwargs):
        """Draw an *extended* line through ``a`` and ``b``.

        ``extend`` is the extra length (scene units) added at each end.
        """
        a, b = geo.P(a), geo.P(b)
        direction = b - a
        norm = float(np.linalg.norm(direction))
        unit = direction / norm
        ea = a - extend * unit
        eb = b + extend * unit
        line = self.draw_segment(
            ea, eb, color=color, stroke_width=stroke_width, construction=construction, **kwargs
        )
        line._sc_geom = ("line", np.array(a), np.array(b))
        return line

    # ------------------------------------------------------------------ #
    # Compass
    # ------------------------------------------------------------------ #

    def compass_sweep(self, center, radius: float, start_angle: float,
                      sweep_angle: float, *, color=CONSTRUCTION_COLOR,
                      stroke_width=2, dashed=False, leave=True,
                      run_time=None, full_circle=False, construction=True):
        """Animate the compass sweeping an arc (or full circle).

        The returned object is a :class:`~manim.Circle` when ``full_circle``
        is true (or ``sweep_angle`` is a full turn), otherwise an
        :class:`~manim.Arc`.
        """
        center = geo.P(center)
        end_angle = start_angle + sweep_angle
        theta = ValueTracker(start_angle)

        compass = always_redraw(
            lambda: make_compass_at(center, radius, theta.get_value())
        )
        arc = always_redraw(
            lambda: static_arc(
                center,
                radius,
                start_angle,
                theta.get_value() - start_angle,
                color=color,
                stroke_width=stroke_width,
            )
        )
        self.play(FadeIn(compass), run_time=self.compass_appear_time)
        self.add(arc)
        sweep_time = run_time or max(
            0.8, abs(sweep_angle) / TAU * self.compass_angular_speed
        )
        self.play(theta.animate.set_value(end_angle), run_time=sweep_time)
        self.play(FadeOut(compass), run_time=0.3)

        if not leave:
            self.remove(arc)
            return None

        # Replace the redrawn arc with a static object.
        self.remove(arc)
        if full_circle or abs(abs(sweep_angle) - TAU) < 1e-6:
            static = Circle(radius=radius, color=color, stroke_width=stroke_width)
            static.move_to(center)
        else:
            static = static_arc(
                center, radius, start_angle, sweep_angle,
                color=color, stroke_width=stroke_width,
            )
        if dashed:
            static = DashedVMobject(static, num_dashes=40)
        static._sc_geom = ("circle", np.array(center), float(radius))
        if construction:
            self.construction_mobjects.add(static)
        else:
            self.add(static)
        return static

    def draw_circle(self, center, through=None, *, radius: float | None = None,
                    color=CONSTRUCTION_COLOR, stroke_width=2, dashed=False,
                    run_time=None, construction=True):
        """Draw a full circle, defined by center and either a point or radius."""
        center = geo.P(center)
        if radius is None:
            if through is None:
                raise ValueError("draw_circle requires either 'through' or 'radius'")
            radius = geo.dist(center, through)
        return self.compass_sweep(
            center, radius, start_angle=0.0, sweep_angle=TAU,
            color=color, stroke_width=stroke_width, dashed=dashed,
            run_time=run_time, full_circle=True, construction=construction,
        )

    def draw_arc(self, center, radius: float, start_angle: float,
                 sweep_angle: float, *, color=CONSTRUCTION_COLOR,
                 stroke_width=2, construction=True, **kwargs):
        """Draw a circular arc with the compass."""
        return self.compass_sweep(
            center, radius, start_angle, sweep_angle,
            color=color, stroke_width=stroke_width,
            construction=construction, **kwargs,
        )

    # ------------------------------------------------------------------ #
    # Intersections
    # ------------------------------------------------------------------ #

    def _geom_of(self, mobject):
        if hasattr(mobject, "_sc_geom"):
            return mobject._sc_geom
        if isinstance(mobject, Circle):
            return ("circle", mobject.get_center(), float(mobject.radius))
        if isinstance(mobject, Line):
            return ("line", mobject.get_start(), mobject.get_end())
        raise TypeError(f"Cannot extract geometry from {mobject}")

    def intersections_of(self, o1, o2):
        """All intersection points of two drawn lines/circles/arcs."""
        kind1, *g1 = self._geom_of(o1)
        kind2, *g2 = self._geom_of(o2)
        if kind1 == "line" and kind2 == "line":
            pt = geo.line_line_intersection(*g1, *g2)
            return [pt] if pt is not None else []
        if kind1 == "circle" and kind2 == "circle":
            return geo.circle_circle_intersection(g1[0], g1[1], g2[0], g2[1])
        # Mixed line / circle.
        if kind1 == "line":
            return geo.line_circle_intersection(*g1, g2[0], g2[1])
        return geo.line_circle_intersection(*g2, g1[0], g1[1])

    def mark_intersection(self, o1, o2, *, which: int = 0,
                          label: str | None = None, **kwargs):
        """Compute an intersection and mark it with a :class:`MarkedPoint`.

        ``which`` selects among the (up to two) intersections.  Keyword
        arguments are forwarded to :class:`MarkedPoint`.
        """
        pts = self.intersections_of(o1, o2)
        if not pts:
            raise ValueError("The two objects do not intersect")
        if which >= len(pts):
            raise IndexError(
                f"Intersection index {which} out of range (found {len(pts)})"
            )
        return self.add_point(pts[which], label, **kwargs)

    # ------------------------------------------------------------------ #
    # Bookkeeping
    # ------------------------------------------------------------------ #

    def fade_construction(self, *extra, run_time: float = 1.0):
        """Fade out every auxiliary object drawn with ``construction=True``."""
        anims = []
        if len(self.construction_mobjects) > 0:
            anims.append(FadeOut(self.construction_mobjects))
        anims.extend(FadeOut(e) for e in extra)
        if anims:
            self.play(*anims, run_time=run_time)
        self.remove(self.construction_mobjects)
        self.construction_mobjects = Group()
        self.add(self.construction_mobjects)

    def emphasize(self, *mobjects, color="#FFD166", width=5, run_time=0.8):
        """Temporarily highlight result objects, then restore their style."""
        originals = [(m, m.get_color(), m.get_stroke_width()) for m in mobjects]
        self.play(
            *[m.animate.set_stroke(color=color, width=width) for m in mobjects],
            run_time=run_time,
        )
        self.play(
            *[m.animate.set_stroke(color=c, width=w) for m, c, w in originals],
            run_time=run_time,
        )
