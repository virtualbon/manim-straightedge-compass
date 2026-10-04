"""Example 3: a regular hexagon inscribed in a circle (Elements IV.15)."""

from manim import ORIGIN, RIGHT
from manim_sc import StraightedgeCompassScene


class HexagonDemo(StraightedgeCompassScene):
    def construct(self):
        center = self.add_point(ORIGIN, "O")
        v0 = self.add_point(2.2 * RIGHT, "A")

        verts, edges = self.regular_hexagon(
            center, v0, label_vertices=True
        )

        self.wait(0.6)
        self.fade_construction()
        self.emphasize(*edges)
        self.wait(0.5)
