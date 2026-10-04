"""manim-sc: a straightedge-and-compass construction plugin for Manim.

Example
-------
.. code-block:: python

    from manim import *
    from manim_sc import StraightedgeCompassScene

    class Equilateral(StraightedgeCompassScene):
        def construct(self):
            A = self.add_point(2 * LEFT, "A")
            B = self.add_point(2 * RIGHT, "B")
            self.equilateral_triangle(A, B)
            self.fade_construction()
"""

from __future__ import annotations

from . import geometry
from .marks import MarkedPoint
from .tools import (
    Straightedge,
    Compass,
    make_compass_at,
    static_arc,
    RULER_COLOR,
    COMPASS_COLOR,
    CONSTRUCTION_COLOR,
    RESULT_COLOR,
)
from .scene import StraightedgeCompassScene
from . import constructions

__version__ = "0.1.0"

__all__ = [
    "geometry",
    "MarkedPoint",
    "Straightedge",
    "Compass",
    "make_compass_at",
    "static_arc",
    "StraightedgeCompassScene",
    "constructions",
    "RULER_COLOR",
    "COMPASS_COLOR",
    "CONSTRUCTION_COLOR",
    "RESULT_COLOR",
    "__version__",
]


# Bind every construction as a convenience method on the scene class.
def _bind_as_method(fn):
    def method(self, *args, **kwargs):
        return fn(self, *args, **kwargs)

    method.__name__ = fn.__name__
    method.__doc__ = fn.__doc__
    return method


for _name in dir(constructions):
    if _name.startswith("_"):
        continue
    _fn = getattr(constructions, _name)
    if callable(_fn):
        setattr(StraightedgeCompassScene, _name, _bind_as_method(_fn))
