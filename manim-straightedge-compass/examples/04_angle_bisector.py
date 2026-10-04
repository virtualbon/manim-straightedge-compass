"""Example 4: bisecting an angle (Elements I.9)."""

from manim import LEFT, RIGHT, UP, DOWN
from manim_sc import StraightedgeCompassScene


class AngleBisectorDemo(StraightedgeCompassScene):
    def construct(self):
        vertex = self.add_point(2.6 * LEFT + 1.4 * DOWN, "O")
        ray_a = self.add_point(2.4 * RIGHT + 0.6 * UP, "A")
        ray_b = self.add_point(2.6 * RIGHT + 1.5 * DOWN, "B")

        self.draw_segment(vertex, ray_a)
        self.draw_segment(vertex, ray_b)

        line, q = self.angle_bisector(vertex, ray_a, ray_b)

        self.wait(0.6)
        self.fade_construction()
        self.emphasize(line)
        self.wait(0.5)
