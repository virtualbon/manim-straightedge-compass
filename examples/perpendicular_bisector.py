"""作已知线段的垂直平分线（中点）。

1. 分别以线段两端 A、B 为圆心，以相同的（大于 AB/2 的）半径作圆；
2. 两圆交于 C、D 两点；
3. 直线 CD 就是 AB 的垂直平分线，CD 与 AB 的交点 M 即中点。
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from manim import UP, DOWN, RIGHT
from manim_sc import (
    EuclidScene, P,
    circle_circle_intersection, line_line_intersection,
    uppermost, lowermost,
)


class PerpendicularBisector(EuclidScene):
    def construct(self):
        self.intro("垂直平分线（中点）的作法")

        A, B = P(-2.2, -0.2), P(2.2, -0.2)
        r = 3.0

        self.draw_segment(A, B)
        self.mark_point(A, "A", direction=0.45 * DOWN)
        self.mark_point(B, "B", direction=0.45 * DOWN)

        self.draw_circle(A, radius=r)
        self.draw_circle(B, radius=r)

        hits = circle_circle_intersection(A, r, B, r)
        C, D = uppermost(hits), lowermost(hits)
        self.mark_point(C, "C", direction=0.4 * UP)
        self.mark_point(D, "D", direction=0.4 * DOWN)

        self.draw_segment(C, D, color="#7AE0A8")
        M = line_line_intersection(A, B, C, D)
        self.mark_point(M, "M", direction=0.4 * UP + 0.15 * RIGHT,
                        color="#FFD54F")
        self.wait(1)
