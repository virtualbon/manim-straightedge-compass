"""正十七边形的尺规作图（Richmond, 1893）——完整构造版。

每一条构造线都在画面上用圆规/直尺实际作出；只在某一步完成使命后，
才把该步的中间痕迹淡出：

  0. 大圆与水平直径；
  1. 用线段垂直平分线作法作出竖直直径（两端点等半径弧 → 连线）；
  2. 两次平分 OB，得到四等分点 J（中点随即淡出）；
  3. 连 JA，两次平分 ∠OJA 得四分之一角方向，交底直径于 E（平分用弧淡出）；
  4. 完整作出 45°：先过 J 作 JE 的垂线，再平分该直角，方向交底直径于 F
     （垂线作法的辅助弧用完即淡出）；
  5. 以 AF 为直径作圆交竖直直径于 K；
  6. 以 E 为心、EK 为半径作圆，交底直径于 N3、N5；
  7. N3、N5 处的垂线交大圆于 P3、P5，Richmond 主干构造整体淡出；
  8. 弧 P3P5 的中点为 P4（平分弧淡出）；
  9. 圆规取边长 P3P4 绕圆截出全部顶点（截取弧淡出）；
 10. 直尺连续画出十七条边。
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
from manim import TAU, PI, UP, DOWN, LEFT, RIGHT, FadeOut
from manim_sc import (
    EuclidScene, P, unit, midpoint, distance, angle_of,
    circle_circle_intersection, circle_line_intersection,
    uppermost, lowermost,
    CONSTRUCTION_GREEN, RESULT_COLOR,
)

GUIDE_COLOR = "#8A97A5"
AUX_POINT = "#F2C744"


class Heptadecagon(EuclidScene):

    # ---------------------------------------------------------- small helpers

    def _arc(self, center, r, theta, span=0.7, color=CONSTRUCTION_GREEN,
             run_time=0.4, keep=False, stroke_width=1.5):
        """A short compass arc centred at ``theta`` (radians)."""
        return self.draw_arc(center, r, start_angle=theta - span / 2,
                             angle=span, color=color, stroke_width=stroke_width,
                             run_time=run_time, keep_compass=keep)

    def _pair_arcs(self, c1, r1, c2, r2, run_time=0.38):
        """Four short arcs (two about each circle's intersections) for the
        classic equal-radius construction; returns the two intersections."""
        hits = circle_circle_intersection(c1, r1, c2, r2)
        arcs = []
        for h in hits:
            arcs.append(self._arc(c1, r1, angle_of(c1, h),
                                  run_time=run_time, keep=True))
        for i, h in enumerate(hits):
            arcs.append(self._arc(c2, r2, angle_of(c2, h),
                                  run_time=run_time, keep=(i == 0)))
        return hits, arcs

    def bisect_segment(self, p1, p2, run_time=0.38):
        """Perpendicular-bisector construction of the midpoint of p1p2."""
        rr = distance(p1, p2) * 0.78
        hits, arcs = self._pair_arcs(p1, rr, p2, rr, run_time=run_time)
        return midpoint(p1, p2), arcs

    def bisect_angle(self, vertex, ang_lo, ang_hi, rarc=0.52, rr=0.40,
                     run_time=0.42):
        """Compass-and-straightedge angle bisection between two absolute
        directions; returns (middle direction, trace mobjects)."""
        mid_ang = (ang_lo + ang_hi) / 2
        traces = [self._arc(vertex, rarc, mid_ang,
                            span=(ang_hi - ang_lo) + 0.12, color=GUIDE_COLOR,
                            run_time=run_time + 0.1, keep=True)]
        q1 = vertex + rarc * P(np.cos(ang_lo), np.sin(ang_lo))
        q2 = vertex + rarc * P(np.cos(ang_hi), np.sin(ang_hi))
        hits = circle_circle_intersection(q1, rr, q2, rr)
        inner = max(hits, key=lambda h: float(
            np.dot(h - vertex, P(np.cos(mid_ang), np.sin(mid_ang)))))
        traces.append(self._arc(q1, rr, angle_of(q1, inner),
                                run_time=run_time, keep=True))
        traces.append(self._arc(q2, rr, angle_of(q2, inner),
                                run_time=run_time))
        return mid_ang, traces

    def fade(self, *groups, run_time=0.7):
        mobjs = [m for g in groups for m in (g if isinstance(g, list) else [g])]
        mobjs = [m for m in mobjs if m is not None]
        if mobjs:
            self.play(*[FadeOut(m) for m in mobjs], run_time=run_time)

    # -------------------------------------------------------------- the proof

    def construct(self):
        self.tool_travel_time = 0.4
        self.intro("正十七边形的尺规作法 · Richmond（完整过程）")

        R = 2.55
        O = P(0, -0.2)
        verts = [O + R * P(np.cos(k * TAU / 17), np.sin(k * TAU / 17))
                 for k in range(17)]
        A = verts[0]
        AL = O - R * RIGHT          # left end of the horizontal diameter
        main = []                   # Richmond backbone traces, faded at step 7

        # ---- 0. horizontal diameter and the circumcircle ----
        main.append(self.draw_segment(AL, A, color=GUIDE_COLOR,
                                      stroke_width=1.5, run_time=0.7))
        self.draw_circle(O, radius=R)
        # O and A survive to the final picture, so they are NOT tracked in main
        self.mark_point(O, "O", direction=0.4 * DOWN + 0.15 * LEFT)
        self.mark_point(A, "A", direction=0.45 * RIGHT)

        # ---- 1. vertical diameter via perpendicular bisector of AL-A ----
        rr = R * 1.12
        hits, temp = self._pair_arcs(AL, rr, A, rr)
        u, d = uppermost(hits), lowermost(hits)
        main.append(self.draw_segment(d, u, color=GUIDE_COLOR,
                                      stroke_width=1.5, run_time=0.7))
        B = O + R * UP
        main.append(self.mark_point(B, color=AUX_POINT, radius=0.05))
        self.fade(temp)

        # ---- 2. J = quarter point of OB: two successive bisections ----
        M1, arcs_a = self.bisect_segment(O, B)
        m1dot = self.mark_point(M1, color=AUX_POINT, radius=0.05)
        J, arcs_b = self.bisect_segment(O, M1)
        jmark = self.mark_point(J, "J", direction=0.35 * LEFT,
                                color=AUX_POINT, radius=0.05)
        self.fade(arcs_a, arcs_b, m1dot)
        main.append(jmark)

        # ---- 3. join JA; bisect angle OJA twice -> E ----
        main.append(self.draw_segment(J, A, color=GUIDE_COLOR,
                                      stroke_width=1.5, run_time=0.7))
        aJO, aJA = angle_of(J, O), angle_of(J, A)
        a_half, g1 = self.bisect_angle(J, aJO, aJA)
        half_line = self.draw_segment(
            J, J + 0.95 * P(np.cos(a_half), np.sin(a_half)),
            color=GUIDE_COLOR, stroke_width=1.2, run_time=0.5)
        a_quarter, g2 = self.bisect_angle(J, aJO, a_half)

        def ray_to_diameter(vertex, ang, y0):
            t = (y0 - vertex[1]) / np.sin(ang)
            return vertex + t * P(np.cos(ang), np.sin(ang))

        E = ray_to_diameter(J, a_quarter, O[1])
        main.append(self.draw_segment(J, E, color=GUIDE_COLOR,
                                      stroke_width=1.5, run_time=0.6))
        emark = self.mark_point(E, "E", direction=0.4 * DOWN,
                                color=AUX_POINT, radius=0.05)
        self.fade(g1, g2, half_line)
        main.append(emark)

        # ---- 4. construct angle EJF = 45° properly ----
        # 4a. perpendicular to JE through J: equal arcs either side of J
        r0 = 0.5
        dq = P(np.cos(a_quarter), np.sin(a_quarter))
        t1, t2 = J + r0 * dq, J - r0 * dq
        perp_ang = a_quarter - PI / 2
        dp = P(np.cos(perp_ang), np.sin(perp_ang))
        temp45 = [self._arc(J, r0, a_quarter, run_time=0.38, keep=True),
                  self._arc(J, r0, a_quarter + PI, run_time=0.38, keep=True)]
        rr_p = 0.62
        hits = circle_circle_intersection(t1, rr_p, t2, rr_p)
        up = max(hits, key=lambda h: float(np.dot(h - J, dp)))
        temp45.append(self._arc(t1, rr_p, angle_of(t1, up),
                                run_time=0.38, keep=True))
        temp45.append(self._arc(t2, rr_p, angle_of(t2, up),
                                run_time=0.38))
        perp_line = self.draw_segment(
            J, J + 0.9 * dp, color=GUIDE_COLOR, stroke_width=1.2,
            run_time=0.5)
        temp45.append(perp_line)
        # 4b. bisect the right angle between JE and its perpendicular
        w1, w2 = t1, J + r0 * dp
        rr_b = 0.46
        bis_ang = a_quarter - PI / 4
        hits = circle_circle_intersection(w1, rr_b, w2, rr_b)
        v = max(hits, key=lambda h: float(
            np.dot(h - J, P(np.cos(bis_ang), np.sin(bis_ang)))))
        temp45.append(self._arc(w1, rr_b, angle_of(w1, v),
                                run_time=0.38, keep=True))
        temp45.append(self._arc(w2, rr_b, angle_of(w2, v),
                                run_time=0.38))
        aJF = angle_of(J, v)
        assert abs(((aJF - bis_ang + PI) % TAU) - PI) < 0.02
        F = ray_to_diameter(J, aJF, O[1])
        main.append(self.draw_segment(J, F, color=GUIDE_COLOR,
                                      stroke_width=1.5, run_time=0.6))
        fmark = self.mark_point(F, "F",
                                direction=0.4 * DOWN + 0.2 * LEFT,
                                color=AUX_POINT, radius=0.05)
        self.fade(temp45)
        main.append(fmark)

        # ---- 5. circle on diameter AF meets vertical diameter at K ----
        cAF = midpoint(A, F)
        rAF = distance(A, F) / 2
        main.append(self.draw_circle(cAF, radius=rAF, run_time=1.5))
        Khits = circle_line_intersection(cAF, rAF, O + P(0, 1), O + P(0, -1))
        K = uppermost(Khits)
        main.append(self.mark_point(K, "K",
                                    direction=0.3 * UP + 0.25 * RIGHT,
                                    color=AUX_POINT, radius=0.05))

        # ---- 6. circle centred at E through K -> N3, N5 ----
        rEK = distance(E, K)
        main.append(self.draw_circle(E, radius=rEK, color=CONSTRUCTION_GREEN,
                                     run_time=1.5))
        Nhits = sorted(circle_line_intersection(
            E, rEK, O + P(-1, 0), O + P(1, 0)), key=lambda q: q[0])
        N_for_P5, N_for_P3 = Nhits[0], Nhits[1]
        main.append(self.mark_point(N_for_P3, "N_3",
                                    direction=0.4 * UP + 0.15 * RIGHT,
                                    color=AUX_POINT, radius=0.05))
        main.append(self.mark_point(N_for_P5, "N_5",
                                    direction=0.4 * UP + 0.2 * LEFT,
                                    color=AUX_POINT, radius=0.05))

        # ---- 7. perpendiculars up to the circumcircle give P3 and P5 ----
        P3 = P5 = None
        for N, which in ((N_for_P3, "P3"), (N_for_P5, "P5")):
            main.append(self.draw_segment(N + P(0, R + 0.25), N + P(0, -0.2),
                                          color=GUIDE_COLOR, stroke_width=1.5,
                                          run_time=0.55))
            p = uppermost(circle_line_intersection(
                O, R, N + P(0, 1), N + P(0, -1)))
            if which == "P3":
                P3 = p
            else:
                P5 = p
        assert np.linalg.norm(P3 - verts[3]) < 0.03
        assert np.linalg.norm(P5 - verts[5]) < 0.03

        # Richmond backbone has finished its job
        self.fade(main, run_time=1.1)
        self.mark_point(P3, "P_3", direction=unit(P3 - O) * 0.55)
        self.mark_point(P5, "P_5", direction=unit(P5 - O) * 0.55)

        # ---- 8. P4 = midpoint of arc P3P5 ----
        rr4 = distance(P3, P5) * 0.85
        hits = circle_circle_intersection(P3, rr4, P5, rr4)
        top, bot = uppermost(hits), lowermost(hits)
        arc4 = [self._arc(P3, rr4, angle_of(P3, top), run_time=0.5,
                          keep=True),
                self._arc(P5, rr4, angle_of(P5, top), run_time=0.5)]
        d = top - bot
        if d[1] < 0:
            d = -d
        P4 = O + R * unit(d)
        assert np.linalg.norm(P4 - verts[4]) < 0.03
        self.mark_point(P4, "P_4", direction=unit(P4 - O) * 0.55,
                        color="#7AE0A8")
        self.fade(arc4)

        # ---- 9. carry side length P3P4 around the circle ----
        side = distance(P3, P4)
        green = []

        def step(prev, nxt, keep):
            th = angle_of(prev, nxt)
            g = self.draw_arc(prev, side, start_angle=th - 0.28, angle=0.56,
                              color=CONSTRUCTION_GREEN, stroke_width=1.5,
                              run_time=0.42, keep_compass=keep)
            green.append(g)
            self.mark_point(nxt, radius=0.05, run_time=0.16)

        step(P3, verts[2], keep=True)
        step(verts[2], verts[1], keep=True)
        for k in range(5, 16):
            step(verts[k], verts[k + 1], keep=(k < 15))
        self.fade(green, run_time=0.8)

        # ---- 10. connect the seventeen vertices ----
        self.tool_travel_time = 0.26
        for k in range(17):
            last = k == 16
            self.draw_segment(verts[k], verts[(k + 1) % 17],
                              color=RESULT_COLOR, stroke_width=3,
                              run_time=0.32, keep_ruler=not last,
                              tip_fade=0.08)
        self.wait(1.5)
