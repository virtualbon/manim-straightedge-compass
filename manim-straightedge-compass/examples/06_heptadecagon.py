"""Example 6: regular heptadecagon (17-gon) via Richmond's construction.

Gauss proved the regular 17-gon constructible in 1796 (17 is a Fermat
prime, 2^4 + 1); Richmond gave this compact straightedge-and-compass
construction in 1893.
"""

from manim import ORIGIN, RIGHT
from manim_sc import StraightedgeCompassScene


class HeptadecagonDemo(StraightedgeCompassScene):
    # Quicker pacing so the long construction stays watchable.
    compass_angular_speed = 1.6
    compass_appear_time = 0.3
    ruler_settle_time = 0.4
    ruler_draw_time = 0.6

    def construct(self):
        center = self.add_point(ORIGIN, "O")
        v0 = self.add_point(2.3 * RIGHT, "V0")

        verts, edges = self.heptadecagon(
            center, v0, label_helpers=True, label_key_vertices=False
        )

        self.wait(0.6)
        self.fade_construction()
        self.emphasize(*edges, run_time=0.7)
        self.wait(0.6)
