"""作已知角的平分线。

设角的两边从 O 出发：
1. 以 O 为圆心作弧，分别交两边于 P、Q；
2. 再分别以 P、Q 为圆心，以相同半径作弧，两弧交于角内一点 R；
3. 直线 OR 即角平分线（两弧的另一交点正是 O）。
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
from manim import UP, DOWN, LEFT, RIGHT
from manim_sc import (
    EuclidScene, P, unit, angle_of,
    circle_circle_intersection, other,
    CONSTRUCTION_GREEN,
)


class AngleBisector(EuclidScene):
    def construct(self):
        self.intro("角平分线的作法")

        O = P(0, -1.4)
        a1, a2 = np.radians(98.0), np.radians(28.0)
        side1_end = O + 3.1 * P(np.cos(a1), np.sin(a1))
        side2_end = O + 3.1 * P(np.cos(a2), np.sin(a2))

        # the given angle
        self.draw_segment(O, side1_end)
        self.draw_segment(O, side2_end)
        self.mark_point(O, "O", direction=0.5 * DOWN)

        # arc centred at O, crossing both sides at P, Q
        rO = 2.1
        Pnt = O + rO * P(np.cos(a1), np.sin(a1))
        Qnt = O + rO * P(np.cos(a2), np.sin(a2))
        self.draw_arc(O, rO, start_angle=a2, angle=a1 - a2)
        self.mark_point(Pnt, "P", direction=0.35 * UP + 0.2 * LEFT)
        self.mark_point(Qnt, "Q", direction=0.3 * RIGHT + 0.15 * UP)

        # equal arcs centred at P and Q; they meet at O and at R
        r2 = rO
        hits = circle_circle_intersection(Pnt, r2, Qnt, r2)
        R = other(hits, O)
        ang_PR = angle_of(Pnt, R)
        ang_QR = angle_of(Qnt, R)
        self.draw_arc(Pnt, r2, start_angle=ang_PR - 0.55, angle=1.1,
                      color=CONSTRUCTION_GREEN, keep_compass=True)
        self.draw_arc(Qnt, r2, start_angle=ang_QR - 0.55, angle=1.1,
                      color=CONSTRUCTION_GREEN)
        self.mark_point(R, "R", direction=0.35 * UP + 0.25 * RIGHT,
                        color="#7AE0A8")

        # the bisector, extended a little past R
        tip = O + unit(R - O) * 3.2
        self.draw_segment(O, tip, color="#7AE0A8")
        self.wait(1)
