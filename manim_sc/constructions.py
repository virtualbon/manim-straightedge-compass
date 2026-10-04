"""Classic straightedge-and-compass constructions, fully animated.

Every function takes a :class:`~manim_sc.scene.StraightedgeCompassScene` as
its first argument and plays the complete construction animation.  Points may
be passed as coordinate arrays, tuples, or :class:`~manim_sc.marks.MarkedPoint`.
"""

from __future__ import annotations

import numpy as np
from manim import TAU, PI

from . import geometry as geo
from .tools import CONSTRUCTION_COLOR, RESULT_COLOR


# ---------------------------------------------------------------------------
# Equilateral triangle (Elements I.1)
# ---------------------------------------------------------------------------


def equilateral_triangle(scene, a, b, *, which: int = 0, draw_base: bool = True,
                         labels=("A", "B", "C"), color=RESULT_COLOR):
    """Construct an equilateral triangle on segment ``a-b``.

    Two circles of radius ``|ab|`` centered at ``a`` and ``b`` meet at the
    third vertex.  ``which`` chooses the intersection (0 = left of the
    directed segment a->b, 1 = right).
    Returns ``(a, b, c, edges)`` where ``edges`` is a list of the drawn sides.
    """
    a, b = geo.P(a), geo.P(b)
    radius = geo.dist(a, b)
    scene.draw_circle(a, radius=radius)
    scene.draw_circle(b, radius=radius)
    pts = geo.circle_circle_intersection(a, radius, b, radius)
    c = scene.add_point(pts[which], labels[2])

    edges = []
    if draw_base:
        edges.append(scene.draw_segment(a, b, color=color))
    edges.append(scene.draw_segment(a, c, color=color))
    edges.append(scene.draw_segment(b, c, color=color))
    return a, b, c, edges


# ---------------------------------------------------------------------------
# Perpendicular bisector & midpoint (Elements I.10)
# ---------------------------------------------------------------------------


def perpendicular_bisector(scene, a, b, *, radius: float | None = None,
                           extend: float = 0.8):
    """Construct the perpendicular bisector of segment ``a-b``.

    Returns ``(midpoint, line)``.
    """
    a, b = geo.P(a), geo.P(b)
    r = radius if radius is not None else geo.dist(a, b) * 1.12
    scene.draw_circle(a, radius=r)
    scene.draw_circle(b, radius=r)
    pts = geo.circle_circle_intersection(a, r, b, r)
    x, y = pts[0], pts[1]
    line = scene.draw_line(x, y, extend=extend, color="#A8DADC", stroke_width=2)
    m = geo.line_line_intersection(a, b, x, y)
    return m, line


def midpoint(scene, a, b, *, label: str | None = "M"):
    """Construct and mark the midpoint of segment ``a-b``."""
    m, line = perpendicular_bisector(scene, a, b)
    mp = scene.add_point(m, label)
    return mp, line


# ---------------------------------------------------------------------------
# Perpendicular through a point on / off a line (Elements I.11, I.12)
# ---------------------------------------------------------------------------


def perpendicular_at(scene, p, l1, l2, *, radius: float | None = None,
                     extend: float = 0.8):
    """Perpendicular to line ``l1-l2`` *at* point ``p`` (p lies on the line).

    Returns the drawn perpendicular line.
    """
    p, l1, l2 = geo.P(p), geo.P(l1), geo.P(l2)
    r = radius if radius is not None else max(0.6, geo.dist(l1, l2) * 0.28)
    scene.draw_circle(p, radius=r)
    hits = geo.line_circle_intersection(l1, l2, p, r)
    x, y = hits[0], hits[1]
    # Perpendicular bisector of the chord x-y passes through p.
    scene.draw_circle(x, radius=r * 1.55)
    scene.draw_circle(y, radius=r * 1.55)
    pts = geo.circle_circle_intersection(x, r * 1.55, y, r * 1.55)
    line = scene.draw_line(pts[0], pts[1], extend=extend, color="#A8DADC")
    return line


