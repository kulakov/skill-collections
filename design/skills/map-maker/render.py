#!/usr/bin/env python3
"""
pycairo rendering engine для создания векторных карт из топологии.

Поддерживает стили:
- british-os-19c (default) — гравюра, сепия, штриховка
- fantasy — castle icons, volumetric mountains
- modern — минимализм, чистые линии
- tolkien — runic fonts, aged paper
"""

import cairo
import json
import math
import numpy as np
import sys
import os


def load_style(style_name="british-os-19c"):
    """Загружает стилевой пресет из JSON."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    style_path = os.path.join(script_dir, "styles", f"{style_name}.json")

    if not os.path.exists(style_path):
        print(f"Warning: Style '{style_name}' not found, using default british-os-19c")
        style_name = "british-os-19c"
        style_path = os.path.join(script_dir, "styles", f"{style_name}.json")

    with open(style_path, 'r') as f:
        style = json.load(f)

    # Конвертация RGB 0-255 → 0-1 для cairo
    for key in ["paper", "ink", "ink_light", "water", "water_dark", "mountain", "road", "forest"]:
        if key in style and isinstance(style[key], list):
            style[key] = tuple(c / 255 for c in style[key])

    return style


def to_px(point, viewport, size):
    """Нормализованные координаты → пиксели."""
    vx, vy, vw, vh = viewport
    x = (point[0] - vx) / vw * size[0]
    y = (point[1] - vy) / vh * size[1]
    return (x, y)


def catmull_rom_to_bezier(p0, p1, p2, p3, alpha=0.5):
    """Конвертирует сегмент Catmull-Rom в кубический Безье для Cairo curve_to."""
    d1 = math.sqrt((p1[0] - p0[0])**2 + (p1[1] - p0[1])**2)
    d2 = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    d3 = math.sqrt((p3[0] - p2[0])**2 + (p3[1] - p2[1])**2)

    d1a = max(d1**alpha, 1e-6)
    d2a = max(d2**alpha, 1e-6)
    d3a = max(d3**alpha, 1e-6)

    b1x = (d1a**2 * p2[0] - d2a**2 * p0[0] + (2*d1a**2 + 3*d1a*d2a + d2a**2) * p1[0]) / (3*d1a*(d1a+d2a))
    b1y = (d1a**2 * p2[1] - d2a**2 * p0[1] + (2*d1a**2 + 3*d1a*d2a + d2a**2) * p1[1]) / (3*d1a*(d1a+d2a))

    b2x = (d3a**2 * p1[0] - d2a**2 * p3[0] + (2*d3a**2 + 3*d3a*d2a + d2a**2) * p2[0]) / (3*d3a*(d2a+d3a))
    b2y = (d3a**2 * p1[1] - d2a**2 * p3[1] + (2*d3a**2 + 3*d3a*d2a + d2a**2) * p2[1]) / (3*d3a*(d2a+d3a))

    return (b1x, b1y), (b2x, b2y)


def cairo_smooth_path(ctx, points, closed=True):
    """Строит гладкий путь из точек через кривые Безье (Catmull-Rom → cubic Bezier)."""
    n = len(points)
    if n < 3:
        if n >= 1:
            ctx.move_to(*points[0])
            for p in points[1:]:
                ctx.line_to(*p)
        return

    ctx.move_to(*points[0])
    for i in range(n):
        p0 = points[(i - 1) % n]
        p1 = points[i]
        p2 = points[(i + 1) % n]
        p3 = points[(i + 2) % n]

        cp1, cp2 = catmull_rom_to_bezier(p0, p1, p2, p3)
        ctx.curve_to(cp1[0], cp1[1], cp2[0], cp2[1], p2[0], p2[1])

    if closed:
        ctx.close_path()


def draw_water_body(ctx, points, viewport, size, style):
    """Рисует водоём: заливка + волнистая штриховка + контур."""
    px_points = [to_px(p, viewport, size) for p in points]

    # Заливка
    ctx.save()
    cairo_smooth_path(ctx, px_points, closed=True)
    ctx.set_source_rgb(*style["water"])
    ctx.fill_preserve()

    # Штриховка внутри (clip)
    if style.get("hachures", True):
        ctx.clip()
        xs = [p[0] for p in px_points]
        ys = [p[1] for p in px_points]
        min_y, max_y = int(min(ys)) - 5, int(max(ys)) + 5
        min_x, max_x = int(min(xs)) - 5, int(max(xs)) + 5

        density = max(4, int(7 * viewport[2]))
        ctx.set_source_rgb(*style["water_dark"])
        ctx.set_line_width(0.5)

        for y in range(min_y, max_y, density):
            ctx.move_to(min_x, y)
            for x in range(min_x, max_x, 8):
                wave = math.sin(x * 0.015 + y * 0.08) * 1.8
                ctx.line_to(x, y + wave)
            ctx.stroke()

    ctx.restore()

    # Контур
    cairo_smooth_path(ctx, px_points, closed=True)
    ctx.set_source_rgb(*style["ink"])
    ctx.set_line_width(1.8)
    ctx.stroke()


def draw_island(ctx, points, viewport, size, style):
    """Рисует остров: заливка бумагой + контур."""
    px_points = [to_px(p, viewport, size) for p in points]

    cairo_smooth_path(ctx, px_points, closed=True)
    ctx.set_source_rgb(*style["paper"])
    ctx.fill_preserve()
    ctx.set_source_rgb(*style["ink"])
    ctx.set_line_width(1.0)
    ctx.stroke()


def render_map(topology_path, style_name="british-os-19c", viewport=(0, 0, 1, 1), size=(2048, 2048), title="MAP"):
    """
    Рендерит карту из топологии.

    Args:
        topology_path: путь к JSON с извлечёнными координатами
        style_name: название стилевого пресета
        viewport: (x, y, width, height) в нормализованных координатах
        size: (width, height) в пикселях
        title: заголовок карты

    Returns:
        cairo.ImageSurface
    """
    # Загрузка топологии
    with open(topology_path, 'r') as f:
        topology = json.load(f)

    # Загрузка стиля
    style = load_style(style_name)

    # Создание surface
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, size[0], size[1])
    ctx = cairo.Context(surface)
    ctx.set_antialias(cairo.ANTIALIAS_BEST)

    # Фон (бумага)
    ctx.set_source_rgb(*style["paper"])
    ctx.rectangle(0, 0, size[0], size[1])
    ctx.fill()

    # 1. Водоёмы (заливка + штриховка + контур)
    for name, feature in topology.items():
        if not feature["is_island"]:
            points = [tuple(p) for p in feature["points"]]
            draw_water_body(ctx, points, viewport, size, style)

    # 2. Острова
    for name, feature in topology.items():
        if feature["is_island"]:
            points = [tuple(p) for p in feature["points"]]
            draw_island(ctx, points, viewport, size, style)

    # TODO: 3. Горы, леса, реки, дороги, города (если будут добавлены в topology)

    # Декорация
    if style.get("compass_rose", True):
        draw_compass_rose(ctx, size[0] - 50, 50, style)

    if style.get("scale_bar", True):
        draw_scale_bar(ctx, size, style)

    if style.get("cartouche", True):
        draw_title(ctx, title, size, style)

    if style.get("decorative_border", False):
        draw_frame(ctx, size, style)

    return surface


def draw_compass_rose(ctx, cx, cy, style, r=30):
    """Компасная роза."""
    ctx.set_source_rgb(*style["ink"])
    ctx.set_line_width(1.0)

    # Перекрестие
    ctx.move_to(cx, cy - r)
    ctx.line_to(cx, cy + r)
    ctx.stroke()
    ctx.move_to(cx - r, cy)
    ctx.line_to(cx + r, cy)
    ctx.stroke()

    # Стрелка N (треугольник)
    ctx.move_to(cx, cy - r)
    ctx.line_to(cx - 4, cy - r + 10)
    ctx.line_to(cx + 4, cy - r + 10)
    ctx.close_path()
    ctx.fill()

    # Буквы
    ctx.select_font_face(style["font_family"], cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(12)
    ctx.move_to(cx - 3, cy - r - 6)
    ctx.show_text("N")


def draw_scale_bar(ctx, size, style):
    """Масштабная линейка."""
    y = size[1] - 30
    x_start = size[0] - 180
    bar_len = 150

    ctx.set_source_rgb(*style["ink"])
    ctx.set_line_width(2.0)
    ctx.move_to(x_start, y)
    ctx.line_to(x_start + bar_len, y)
    ctx.stroke()

    ctx.set_line_width(1.0)
    for x in [x_start, x_start + bar_len // 2, x_start + bar_len]:
        ctx.move_to(x, y - 5)
        ctx.line_to(x, y + 5)
        ctx.stroke()


def draw_title(ctx, text, size, style):
    """Заголовок в картуше."""
    font_size = max(16, size[0] // 40)
    ctx.select_font_face(style["font_family"], cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(font_size)

    extents = ctx.text_extents(text)
    tw = extents.width
    th = extents.height

    x = (size[0] - tw) / 2
    y = 22 + th

    pad = 10
    # Двойная рамка картуша
    ctx.set_source_rgb(*style["paper"])
    ctx.rectangle(x - pad * 2, y - th - pad, tw + pad * 4, th + pad * 2)
    ctx.fill()

    ctx.set_source_rgb(*style["ink"])
    ctx.set_line_width(2.0)
    ctx.rectangle(x - pad * 2, y - th - pad, tw + pad * 4, th + pad * 2)
    ctx.stroke()

    ctx.move_to(x, y)
    ctx.show_text(text)


def draw_frame(ctx, size, style):
    """Двойная рамка."""
    ctx.set_source_rgb(*style["ink"])
    ctx.set_line_width(2.0)
    ctx.rectangle(10, 10, size[0] - 20, size[1] - 20)
    ctx.stroke()

    ink_light = style.get("ink_light", style["ink"])
    ctx.set_source_rgb(*ink_light)
    ctx.set_line_width(0.8)
    ctx.rectangle(15, 15, size[0] - 30, size[1] - 30)
    ctx.stroke()


def main():
    if len(sys.argv) < 2:
        print("Usage: python render.py <topology.json> [style] [output.png]")
        print("Styles: british-os-19c (default), fantasy, modern, tolkien")
        sys.exit(1)

    topology_path = sys.argv[1]
    style_name = sys.argv[2] if len(sys.argv) > 2 else "british-os-19c"
    output_path = sys.argv[3] if len(sys.argv) > 3 else "map_world.png"

    print(f"Rendering map from {topology_path}...")
    print(f"Style: {style_name}")

    # Рендеринг
    surface = render_map(topology_path, style_name=style_name, title="WORLD MAP")

    # Сохранение
    surface.write_to_png(output_path)
    print(f"✓ Map saved: {output_path}")


if __name__ == "__main__":
    main()
