"""Example 2: midpoint and perpendicular bisector of a segment (Elements I.10)."""

from manim import LEFT, RIGHT, UP
from manim_sc import StraightedgeCompassScene


class MidpointDemo(StraightedgeCompassScene):
    def construct(self):
        a = self.add_point(2.6 * LEFT + 0.4 * UP, "A")
        b = self.add_point(2.6 * RIGHT + 0.4 * UP, "B")
        self.draw_segment(a, b)

        m, bisector = self.midpoint(a, b)

        self.wait(0.6)
        self.fade_construction()
        self.emphasize(m)
        self.wait(0.5)
