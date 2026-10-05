"""过直线外一点作已知直线的垂线。

1. 以直线外点 P 为圆心作弧，交直线于 X、Y 两点；
2. 保持半径不变（半径取 PX = PY），分别以 X、Y 为圆心在直线另一侧作弧，
   两弧交于 Q（P 关于该直线的镜像点）；
3. 直线 PQ 即所求垂线，它与已知直线的交点 F 即垂足。
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
from manim import UP, DOWN, LEFT, RIGHT
from manim_sc import (
    EuclidScene, P, angle_of,
    circle_line_intersection, circle_circle_intersection,
    line_line_intersection, other,
    CONSTRUCTION_GREEN,
)


class PerpendicularFromPoint(EuclidScene):
    def construct(self):
        self.intro("过直线外一点作垂线")

        A, B = P(-2.9, -0.4), P(2.9, -0.4)
        Pnt = P(0.6, 2.0)
        r = 3.2

        self.draw_segment(A, B)
        self.mark_point(Pnt, "P", direction=0.4 * UP)

        # arc centred at P, crossing the line at X and Y
        hits = circle_line_intersection(Pnt, r, A, B)
        hits.sort(key=lambda q: q[0])
        X, Y = hits
        aX, aY = angle_of(Pnt, X), angle_of(Pnt, Y)
        lo, hi = min(aX, aY), max(aX, aY)
        self.draw_arc(Pnt, r, start_angle=lo, angle=hi - lo)
        self.mark_point(X, "X", direction=0.45 * DOWN)
        self.mark_point(Y, "Y", direction=0.45 * DOWN)

        # equal arcs on the other side, meeting at Q
        hits2 = circle_circle_intersection(X, r, Y, r)
        Q = other(hits2, Pnt)
        aXQ, aYQ = angle_of(X, Q), angle_of(Y, Q)
        self.draw_arc(X, r, start_angle=aXQ - 0.55, angle=1.1,
                      color=CONSTRUCTION_GREEN, keep_compass=True)
        self.draw_arc(Y, r, start_angle=aYQ - 0.55, angle=1.1,
                      color=CONSTRUCTION_GREEN)
        self.mark_point(Q, "Q", direction=0.45 * DOWN, color="#7AE0A8")

        F = line_line_intersection(A, B, Pnt, Q)
        self.draw_segment(Pnt, Q, color="#7AE0A8")
        self.mark_point(F, "F", direction=0.35 * UP + 0.2 * RIGHT,
                        color="#FFD54F")
        self.wait(1)
