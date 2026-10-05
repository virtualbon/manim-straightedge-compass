"""圆内接正六边形的作法。

圆内接正六边形的边长恰好等于半径：
1. 作基圆，圆心 O，在圆上取起点 A；
2. 以 A 为圆心、半径 OA 作弧，与基圆交于 B；
3. 依次以 B、C、D、E 为圆心重复，得到六个顶点 A…F；
4. 顺次连接六个顶点即得正六边形。
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
from manim import UP, DOWN, LEFT, RIGHT, TAU
from manim_sc import (
    EuclidScene, P, angle_of,
    circle_circle_intersection, other,
    CONSTRUCTION_GREEN,
)


class RegularHexagon(EuclidScene):
    def construct(self):
        self.intro("圆内接正六边形的作法")

        O = P(0, -0.1)
        R = 2.0
        verts = [O + R * P(np.cos(k * TAU / 6), np.sin(k * TAU / 6))
                 for k in range(6)]
        A, B, C, D, E, F = verts
        labels = ["A", "B", "C", "D", "E", "F"]
        label_dirs = [RIGHT, 0.6 * UP + 0.3 * RIGHT, 0.6 * UP + 0.3 * LEFT,
                      LEFT, 0.6 * DOWN + 0.3 * LEFT, 0.6 * DOWN + 0.3 * RIGHT]

        self.draw_circle(O, radius=R)
        self.mark_point(O, "O", direction=0.4 * DOWN + 0.15 * LEFT)
        self.mark_point(A, "A", direction=0.45 * RIGHT)

        # walk around the circle: arc centred at the previous vertex passes
        # through the next one (and also the one before it).
        prev = A
        for k in range(1, 6):
            nxt = verts[k]
            theta = angle_of(prev, nxt)
            self.draw_arc(prev, R, start_angle=theta - 0.38, angle=0.76,
                          color=CONSTRUCTION_GREEN,
                          keep_compass=(k < 5))
            self.mark_point(nxt, labels[k], direction=label_dirs[k])
            prev = nxt

        for k in range(6):
            self.draw_segment(verts[k], verts[(k + 1) % 6])
        self.wait(1)