def perpendicular_through(scene, p, l1, l2, *, extend: float = 0.8):
    """Perpendicular to line ``l1-l2`` *through external point* ``p``.

    A circle centered at ``p`` cuts the line at x, y; the perpendicular
    bisector of chord x-y passes through p.  Returns the drawn line.
    """
    p, l1, l2 = geo.P(p), geo.P(l1), geo.P(l2)
    r = max(geo.dist(p, l1), geo.dist(p, l2)) + 0.4
    scene.draw_circle(p, radius=r)
    hits = geo.line_circle_intersection(l1, l2, p, r)
    x, y = hits[0], hits[1]
    r2 = r * 1.05
    scene.draw_circle(x, radius=r2)
    scene.draw_circle(y, radius=r2)
    pts = geo.circle_circle_intersection(x, r2, y, r2)
    line = scene.draw_line(pts[0], pts[1], extend=extend, color="#A8DADC")
    return line


# ---------------------------------------------------------------------------
# Angle bisector (Elements I.9)
# ---------------------------------------------------------------------------


def angle_bisector(scene, vertex, ray1, ray2, *, extend: float = 0.9):
    """Bisect the angle formed by rays ``vertex->ray1`` and ``vertex->ray2``.

    Returns ``(line, q)`` where ``q`` is the constructed point on the
    bisector.
    """
    v, r1, r2 = geo.P(vertex), geo.P(ray1), geo.P(ray2)
    r_arc = min(geo.dist(v, r1), geo.dist(v, r2)) * 0.6
    scene.draw_circle(v, radius=r_arc)
    x = geo.line_circle_intersection(v, r1, v, r_arc)
    y = geo.line_circle_intersection(v, r2, v, r_arc)
    # Pick the intersections lying on the rays (not opposite rays).
    xpt = _on_ray(v, r1, x)
    ypt = _on_ray(v, r2, y)
    r2c = max(geo.dist(xpt, ypt) * 1.05, r_arc)
    scene.draw_circle(xpt, radius=r2c)
    scene.draw_circle(ypt, radius=r2c)
    pts = geo.circle_circle_intersection(xpt, r2c, ypt, r2c)
    # Choose the intersection away from the vertex.
    q = max(pts, key=lambda z: geo.dist(z, v))
    qm = scene.add_point(q)
    line = scene.draw_line(v, q, extend=extend, color="#A8DADC")
    return line, qm


def _on_ray(v, ray_point, candidates):
    direction = (ray_point - v)[:2]
    best, best_dot = None, -np.inf
    for c in candidates:
        d = (c - v)[:2]
        score = float(np.dot(d, direction))
        if score > best_dot:
            best, best_dot = c, score
    return best


# ---------------------------------------------------------------------------
# Parallel line through a point (by two perpendiculars)
# ---------------------------------------------------------------------------


def parallel_through(scene, p, l1, l2, *, extend: float = 0.8):
    """Construct a line through ``p`` parallel to line ``l1-l2``.

    Uses two successive perpendiculars.  Returns the parallel line.
    """
    p = geo.P(p)
    perp = perpendicular_through(scene, p, l1, l2, extend=extend)
    s, e = perp.get_start(), perp.get_end()
    parallel = perpendicular_at(scene, p, s, e, extend=extend)
    return parallel


# ---------------------------------------------------------------------------
# Regular hexagon inscribed in a circle (Elements IV.15)
# ---------------------------------------------------------------------------


def regular_hexagon(scene, center, v0, *, draw_circumcircle: bool = True,
                    label_vertices: bool = False, color=RESULT_COLOR):
    """Inscribe a regular hexagon in the circle centered at ``center`` through
    ``v0``.

    Returns ``(vertices, edges)``.
    """
    center, v0 = geo.P(center), geo.P(v0)
    r = geo.dist(center, v0)
    if draw_circumcircle:
        scene.draw_circle(center, radius=r, color="#6C7A89", stroke_width=2)

    verts = [v0]
    prev2 = None
    current = v0
    for i in range(1, 6):
        hits = geo.circle_circle_intersection(center, r, current, r)
        # One intersection is the previous vertex (two steps back for i>1);
        # keep marching forward.
        nxt = None
        for h in hits:
            if prev2 is not None and geo.dist(h, prev2) < 1e-5:
                continue
            nxt = h
        if nxt is None:
            nxt = hits[0]
        # Sweep a short arc around `current` where the new vertex appears.
        ang = geo.angle_of(current, nxt)
        scene.draw_arc(
            current, r, start_angle=ang - 0.55, sweep_angle=1.1,
            color=CONSTRUCTION_COLOR, stroke_width=2,
        )
        label = chr(ord("B") + i - 1) if label_vertices else None
        verts.append(scene.add_point(nxt, label))
        prev2, current = current, nxt

    # Draw the six sides.
    edges = []
    pts = [geo.P(v) for v in verts]
    for i in range(6):
        edges.append(
            scene.draw_segment(
                pts[i], pts[(i + 1) % 6], color=color, run_time=0.6
            )
        )
    return verts, edges


