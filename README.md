# manim-straightedge-compass

一个用于 [Manim](https://www.manim.community/) 的**尺规作图动画插件**：圆规会带着针尖与铅笔腿真实地旋转扫出圆弧，直尺会落到两点之间、铅笔沿尺边滑动画出直线。配合一组几何求交工具，可以用声明式的几行代码还原欧几里得式尺规作图。

- 圆规 `Compass`：金属双腿 + 红色针尖 + 黄色铅笔，绕针尖刚性旋转，弧与铅笔尖严格同步
- 直尺 `Straightedge`：半透明尺身、刻度、高亮刃边，自动对齐任意两点
- 几何工具：圆–圆、圆–直线、直线–直线求交，中点、角度、选点等
- 场景基类 `EuclidScene`：`mark_point / draw_circle / draw_arc / draw_segment` 四个方法完成大部分作图
- 6 个经典示例：等边三角形、垂直平分线（中点）、角平分线、过点作垂线、圆内接正六边形、复制线段
- 进阶示例：**正十七边形**（Richmond 尺规作法，辅助线分批淡出）

## 安装

```bash
# 需要先具备 manim 的系统依赖（ffmpeg、LaTeX 等），见 https://docs.manim.community/
pip install manim

# 安装本插件（在项目根目录）
pip install -e .
```

不安装也可以使用：直接把 `manim_sc` 目录放进工程，或在示例脚本中
`sys.path.insert(0, <项目根目录>)`（示例文件已这样处理）。

## 快速开始

```python
from manim_sc import (
    EuclidScene, P,
    circle_circle_intersection, uppermost,
)

class EquilateralTriangle(EuclidScene):
    def construct(self):
        A, B = P(-1.5, -0.7), P(1.5, -0.7)
        r = 3.0                                   # 圆规张开的半径
        self.mark_point(A, "A")                   # 标注点
        self.mark_point(B, "B")
        self.draw_circle(A, radius=r)             # 圆规画圆
        self.draw_circle(B, radius=r)
        C = uppermost(circle_circle_intersection(A, r, B, r))
        self.mark_point(C, "C")
        self.draw_segment(A, B)                   # 直尺画线
        self.draw_segment(A, C)
        self.draw_segment(B, C)
        self.wait(1)
```

渲染：

```bash
manim -qm examples/equilateral_triangle.py EquilateralTriangle
```

## API 文档

### `EuclidScene` 场景基类

| 方法 | 说明 |
| --- | --- |
| `intro(title)` | 显示中文标题并缩到左上角 |
| `mark_point(p, label=None, direction=UP, color=..., radius=0.06)` | 在 `p` 处落下红点，可选 LaTeX 标签与标签方向 |
| `draw_circle(center, through=None, radius=None, color=CONSTRUCTION_COLOR, start_angle=0)` | 圆规画整圆；半径可直接给，或给圆周上一点 `through` 自动量取 |
| `draw_arc(center, radius, start_angle=0, angle=TAU, color=..., stroke_width=2, keep_compass=False)` | 圆规扫一段弧；`keep_compass=True` 时圆规不收走，便于保持张角搬到下一个圆心 |
| `draw_segment(p1, p2, color=RESULT_COLOR, stroke_width=4, keep_ruler=False)` | 直尺对齐 `p1p2`，铅笔从 `p1` 滑到 `p2` 画出线段；连续画多边形边时传 `keep_ruler=True`，最后调用 `retire_ruler()` 收尺 |
| `retire_ruler()` | 一组 `keep_ruler=True` 线段画完后把直尺移出画面 |

工具会自动从画面下方移入、作画、再移出；颜色常量 `CONSTRUCTION_COLOR`（蓝，辅助痕迹）、`CONSTRUCTION_GREEN`（绿，第二组痕迹）、`RESULT_COLOR`（黄，最终结果）、`RESULT_RED` 可直接导入。

### 几何工具（`manim_sc.geometry`，纯 numpy 计算，与渲染无关）

```python
P(x, y)                               # 构造点 (x, y, 0)
distance(a, b)；midpoint(a, b)；angle_of(a, b)；unit(v)；point_on(c, r, theta)
circle_circle_intersection(c1, r1, c2, r2)   # -> 0/1/2 个交点
circle_line_intersection(center, r, p1, p2)  # 圆与（无限长）直线的交点
line_line_intersection(p1, p2, p3, p4)       # 两直线交点或 None
uppermost / lowermost / leftmost / rightmost(points)   # 选点
other(two_points, given)             # 两点中不是 given 的另一个
```

### 工具 Mobject 与动画（可脱离基类自由编排）

```python
from manim_sc import Compass, CompassDrawArc, Straightedge, PencilTip, RulerDraw, Arc, Line, TAU

compass = Compass(radius=1.5, start_angle=0, center=P(0, 0))
compass.pose(center, radius, theta)          # 定位（可配合 .animate）
arc = Arc(radius=1.5, start_angle=0, angle=1e-6, arc_center=center)
self.play(CompassDrawArc(compass, arc, TAU)) # 边旋转边出弧

ruler = Straightedge()
ruler.pose(p1, p2)                            # 刃边对齐两点
line = Line(p1, p1)
tip = PencilTip(p1)
self.play(RulerDraw(line, tip, p1, p2))       # 铅笔滑过，线段生长
```

`Compass` 腿长、颜色，`Straightedge` 长度/宽度/填充透明度等都可在构造时调整
（见 `manim_sc/compass.py`、`manim_sc/straightedge.py` 顶部常量）。

## 示例

| 文件 | 内容 |
| --- | --- |
| `examples/equilateral_triangle.py` | 等边三角形（《原本》I.1） |
| `examples/perpendicular_bisector.py` | 线段的垂直平分线与中点 |
| `examples/angle_bisector.py` | 角平分线 |
| `examples/perpendicular_from_point.py` | 过直线外一点作垂线、垂足 |
| `examples/regular_hexagon.py` | 圆内接正六边形（边长 = 半径） |
| `examples/copy_segment.py` | 圆规保持张角，把线段长度搬到射线上 |
| `examples/heptadecagon.py` | 正十七边形（Richmond 作法）完整过程：垂直直径、J 点两次平分、两次角平分、45° 角的垂线+平分、两构造圆定出 P3/P4/P5，圆规绕圆截取全部顶点；每步的中间痕迹在完成使命后分批淡出 |

渲染全部示例：

```bash
for f in examples/*.py; do manim -qm "$f"; done
```

## 项目结构

```
manim-straightedge-compass/
├── manim_sc/
│   ├── __init__.py        # 公共导出
│   ├── geometry.py        # 纯几何：交点、选点、向量工具
│   ├── compass.py         # Compass 圆规 + CompassDrawArc 动画
│   ├── straightedge.py    # Straightedge 直尺 + PencilTip + RulerDraw
│   ├── marks.py           # MarkedPoint 点与标签
│   └── scene.py           # EuclidScene 高层场景基类
├── examples/              # 六个经典作图示例
└── demo/                  # 预渲染的 720p 演示视频
```

## 许可

MIT
