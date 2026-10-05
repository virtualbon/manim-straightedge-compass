"""把已知线段的长度复制到射线上。

1. 已知线段 AB 和从 O 出发的射线；
2. 圆规张开成 AB 的长度（以 A 为圆心过 B 作弧）；
3. 保持张角不变，把圆规搬到 O，作弧与射线交于 D；
4. 则 OD = AB。
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
from manim import UP, DOWN, LEFT, RIGHT
from manim_sc import (
    EuclidScene, P, distance, angle_of, RESULT_RED,
)


class CopySegment(EuclidScene):
    def construct(self):
        self.intro("复制线段长度")

        A, B = P(-4.4, 1.3), P(-2.7, 0.7)
        O = P(-0.3, -1.7)
        ray_angle = np.radians(32.0)
        C = O + 3.4 * P(np.cos(ray_angle), np.sin(ray_angle))
        r = distance(A, B)

        # given segment and target ray
        self.draw_segment(A, B)
        self.mark_point(A, "A", direction=0.4 * UP + 0.2 * LEFT)
        self.mark_point(B, "B", direction=0.35 * UP + 0.3 * RIGHT)
        self.draw_segment(O, C)
        self.mark_point(O, "O", direction=0.5 * DOWN + 0.2 * LEFT)
        self.mark_point(C, "l", direction=0.3 * UP + 0.3 * RIGHT)

        # pick up the length AB ...
        self.draw_arc(A, r, start_angle=angle_of(A, B) - 0.6, angle=1.2,
                      keep_compass=True)
        # ... carry the unchanged opening over to O
        self.draw_arc(O, r, start_angle=ray_angle - 0.6, angle=1.2)

        D = O + r * P(np.cos(ray_angle), np.sin(ray_angle))
        self.mark_point(D, "D", direction=0.4 * DOWN + 0.3 * RIGHT,
                        color="#FFD54F")
        # highlight the copied length OD
        self.draw_segment(O, D, color=RESULT_RED, stroke_width=5)
        self.wait(1)