# ---------------------------------------------------------------------------
# Regular heptadecagon — Richmond's construction (1893), after Gauss (1796)
# ---------------------------------------------------------------------------


def _ang(p):
    p = geo.P(p)
    return float(np.arctan2(p[1], p[0]))


def _pick_between(points, lo, hi):
    """Point whose polar angle lies in the angular interval (lo, hi)."""
    lo, hi = _ang(lo), _ang(hi)
    if lo > hi:
        lo, hi = hi, lo
    for p in points:
        a = _ang(p)
        if lo - 1e-6 < a < hi + 1e-6:
            return geo.P(p)
    raise ValueError("No point lies in the requested arc")


def _step_vertex(scene, center, R, chord, prev2, current, label=None):
    """March one vertex: circle centered at `current` (radius chord) meets the
    main circle at the next vertex; sweep a short arc and mark it."""
    hits = geo.circle_circle_intersection(center, R, current, chord)
    nxt = None
    for h in hits:
        if prev2 is not None and geo.dist(h, prev2) < 1e-5:
            continue
        nxt = h
    if nxt is None:
        nxt = hits[0]
    ang = geo.angle_of(current, nxt)
    scene.draw_arc(
        current, chord, start_angle=ang - 0.45, sweep_angle=0.9,
        color=CONSTRUCTION_COLOR, stroke_width=2,
    )
    pt = scene.add_point(nxt, label, radius=0.035)
    return current, geo.P(pt)


