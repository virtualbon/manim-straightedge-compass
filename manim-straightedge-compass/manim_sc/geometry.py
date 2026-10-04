"""Pure planar-geometry helpers used by the straightedge-and-compass plugin.

Points are plain ``numpy`` arrays of shape ``(3,)`` (Manim scene coordinates,
``z = 0``).  Every routine is exact up to floating-point tolerance and has no
dependency on Manim, so it can be unit-tested independently.
"""

from __future__ import annotations

import numpy as np

EPS = 1e-7


def P(x, y: float | None = None) -> np.ndarray:
    """Coerce a wide range of point representations to a 3-vector.

    Accepts ``(x, y)`` numbers, a 2-/3-tuple/list, a numpy array, or any
    object exposing a ``.pt`` attribute (such as :class:`MarkedPoint`).
    """
    if y is not None:
        return np.array([float(x), float(y), 0.0])
    if hasattr(x, "pt"):
        return np.asarray(x.pt, dtype=float)
    arr = np.asarray(x, dtype=float).reshape(-1)
    if arr.shape[0] == 2:
        return np.array([arr[0], arr[1], 0.0])
    return np.array([arr[0], arr[1], 0.0])


def dist(a, b) -> float:
    """Euclidean distance between two points."""
    return float(np.linalg.norm(P(a) - P(b)))


def midpoint(a, b) -> np.ndarray:
    return (P(a) + P(b)) / 2.0


def angle_of(a, b) -> float:
    """Angle of the directed line ``a -> b``, in radians."""
    d = P(b) - P(a)
    return float(np.arctan2(d[1], d[0]))


def rotate_around(center, point, angle: float) -> np.ndarray:
    """Rotate ``point`` about ``center`` by ``angle`` radians."""
    c, p = P(center), P(point)
    c_a, s_a = np.cos(angle), np.sin(angle)
    rot = np.array([[c_a, -s_a], [s_a, c_a]])
    rel = rot @ (p[:2] - c[:2])
    return np.array([c[0] + rel[0], c[1] + rel[1], 0.0])


def point_on_line(p1, p2, t: float) -> np.ndarray:
    """Point ``p1 + t * (p2 - p1)``."""
    return P(p1) + t * (P(p2) - P(p1))


# ---------------------------------------------------------------------------
# Intersections
# ---------------------------------------------------------------------------


def line_line_intersection(l1a, l1b, l2a, l2b):
    """Intersection of two (infinite) lines.

    Returns a point array, or ``None`` when the lines are parallel.
    """
    p, r = P(l1a), P(l1b) - P(l1a)
    q, s = P(l2a), P(l2b) - P(l2a)
    rxs = r[0] * s[1] - r[1] * s[0]
    if abs(rxs) < EPS:
        return None
    qp = q - p
    t = (qp[0] * s[1] - qp[1] * s[0]) / rxs
    return p + t * r


def line_circle_intersection(p1, p2, center, radius: float):
    """Intersections of the infinite line through ``p1, p2`` with a circle.

    Returns a list of 0, 1 or 2 point arrays.
    """
    p, d = P(p1), P(p2) - P(p1)
    norm = np.linalg.norm(d[:2])
    if norm < EPS:
        return []
    d = d / norm
    f = p - P(center)
    b = 2.0 * float(np.dot(f[:2], d[:2]))
    c = float(np.dot(f[:2], f[:2])) - radius * radius
    disc = b * b - 4.0 * c
    if disc < -EPS:
        return []
    if disc < 0:
        disc = 0.0
    root = np.sqrt(disc)
    t1 = (-b - root) / 2.0
    t2 = (-b + root) / 2.0
    out = [p + t1 * d]
    if root > EPS:
        out.append(p + t2 * d)
    return out


def circle_circle_intersection(c1, r1: float, c2, r2: float):
    """Intersections of two circles.

    Returns a list of 0, 1 or 2 point arrays.  Points are returned with the
    point on the left of the directed line ``c1 -> c2`` first.
    """
    a, b = P(c1), P(c2)
    d_vec = b - a
    d = float(np.linalg.norm(d_vec[:2]))
    if d < EPS:
        # Concentric circles.
        return []
    if d > r1 + r2 + EPS or d < abs(r1 - r2) - EPS:
        return []
    x = (d * d + r1 * r1 - r2 * r2) / (2.0 * d)
    y2 = r1 * r1 - x * x
    if y2 < 0:
        y2 = 0.0
    y = np.sqrt(y2)
    u = d_vec / d
    v = np.array([-u[1], u[0], 0.0])
    base = a + x * u
    out = [base + y * v]
    if y > EPS:
        out.append(base - y * v)
    return out


def circle_through(p1, p2, p3):
    """Center and radius of the circle through three points.

    Returns ``(center, radius)`` or ``None`` if the points are collinear.
    """
    a, b, c = P(p1), P(p2), P(p3)
    d = 2.0 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
    if abs(d) < EPS:
        return None
    a2, b2, c2 = a[0] ** 2 + a[1] ** 2, b[0] ** 2 + b[1] ** 2, c[0] ** 2 + c[1] ** 2
    cx = (a2 * (b[1] - c[1]) + b2 * (c[1] - a[1]) + c2 * (a[1] - b[1])) / d
    cy = (a2 * (c[0] - b[0]) + b2 * (a[0] - c[0]) + c2 * (b[0] - a[0])) / d
    center = np.array([cx, cy, 0.0])
    return center, dist(center, a)
