"""等边三角形的作法（《几何原本》第一卷命题 1）。

给定线段 AB：
1. 以 A 为圆心、AB 为半径作圆；
2. 以 B 为圆心、BA 为半径作圆；
3. 两圆的一个交点为 C，连接 AC、BC，即得等边三角形 ABC。
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from manim import UP, DOWN
from manim_sc import (
    EuclidScene, P, distance,
    circle_circle_intersection, uppermost,
)


class EquilateralTriangle(EuclidScene):
    def construct(self):
        self.intro("等边三角形的作法")

        A, B = P(-1.5, -0.7), P(1.5, -0.7)
        r = distance(A, B)

        self.mark_point(A, "A", direction=0.45 * DOWN)
        self.mark_point(B, "B", direction=0.45 * DOWN)

        self.draw_circle(A, radius=r)
        self.draw_circle(B, radius=r)

        C = uppermost(circle_circle_intersection(A, r, B, r))
        self.mark_point(C, "C", direction=0.45 * UP)

        self.draw_segment(A, B)
        self.draw_segment(A, C)
        self.draw_segment(B, C)
        self.wait(1)