def heptadecagon(scene, center, v0, *, label_helpers=True,
                 label_key_vertices=False, color=RESULT_COLOR):
    """Inscribe a regular 17-gon in the circle centered at ``center`` through
    ``v0``, using Richmond's (1893) straightedge-and-compass construction.

    Steps: quarter a radius; quarter an angle; lay off 45°; use the circle on
    the resulting diameter and a circle through its intersection point to
    locate vertices V3 and V5; V4 is the arc midpoint; the chord V3V4 is then
    stepped around the circle to yield all 17 vertices.

    Returns ``(vertices, edges)`` where ``vertices`` maps index -> point.
    """
    O = geo.P(center)
    V = geo.P(v0)
    R = geo.dist(O, V)
    A = geo.rotate_around(O, V, PI / 2)          # quadrant point
    Aopp = geo.rotate_around(O, V, -PI / 2)
    Vopp = geo.rotate_around(O, V, PI)

    h = lambda s: s if label_helpers else None
    kv = lambda s: s if label_key_vertices else None

    def hide(*ms):
        """Move intermediate helper objects into the construction group."""
        for m in ms:
            if m is None:
                continue
            if m in scene.mobjects:
                scene.remove(m)
            scene.construction_mobjects.add(m)

    main = scene.draw_circle(O, radius=R, color="#6C7A89", stroke_width=2)
    # Reference diameters (construction lines).
    diam_h = scene.draw_line(Vopp, V, extend=0, color="#5D6D7E", stroke_width=1)
    diam_v = scene.draw_line(Aopp, A, extend=0, color="#5D6D7E", stroke_width=1)
    hide(diam_h, diam_v)

    # --- B: quarter point of radius OA (two successive bisections) --------
    m_half, l_h = perpendicular_bisector(scene, O, A)
    b_coord, l_h2 = perpendicular_bisector(scene, O, m_half)
    hide(l_h, l_h2)
    B = scene.add_point(b_coord, h("B"))

    # --- C: ray making 1/4 of angle OBV, meets horizontal diameter -------
    l_a1, q_half = scene.angle_bisector(B, O, V, extend=0.6)
    l_quarter, q_a2 = scene.angle_bisector(B, O, q_half, extend=0.6)
    hide(l_a1, q_half, l_quarter, q_a2)
    c_coord = scene.intersections_of(l_quarter, diam_h)[0]
    C = scene.add_point(c_coord, h("C"))

    # --- D: 45 degrees from BC at B, meets horizontal diameter ----------
    perp_bc = scene.perpendicular_at(B, B, C, extend=0.6)
    hide(perp_bc)
    bc_ang = geo.angle_of(B, C)
    target_ang = bc_ang - PI / 4
    ends = [perp_bc.get_start(), perp_bc.get_end()]
    Hpt = min(ends, key=lambda e: abs(_wrap(_ang(e) - target_ang)))
    l_45, q_45 = scene.angle_bisector(B, Hpt, C, extend=0.6)
    hide(l_45, q_45)
    d_coord = scene.intersections_of(l_45, diam_h)[0]
    D = scene.add_point(d_coord, h("D"))

    # --- E: circle on DV (as diameter) meets vertical diameter ----------
    dv_mid = geo.midpoint(D, V)
    dv_r = geo.dist(D, V) / 2.0
    cir_dv = scene.draw_circle(dv_mid, radius=dv_r)
    e_hits = scene.intersections_of(cir_dv, diam_v)
    e_coord = max(e_hits, key=lambda p: p[1])   # upper intersection, near B
    E = scene.add_point(e_coord, h("E"))

    # --- F, G: circle centered C through E meets horizontal diameter ----
    cir_ce = scene.draw_circle(C, through=E)
    fg = scene.intersections_of(cir_ce, diam_h)
    g_coord = max(fg, key=lambda p: p[0])
    f_coord = min(fg, key=lambda p: p[0])
    G = scene.add_point(g_coord, h("G"))
    F = scene.add_point(f_coord, h("F"))

    # --- V3, V5: perpendiculars at G, F meet the main circle -----------
    perp_g = scene.perpendicular_at(G, O, V, extend=0.3)
    hide(perp_g)
    v3_coord = _pick_between(scene.intersections_of(perp_g, main), A, V)
    V3 = scene.add_point(v3_coord, kv("V3"), color="#E84A5F")
    perp_f = scene.perpendicular_at(F, O, V, extend=0.3)
    hide(perp_f)
    v5_hits = scene.intersections_of(perp_f, main)
    v5_coord = max(v5_hits, key=lambda p: p[1])
    V5 = scene.add_point(v5_coord, kv("V5"), color="#E84A5F")

    # --- V4: bisect angle V3 O V5, meet main circle ---------------------
    l_v4, q_v4 = scene.angle_bisector(O, V3, V5, extend=0.3)
    hide(l_v4, q_v4)
    v4_coord = _pick_between(scene.intersections_of(l_v4, main), V3, V5)
    V4 = scene.add_point(v4_coord, kv("V4"), color="#E84A5F")

    chord = geo.dist(V3, V4)
    verts = {0: V, 3: geo.P(V3), 4: geo.P(V4), 5: geo.P(V5)}

    # --- March backward V3 -> V2 -> V1 ----------------------------------
    prev2, cur = geo.P(V4), geo.P(V3)
    for idx in (2, 1):
        prev2, cur = _step_vertex(scene, O, R, chord, prev2, cur,
                                  kv(f"V{idx}"))
        verts[idx] = cur

    # --- March forward V5 -> V6 ... V16 ---------------------------------
    prev2, cur = geo.P(V4), geo.P(V5)
    for idx in range(6, 17):
        prev2, cur = _step_vertex(scene, O, R, chord, prev2, cur,
                                  kv(f"V{idx}"))
        verts[idx] = cur

    # The Richmond helper points have served their purpose; remove them
    # with the rest of the construction, leaving only the polygon.
    hide(B, C, D, E, F, G)

    # --- Draw the 17 sides in cyclic order ------------------------------
    edges = []
    for i in range(17):
        edges.append(
            scene.draw_segment(
                verts[i], verts[(i + 1) % 17], color=color, run_time=0.4
            )
        )
    return verts, edges


def _wrap(a):
    """Wrap an angle difference to (-pi, pi)."""
    return (a + PI) % (2 * PI) - PI
