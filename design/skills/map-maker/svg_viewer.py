#!/usr/bin/env python3
"""
SVG viewer для векторных карт с pan/zoom через panzoom.js.
Простой и работающий интерактивный просмотр.
"""

import json
import sys


def topology_to_svg(topology_path, output_html="map_viewer.html", width=1200, height=1200):
    """
    Создаёт HTML с SVG и pan/zoom для интерактивного просмотра карты.

    Args:
        topology_path: путь к JSON с топологией
        output_html: путь для сохранения HTML
        width, height: размер viewport в пикселях
    """
    with open(topology_path, 'r') as f:
        topology = json.load(f)

    # Генерация SVG paths из топологии
    svg_paths = []

    for name, feature in topology.items():
        points = feature["points"]
        is_island = feature["is_island"]

        # Конвертация нормализованных координат в пиксели
        path_data = "M "
        for i, (x, y) in enumerate(points):
            px = x * width
            py = y * height
            if i == 0:
                path_data += f"{px:.2f},{py:.2f} "
            else:
                path_data += f"L {px:.2f},{py:.2f} "
        path_data += "Z"  # Замыкание пути

        # Стили
        if is_island:
            fill = "#f5e6d3"
            stroke = "#2a2a2e"
            fill_opacity = 0.9
        else:
            fill = "#3b82f6"
            stroke = "#2a2a2e"
            fill_opacity = 0.6

        svg_paths.append({
            "path": path_data,
            "fill": fill,
            "stroke": stroke,
            "fill_opacity": fill_opacity,
            "name": name,
            "type": "island" if is_island else "water"
        })

    # HTML template с panzoom
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Map Viewer — Interactive</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Panzoom library -->
    <script src="https://unpkg.com/@panzoom/panzoom@4.5.1/dist/panzoom.min.js"></script>

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #0a0a0b;
            color: #fafafa;
            overflow: hidden;
        }}

        #container {{
            width: 100vw;
            height: 100vh;
            position: relative;
            overflow: hidden;
        }}

        #map-svg {{
            cursor: grab;
            display: block;
        }}

        #map-svg:active {{
            cursor: grabbing;
        }}

        path {{
            stroke-width: 2;
            transition: stroke-width 0.2s, fill-opacity 0.2s;
        }}

        path:hover {{
            stroke-width: 4;
            fill-opacity: 0.9 !important;
        }}

        .controls {{
            position: absolute;
            top: 20px;
            right: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            z-index: 100;
        }}

        button {{
            width: 40px;
            height: 40px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 4px;
            color: #fafafa;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.2s;
        }}

        button:hover {{
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-1px);
        }}

        .legend {{
            position: absolute;
            bottom: 20px;
            right: 20px;
            background: rgba(10, 10, 11, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 16px;
            font-size: 14px;
            z-index: 100;
        }}

        .legend-title {{
            font-weight: 600;
            margin-bottom: 12px;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
        }}

        .legend-color {{
            width: 18px;
            height: 18px;
            border-radius: 2px;
            border: 1px solid #2a2a2e;
        }}

        #info {{
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(10, 10, 11, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 16px;
            font-size: 14px;
            max-width: 300px;
            display: none;
            z-index: 100;
        }}

        #info.active {{
            display: block;
        }}

        .info-title {{
            font-weight: 600;
            font-size: 16px;
            margin-bottom: 8px;
        }}

        .info-detail {{
            color: #888;
            margin-bottom: 4px;
        }}

        .instructions {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: rgba(10, 10, 11, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 12px;
            font-size: 12px;
            color: #888;
            z-index: 100;
        }}
    </style>
</head>
<body>
    <div id="container">
        <svg id="map-svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
            <rect width="{width}" height="{height}" fill="#fafafa"/>
"""

    # Добавление paths в SVG
    for item in svg_paths:
        html += f'''            <path
                d="{item['path']}"
                fill="{item['fill']}"
                stroke="{item['stroke']}"
                fill-opacity="{item['fill_opacity']}"
                data-name="{item['name']}"
                data-type="{item['type']}"
            />
'''

    html += f"""        </svg>

        <div class="controls">
            <button id="zoom-in" title="Zoom In">+</button>
            <button id="zoom-out" title="Zoom Out">−</button>
            <button id="reset" title="Reset View">⟲</button>
        </div>

        <div class="legend">
            <div class="legend-title">Map Legend</div>
            <div class="legend-item">
                <div class="legend-color" style="background: #3b82f6; opacity: 0.6;"></div>
                <span>Water</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #f5e6d3; opacity: 0.9;"></div>
                <span>Land</span>
            </div>
        </div>

        <div id="info">
            <div class="info-title" id="info-name">-</div>
            <div class="info-detail" id="info-type">-</div>
        </div>

        <div class="instructions">
            Drag to pan • Scroll to zoom • Click feature for info
        </div>
    </div>

    <script>
        const svg = document.getElementById('map-svg');
        const info = document.getElementById('info');
        const infoName = document.getElementById('info-name');
        const infoType = document.getElementById('info-type');

        // Initialize panzoom
        const panzoomInstance = Panzoom(svg, {{
            maxScale: 10,
            minScale: 0.5,
            step: 0.3,
            contain: 'outside'
        }});

        // Zoom buttons
        document.getElementById('zoom-in').addEventListener('click', () => {{
            panzoomInstance.zoomIn();
        }});

        document.getElementById('zoom-out').addEventListener('click', () => {{
            panzoomInstance.zoomOut();
        }});

        document.getElementById('reset').addEventListener('click', () => {{
            panzoomInstance.reset();
        }});

        // Wheel zoom
        svg.parentElement.addEventListener('wheel', (e) => {{
            e.preventDefault();
            panzoomInstance.zoomWithWheel(e);
        }});

        // Click on features
        const paths = svg.querySelectorAll('path');
        paths.forEach(path => {{
            path.addEventListener('click', (e) => {{
                e.stopPropagation();
                const name = path.getAttribute('data-name');
                const type = path.getAttribute('data-type');

                infoName.textContent = name;
                infoType.textContent = `Type: ${{type}}`;
                info.classList.add('active');
            }});
        }});

        // Click outside to hide info
        svg.addEventListener('click', () => {{
            info.classList.remove('active');
        }});
    </script>
</body>
</html>"""

    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ SVG viewer saved: {output_html}")
    print(f"  Open in browser to view interactive map")


def main():
    if len(sys.argv) < 2:
        print("Usage: python svg_viewer.py <topology.json> [output.html]")
        sys.exit(1)

    topology_path = sys.argv[1]
    output_html = sys.argv[2] if len(sys.argv) > 2 else "map_viewer.html"

    topology_to_svg(topology_path, output_html)


if __name__ == "__main__":
    main()
