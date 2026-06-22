---
description: "Апскейл изображений через AuraSR v2 (4x, GAN, локально на MPS). Используй когда пользователь говорит 'увеличь картинку', 'upscale', 'апскейл', 'enhance image', 'увеличь разрешение', 'сделай картинку больше', '4x', 'улучши качество картинки'. Локальный процессинг на Mac (MPS). НЕ используй для: генерации новых изображений (/nanobanana), редактирования изображений (/l-d-img-edit), промптов Midjourney (/l-g-midjourney)."
aliases:
  - enhance
  - upscale
  - l-d-upscale
---

# AuraSR v2: Апскейл изображений

Локальный 4x апскейлер на базе AuraSR v2 (GAN). Работает на Apple M3 Max через MPS. ~50 сек на изображение.

## Модель и зависимости

- **Модель:** `/Users/lance/ComfyUI/models/Aura-SR/model.safetensors` (2.3 GB)
- **Config:** `/Users/lance/ComfyUI/models/Aura-SR/config.json`
- **Python venv:** `/Users/lance/ComfyUI/venv/bin/python3`
- **Пакет:** `aura-sr` (установлен в ComfyUI venv)
- **ComfyUI нода:** `~/ComfyUI/custom_nodes/AuraSR-ComfyUI/` (тоже установлена)

## Как использовать

### Вход от пользователя

Пользователь указывает путь к изображению (или оно только что сгенерировано через nanobanana).

### Скрипт апскейла

```bash
/Users/lance/ComfyUI/venv/bin/python3 << 'PYEOF'
import time, json, os
import torch
from pathlib import Path
from PIL import Image
from safetensors.torch import load_file
from aura_sr import AuraSR

device = "mps"
model_dir = Path("/Users/lance/ComfyUI/models/Aura-SR")

# Load model
config = json.loads((model_dir / "config.json").read_text())
aura_sr = AuraSR(config=config, device=device)
weights = load_file(str(model_dir / "model.safetensors"))
aura_sr.upsampler.load_state_dict(weights)
aura_sr.upsampler.to(device)

# Load image
src = "$IMAGE_PATH"
img = Image.open(src)
print(f"Input: {img.size[0]}x{img.size[1]}")

# Upscale 4x
t0 = time.time()
result = aura_sr.upscale_4x(img)
print(f"Upscaled in {time.time()-t0:.1f}s -> {result.size[0]}x{result.size[1]}")

# Save next to original with _4x suffix
src_path = Path(src)
out_path = src_path.parent / f"{src_path.stem}_4x.png"
result.save(str(out_path))
print(f"Saved: {out_path} ({os.path.getsize(out_path)/1024/1024:.1f} MB)")
PYEOF
```

### Переменные

- `$IMAGE_PATH` — заменить на абсолютный путь к изображению

### Правила

1. **Выходной файл** сохраняется рядом с оригиналом с суффиксом `_4x`
2. Формат выхода — PNG (без потерь)
3. После апскейла — сообщи путь к файлу и предложи открыть (`open <path>`)
4. Если изображение очень большое (>2000px по стороне), предупреди что выход будет >8000px и ~30+ MB
5. Можно использовать после nanobanana: сгенерировал -> улучшил

### Характеристики

| Параметр | Значение |
|----------|----------|
| Масштаб | 4x (фиксированный) |
| Модель | AuraSR v2 (GAN, fal-ai) |
| Размер модели | 2.3 GB |
| Скорость | ~50 сек на M3 Max MPS |
| Качество | Отличное для AI-арта, hard-surface, sci-fi |
| Артефакты | Нет (проверено) |
