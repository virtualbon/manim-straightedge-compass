"""Example 5: drawing a parallel line through an external point."""

from manim import LEFT, RIGHT, UP, DOWN
from manim_sc import StraightedgeCompassScene


class ParallelLineDemo(StraightedgeCompassScene):
    def construct(self):
        a = 2.8 * LEFT + 0.8 * DOWN
        b = 2.8 * RIGHT + 0.2 * UP
        p = self.add_point(1.6 * UP, "P")

        original = self.draw_line(a, b, extend=0.6)
        parallel = self.parallel_through(p, a, b)

        self.wait(0.6)
        self.fade_construction()
        self.emphasize(original, parallel)
        self.wait(0.5)
