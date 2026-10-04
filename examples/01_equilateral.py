"""Example 1: constructing an equilateral triangle (Euclid, Elements I.1)."""

from manim import LEFT, RIGHT, DOWN
from manim_sc import StraightedgeCompassScene


class EquilateralTriangleDemo(StraightedgeCompassScene):
    def construct(self):
        a = self.add_point(2 * LEFT + 0.6 * DOWN, "A")
        b = self.add_point(2 * RIGHT + 0.6 * DOWN, "B")

        _, _, c, edges = self.equilateral_triangle(a, b)

        self.wait(0.6)
        self.fade_construction()
        self.emphasize(*edges)
        self.wait(0.5)
