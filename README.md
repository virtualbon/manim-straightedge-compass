# manim-sc — Straightedge & Compass Plugin for Manim

A plugin for [Manim Community](https://www.manim.community/) that animates
classical **straightedge-and-compass** (ruler and compass) constructions.
A translucent ruler actually slides into place before every line is drawn,
and a pair of compass legs sweeps every circle and arc in real time.

It follows Euclid's *Elements*: every result is produced from points,
segments, circles and their intersections — nothing is "magically" placed.

## Features

- **Animated tools** — `Straightedge` (graded translucent ruler) and
  `Compass` (two legs, hinge, needle & pencil tips).
- **Exact geometry engine** (`manim_sc.geometry`) — line–line,
  line–circle and circle–circle intersections, tested independently.
- **Ready-made constructions**, fully animated:
  | Construction | Euclid ref. | Method |
  |---|---|---|
  | Equilateral triangle | I.1 | `equilateral_triangle(a, b)` |
  | Perpendicular bisector | I.10 | `perpendicular_bisector(a, b)` |
  | Midpoint of a segment | I.10 | `midpoint(a, b)` |
  | Perpendicular at a point on a line | I.11 | `perpendicular_at(p, l1, l2)` |
  | Perpendicular through an external point | I.12 | `perpendicular_through(p, l1, l2)` |
  | Angle bisector | I.9 | `angle_bisector(v, ray1, ray2)` |
  | Parallel line through a point | I.31 | `parallel_through(p, l1, l2)` |
  | Regular hexagon in a circle | IV.15 | `regular_hexagon(center, v0)` |
  | Regular heptadecagon (Richmond, after Gauss) | — | `heptadecagon(center, v0)` |
- **Bookkeeping** — auxiliary objects are tracked automatically and removed
  together with `fade_construction()`; `emphasize()` highlights results.
- **No LaTeX required** — labels use `Text`, so the plugin renders with a
  bare Manim install.

## Installation

```bash
# 1. Install Manim (system deps: ffmpeg; see Manim docs for your OS)
pip install manim

# 2. Install the plugin (from the project root)
pip install -e .
```

## Quick start

```python
from manim import LEFT, RIGHT
from manim_sc import StraightedgeCompassScene


class Equilateral(StraightedgeCompassScene):
    def construct(self):
        a = self.add_point(2 * LEFT, "A")
        b = self.add_point(2 * RIGHT, "B")

        _, _, c, edges = self.equilateral_triangle(a, b)

        self.wait(0.5)
        self.fade_construction()   # remove the two helper circles
        self.emphasize(*edges)     # flash the finished triangle
```

Render it:

```bash
manim -pql examples/01_equilateral.py EquilateralTriangleDemo
```

## API reference

All methods live on `StraightedgeCompassScene` (a subclass of `manim.Scene`).
Points may be passed as coordinate arrays, tuples, or `MarkedPoint` objects.

### Points

```python
pt = self.add_point([1.0, 2.0], "P")          # grows in, labelled
pt = self.add_point(3 * RIGHT, animate=False) # static
```

### Straightedge

```python
seg = self.draw_segment(a, b)                       # finite segment
ln  = self.draw_line(a, b, extend=1.0)              # extended line
```

### Compass

```python
cir = self.draw_circle(center, through=a)           # full circle
cir = self.draw_circle(center, radius=1.5, dashed=True)
arc = self.draw_arc(center, radius, start_angle, sweep_angle)
```

### Intersections

```python
pts = self.intersections_of(circle1, circle2)       # raw point arrays
x   = self.mark_intersection(line, circle, which=0, label="X")
```

`which` selects among up to two intersections. Works for line–line,
line–circle and circle–circle pairs.

### Cleanup / presentation

```python
self.fade_construction()                 # fade all helpers at once
self.fade_construction(some_extra_obj)   # plus arbitrary objects
self.emphasize(obj1, obj2)               # temporary gold highlight
```

Anything drawn with `construction=True` (the default for circles/arcs and
for construction helpers) is collected; result segments are not.

### Low-level objects

```python
from manim_sc import Straightedge, Compass, MarkedPoint
from manim_sc import geometry
```

- `geometry.P(x)` — coerce anything to a 3-vector.
- `geometry.dist`, `geometry.midpoint`, `geometry.angle_of`,
  `geometry.rotate_around`.
- `geometry.line_line_intersection`,
  `geometry.line_circle_intersection`,
  `geometry.circle_circle_intersection`,
  `geometry.circle_through`.

## Examples

Five worked scenes live in [`examples/`](examples):

```bash
manim -pql examples/01_equilateral.py   EquilateralTriangleDemo
manim -pql examples/02_midpoint.py      MidpointDemo
manim -pql examples/03_hexagon.py       HexagonDemo
manim -pql examples/04_angle_bisector.py AngleBisectorDemo
manim -pql examples/05_parallel.py      ParallelLineDemo
manim -pql examples/06_heptadecagon.py  HeptadecagonDemo
```

The heptadecagon demo runs about 2.5 minutes: Richmond's 1893 construction,
which realizes Gauss's 1796 result that the regular 17-gon is constructible
(17 = 2^4 + 1 is a Fermat prime).

Use `-pqh` (high quality) or `-pqh --fps 60` for final videos.

## Writing your own construction

1. Place points with `add_point`.
2. Draw lines/circles only via `draw_segment`, `draw_line`,
   `draw_circle`, `draw_arc` — each plays the tool animation and registers
   geometry for intersection solving.
3. Find new points with `mark_intersection`.
4. Keep helpers as construction objects (default); call
   `fade_construction()` when the proof figure is complete.

## Tests

```bash
python tests/test_geometry.py
```

## License

MIT — see [LICENSE](LICENSE).
