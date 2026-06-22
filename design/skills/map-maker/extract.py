#!/usr/bin/env python3
"""
OpenCV extraction engine для извлечения топологии из AI-референса.

Алгоритм:
1. HSV-сегментация (H=90-130, S>80, V>80) → маска воды
2. Морфологическая очистка (CLOSE → OPEN)
3. Извлечение контуров (RETR_TREE) → иерархия
4. Упрощение Douglas-Peucker → целевое количество точек
5. Нормализация координат (0..1)
6. Сохранение JSON + debug visualization
"""

import cv2
import numpy as np
import json
import sys
import os


def simplify_contour(contour, target_points):
    """
    Binary search для достижения целевого количества точек.

    Args:
        contour: OpenCV contour (Nx1x2 array)
        target_points: желаемое количество точек

    Returns:
        Simplified contour с ~target_points точками
    """
    perimeter = cv2.arcLength(contour, closed=True)
    epsilon_low, epsilon_high = 0.0, perimeter * 0.1

    best_simplified = contour
    best_diff = float('inf')

    for _ in range(50):  # max iterations
        epsilon = (epsilon_low + epsilon_high) / 2
        simplified = cv2.approxPolyDP(contour, epsilon, closed=True)
        num_points = len(simplified)

        diff = abs(num_points - target_points)
        if diff < best_diff:
            best_diff = diff
            best_simplified = simplified

        if num_points > target_points:
            epsilon_low = epsilon
        else:
            epsilon_high = epsilon

        if epsilon_high - epsilon_low < 1e-6:
            break

    return best_simplified


def extract_topology(image_path, target_points=None, debug=True):
    """
    Извлекает топологию из AI-референса через HSV-сегментацию.

    Args:
        image_path: путь к reference PNG с чистыми цветами
        target_points: dict с целевым количеством точек для каждого типа контура
                       {"sea": 30, "large_island": 15, "small_island": 7}
        debug: создавать ли debug visualization

    Returns:
        dict с извлечёнными контурами в формате:
        {
            "sea_name": {
                "points": [[x, y], ...],  # normalized 0..1
                "area_pct": 16.82,
                "is_island": false
            },
            ...
        }
    """
    if target_points is None:
        target_points = {"sea": 30, "large_island": 15, "small_island": 7}

    # Загрузка изображения
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Cannot load image: {image_path}")

    h, w = img.shape[:2]
    total_pixels = h * w

    # Конвертация BGR → HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Маска воды: синий цвет (H=90-130), высокая насыщенность (S>80), яркость (V>80)
    lower_blue = np.array([90, 80, 80])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Морфологическая очистка
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # закрыть дыры
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # убрать шум

    # Извлечение контуров с иерархией
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if hierarchy is None:
        return {}

    hierarchy = hierarchy[0]  # unwrap

    # Классификация контуров
    result = {}
    sea_count = 0
    island_count = 0

    # Создание debug изображения
    if debug:
        debug_img = img.copy()

    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        area_pct = (area / total_pixels) * 100

        # Пропускаем слишком маленькие контуры (шум)
        if area_pct < 0.1:
            continue

        # Определяем тип контура по иерархии
        parent_idx = hierarchy[i][3]
        is_island = parent_idx >= 0  # если есть parent → это остров (hole внутри моря)

        # Выбор target_points
        if is_island:
            if area_pct > 1.0:
                target = target_points.get("large_island", 15)
                name = f"island_large_{island_count}"
            else:
                target = target_points.get("small_island", 7)
                name = f"island_small_{island_count}"
            island_count += 1
        else:
            target = target_points.get("sea", 30)
            if area_pct > 10:
                name = f"sea_{sea_count}"
            elif area_pct > 2:
                name = f"water_region_{sea_count}"
            else:
                name = f"pond_{sea_count}"
            sea_count += 1

        # Упрощение контура
        simplified = simplify_contour(contour, target)

        # Нормализация координат (0..1)
        points = []
        for pt in simplified:
            x, y = pt[0]
            norm_x = x / w
            norm_y = y / h
            points.append([round(norm_x, 4), round(norm_y, 4)])

        # Сохранение
        result[name] = {
            "points": points,
            "area_pct": round(area_pct, 2),
            "is_island": bool(is_island)  # Convert numpy bool to Python bool
        }

        # Debug visualization
        if debug:
            color = (0, 255, 255) if is_island else (0, 255, 0)  # cyan для островов, зелёный для воды
            cv2.drawContours(debug_img, [simplified], -1, color, 2)

            # Подпись
            M = cv2.moments(simplified)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.putText(debug_img, f"{name} ({len(simplified)}pts)", (cx - 50, cy),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    # Сохранение debug изображения
    if debug:
        output_dir = os.path.dirname(image_path)
        debug_path = os.path.join(output_dir, "_debug_contours.png")
        cv2.imwrite(debug_path, debug_img)
        print(f"Debug visualization saved: {debug_path}")

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract.py <reference_image.png> [output.json]")
        sys.exit(1)

    image_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "topology.json"

    print(f"Extracting topology from {image_path}...")

    # Извлечение
    topology = extract_topology(image_path, debug=True)

    # Сохранение JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(topology, f, ensure_ascii=False, indent=2)

    print(f"✓ Topology saved: {output_path}")
    print(f"  {len(topology)} features extracted")

    # Статистика
    seas = sum(1 for v in topology.values() if not v["is_island"])
    islands = sum(1 for v in topology.values() if v["is_island"])
    total_area = sum(v["area_pct"] for v in topology.values() if not v["is_island"])

    print(f"  Seas: {seas}, Islands: {islands}")
    print(f"  Total water coverage: {total_area:.1f}%")


if __name__ == "__main__":
    main()
