#!/usr/bin/env python3
"""
GeoJSON export для интеграции с Leaflet/OpenStreetMap.

Конвертирует топологию из JSON в GeoJSON FeatureCollection.
Поддерживает: моря, острова, города, горы, дороги, реки.
"""

import json
import sys


def topology_to_geojson(topology_path, output_path=None):
    """
    Конвертирует topology JSON в GeoJSON для Leaflet.

    Args:
        topology_path: путь к JSON с извлечёнными координатами
        output_path: путь для сохранения GeoJSON (опционально)

    Returns:
        dict: GeoJSON FeatureCollection
    """
    with open(topology_path, 'r') as f:
        topology = json.load(f)

    features = []

    for name, feature in topology.items():
        points = feature["points"]
        is_island = feature["is_island"]
        area_pct = feature["area_pct"]

        # GeoJSON использует [lon, lat] (x, y), наши координаты уже в 0..1
        # Для веб-карт нужно перевести в географические координаты
        # Условные границы: lon [-10, 10], lat [40, 60]
        coordinates = []
        for x, y in points:
            lon = -10 + x * 20  # -10..10 degrees
            lat = 60 - y * 20   # 60..40 degrees (y инвертирован)
            coordinates.append([lon, lat])

        # Замыкаем полигон (первая точка = последняя)
        if coordinates[0] != coordinates[-1]:
            coordinates.append(coordinates[0])

        geo_feature = {
            "type": "Feature",
            "properties": {
                "name": name,
                "type": "island" if is_island else "water",
                "area_pct": area_pct
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [coordinates]  # GeoJSON требует массив массивов
            }
        }

        features.append(geo_feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(geojson, f, ensure_ascii=False, indent=2)
        print(f"✓ GeoJSON saved: {output_path}")

    return geojson


def create_leaflet_html(geojson_path, output_html="map_leaflet.html"):
    """
    Создаёт HTML файл с интерактивной картой Leaflet.

    Args:
        geojson_path: путь к GeoJSON файлу
        output_html: путь для сохранения HTML
    """
    with open(geojson_path, 'r') as f:
        geojson_data = json.load(f)

    html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Map Viewer — Leaflet</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Leaflet CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
          integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
          crossorigin=""/>

    <!-- Leaflet JS -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
            integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
            crossorigin=""></script>

    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        #map {
            width: 100vw;
            height: 100vh;
        }
        .info {
            padding: 6px 8px;
            font: 14px/16px Arial, Helvetica, sans-serif;
            background: white;
            background: rgba(255,255,255,0.9);
            box-shadow: 0 0 15px rgba(0,0,0,0.2);
            border-radius: 5px;
        }
        .info h4 {
            margin: 0 0 5px;
            color: #777;
        }
    </style>
</head>
<body>
    <div id="map"></div>

    <script>
        // Инициализация карты
        const map = L.map('map', {
            crs: L.CRS.Simple,
            minZoom: -5,
            maxZoom: 2
        });

        // GeoJSON данные
        const geojsonData = """ + json.dumps(geojson_data, indent=4) + """;

        // Вычисление bounds из GeoJSON
        let minLon = Infinity, maxLon = -Infinity;
        let minLat = Infinity, maxLat = -Infinity;

        geojsonData.features.forEach(feature => {
            feature.geometry.coordinates[0].forEach(coord => {
                const [lon, lat] = coord;
                minLon = Math.min(minLon, lon);
                maxLon = Math.max(maxLon, lon);
                minLat = Math.min(minLat, lat);
                maxLat = Math.max(maxLat, lat);
            });
        });

        // Преобразование географических координат в пиксели для Simple CRS
        const bounds = [[minLat, minLon], [maxLat, maxLon]];
        map.fitBounds(bounds);

        // Функция стилизации
        function style(feature) {
            return {
                fillColor: feature.properties.type === 'water' ? '#3b82f6' : '#f5e6d3',
                weight: 2,
                opacity: 1,
                color: '#2a2a2e',
                fillOpacity: feature.properties.type === 'water' ? 0.6 : 0.9
            };
        }

        // Функция подсветки при наведении
        function highlightFeature(e) {
            const layer = e.target;
            layer.setStyle({
                weight: 4,
                color: '#e8ff47',
                fillOpacity: 0.8
            });
            layer.bringToFront();
        }

        function resetHighlight(e) {
            geojsonLayer.resetStyle(e.target);
        }

        // Функция при клике
        function onEachFeature(feature, layer) {
            layer.on({
                mouseover: highlightFeature,
                mouseout: resetHighlight
            });

            // Popup с информацией
            if (feature.properties) {
                const props = feature.properties;
                layer.bindPopup(`
                    <strong>${props.name}</strong><br>
                    Type: ${props.type}<br>
                    Area: ${props.area_pct.toFixed(2)}%
                `);
            }
        }

        // Добавление GeoJSON слоя
        const geojsonLayer = L.geoJSON(geojsonData, {
            style: style,
            onEachFeature: onEachFeature
        }).addTo(map);

        // Легенда
        const legend = L.control({position: 'bottomright'});
        legend.onAdd = function (map) {
            const div = L.DomUtil.create('div', 'info');
            div.innerHTML = `
                <h4>Map Legend</h4>
                <i style="background: #3b82f6; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.6;"></i> Water<br>
                <i style="background: #f5e6d3; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.9;"></i> Land
            `;
            return div;
        };
        legend.addTo(map);
    </script>
</body>
</html>""";

    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print(f"✓ Leaflet HTML saved: {output_html}")
    print(f"  Open in browser to view interactive map")


def main():
    if len(sys.argv) < 2:
        print("Usage: python geojson_export.py <topology.json> [output.geojson]")
        sys.exit(1)

    topology_path = sys.argv[1]
    geojson_path = sys.argv[2] if len(sys.argv) > 2 else "map.geojson"

    # Экспорт GeoJSON
    topology_to_geojson(topology_path, geojson_path)

    # Создание HTML с Leaflet
    html_path = geojson_path.replace('.geojson', '_leaflet.html')
    create_leaflet_html(geojson_path, html_path)


if __name__ == "__main__":
    main()
