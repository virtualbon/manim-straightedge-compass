"""Unit tests for the pure-geometry routines."""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manim_sc import geometry as geo  # noqa: E402


def assert_close(a, b, tol=1e-9):
    assert abs(a - b) < tol, f"{a} != {b}"


def test_line_line():
    p = geo.line_line_intersection([0, 0], [2, 2], [0, 2], [2, 0])
    assert np.allclose(p[:2], [1, 1])
    assert geo.line_line_intersection([0, 0], [1, 1], [0, 1], [1, 2]) is None


def test_line_circle():
    # Horizontal line y = 0 through unit circle centered at origin.
    hits = geo.line_circle_intersection([-5, 0], [5, 0], [0, 0], 1)
    assert len(hits) == 2
    assert np.allclose(hits[0][:2], [-1, 0])
    assert np.allclose(hits[1][:2], [1, 0])
    # Tangent.
    hits = geo.line_circle_intersection([-5, 1], [5, 1], [0, 0], 1)
    assert len(hits) == 1
    assert np.allclose(hits[0][:2], [0, 1])
    # Miss.
    assert geo.line_circle_intersection([-5, 2], [5, 2], [0, 0], 1) == []


def test_circle_circle():
    # Two unit circles centered 1 unit apart: equilateral geometry.
    hits = geo.circle_circle_intersection([0, 0], 1, [1, 0], 1)
    assert len(hits) == 2
    assert np.allclose(hits[0][:2], [0.5, np.sqrt(3) / 2])
    assert np.allclose(hits[1][:2], [0.5, -np.sqrt(3) / 2])
    # Touching externally.
    hits = geo.circle_circle_intersection([0, 0], 1, [2, 0], 1)
    assert len(hits) == 1
    # Disjoint / concentric.
    assert geo.circle_circle_intersection([0, 0], 1, [5, 0], 1) == []
    assert geo.circle_circle_intersection([0, 0], 1, [0, 0], 2) == []


def test_midpoint_distance():
    assert_close(geo.dist([0, 0], [3, 4]), 5)
    m = geo.midpoint([0, 0], [4, 2])
    assert np.allclose(m[:2], [2, 1])


def test_rotate():
    r = geo.rotate_around([0, 0], [1, 0], np.pi / 2)
    assert np.allclose(r[:2], [0, 1], atol=1e-10)


def test_circle_through():
    center, r = geo.circle_through([1, 0], [0, 1], [-1, 0])
    assert np.allclose(center[:2], [0, 0])
    assert_close(r, 1)
    assert geo.circle_through([0, 0], [1, 1], [2, 2]) is None


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(fns)} geometry tests passed.")
