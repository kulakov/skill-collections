---
description: "Вайб-кодинг лендингов по референсу. Используй когда пользователь говорит 'сделай лендинг как у X', 'лендинг по референсу', 'vibe landing', 'скопируй стиль сайта', 'сверстай как этот сайт', 'landing like this', 'одностраничник по примеру'. Берёт паттерн из каталога аналогов, спрашивает контент, генерирует готовый HTML через диалог. НЕ используй для: методики копирайтинга лендинга (/l-d-landing), оркестрации полного пайплайна (/l-d-land-orch), генерации картинок для лендинга (/nanobanana), Figma-to-code (/l-d-figma)."
aliases:
  - l-d-vl
  - vibe-landing
allowed-tools: Read, Write, Edit, Bash, WebFetch, WebSearch, Glob, Grep
---

# Vibe Landing — Лендинг по референсу через диалог

Генерация одностраничных лендингов через разговор. Без 7-фазных пайплайнов — сразу к делу.

## Вход

**Запрос пользователя:** $ARGUMENTS

---

## ПРОТОКОЛ

### Шаг 1: Определить референс

Если пользователь дал URL — проанализировать через WebFetch.
Если дал номер/название из каталога — прочитать паттерны из:
`~/10-CLAUDE/jetstyle-dreambooth-landing/ANALOG-CATALOG.md`

Если ничего не дал — спросить:

> Какой вайб? Выбери или дай ссылку:
> 1. **Dark premium** (как Lightweight) — narrative scroll, 3D, минимум CTA
> 2. **SaaS dark** (как Linear) — dot grid, gradient text, developer feel
> 3. **Playful** (как Arc) — бежевый, SVG waves, personality
> 4. **Automotive** (как Rivian) — параллакс, fullscreen фото, жёлтый CTA
> 5. **B2B enterprise** (как Varjo) — чёрно-белый, моношрифт, модульный
> 6. **Product showcase** (как Nothing) — fullscreen slides, минимализм
> 7. **Apple-style** — scroll-driven video, progressive disclosure
> 8. **SaaS PLG** (как Matterport) — embedded demo, pricing, множество CTA
> 9. Свой URL — проанализирую и скопирую стиль

### Шаг 2: Собрать контент (быстро)

Спросить **только необходимое** (не 5 вопросов — одним блоком):

> Заполни:
> - **Продукт:** (что продаёшь, 1 предложение)
> - **Для кого:** (кто покупает)
> - **Главный CTA:** (что должен сделать посетитель)
> - **Есть тексты?** (ссылка на COPY.md, BRIEF.md, или "напиши сам")

Если есть COPY.md/BRIEF.md в проекте — прочитать и использовать.
Если пользователь говорит "напиши сам" — сгенерировать тексты по паттерну референса.

### Шаг 3: Выбрать техническую реализацию

На основе паттернов референса, выбрать нужные CDN:

#### Базовый набор (всегда)

```html
<!-- Tailwind для быстрой стилизации -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- Lucide Icons (SVG, без эмодзи) -->
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>

<!-- Google Fonts (выбрать под стиль) -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

#### Scroll-анимации (Lightweight, Apple, Rivian)

```html
<!-- GSAP + ScrollTrigger -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/ScrollTrigger.min.js"></script>
```

Паттерны:
- **Fade-in при скролле**: `gsap.from(el, {opacity:0, y:50, scrollTrigger: el})`
- **Parallax**: `gsap.to(bg, {yPercent: -30, scrollTrigger: {scrub: true}})`
- **Scroll-snap sections**: `gsap.utils.toArray('.section').forEach(s => ScrollTrigger.create({snap:...}))`
- **Pin + timeline**: `ScrollTrigger.create({pin: true, scrub: true})`

#### 3D Hero (Lightweight-style)

```html
<!-- Three.js (vanilla, без React) -->
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.160/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160/examples/jsm/"
  }
}
</script>
```

**КРИТИЧЕСКАЯ АРХИТЕКТУРА — Fixed Canvas + Scrollable Overlay:**

```css
/* Canvas FIXED за всем контентом */
#canvas-3d { position: fixed; inset: 0; z-index: 1; }
/* Контент скроллится ПОВЕРХ canvas */
.scroll-content { position: relative; z-index: 10; }
/* Секции прозрачные — 3D видно сквозь */
.hero, .scroll-chapter { pointer-events: none; }
.hero-content, .chapter-text { pointer-events: auto; }
```

Без этого камера не облетает — canvas уедет вместе с контентом.

**Camera Orbit — сферические координаты через ScrollTrigger:**

```javascript
// Keyframes: theta=горизонтальный угол, phi=вертикальный, r=расстояние
const KF = [
  { theta: 0.3,  phi: 0.15, r: 7.0 },  // Hero: front 3/4
  { theta: 1.4,  phi: 0.25, r: 5.0 },  // Section 2: side
  { theta: 2.8,  phi: 0.45, r: 3.5 },  // Section 3: back-top
  { theta: 4.2,  phi: 0.08, r: 2.5 },  // Section 4: dramatic close
];

// Один master ScrollTrigger на весь scroll-content
ScrollTrigger.create({
  trigger: '.scroll-content',
  start: 'top top', end: 'bottom bottom',
  scrub: 1.5,
  onUpdate: (self) => {
    const p = self.progress * (KF.length - 1);
    const i = Math.min(Math.floor(p), KF.length - 2);
    const t = p - i;
    camTarget.theta = KF[i].theta + (KF[i+1].theta - KF[i].theta) * t;
    camTarget.phi   = KF[i].phi   + (KF[i+1].phi   - KF[i].phi)   * t;
    camTarget.r     = KF[i].r     + (KF[i+1].r     - KF[i].r)     * t;
  }
});

// В animate() — smooth follow + spherical → cartesian
cam.theta += (camTarget.theta - cam.theta) * 0.05;
const pos = new THREE.Vector3(
  cam.r * Math.cos(cam.phi) * Math.sin(cam.theta),
  cam.r * Math.sin(cam.phi) + 0.3,
  cam.r * Math.cos(cam.phi) * Math.cos(cam.theta)
);
camera.position.copy(pos);
camera.lookAt(0, 0.3, 0);
```

**GLB модель — auto-center + auto-scale:**

```javascript
new GLTFLoader().load(url, (gltf) => {
  const model = gltf.scene;
  const box = new THREE.Box3().setFromObject(model);
  const center = box.getCenter(new THREE.Vector3());
  const maxDim = Math.max(...box.getSize(new THREE.Vector3()).toArray());
  const scale = 3.0 / maxDim;
  const wrap = new THREE.Group();
  model.position.set(-center.x, -center.y, -center.z);
  wrap.add(model);
  wrap.scale.setScalar(scale);
  scene.add(wrap);
});
```

**Освещение для тёмного фона (6 источников):**

```javascript
scene.add(new THREE.DirectionalLight(0xfff5e6, 3.5));  // Key: тёплый
scene.add(new THREE.DirectionalLight(0x88bbff, 1.5));  // Fill: холодный
scene.add(new THREE.DirectionalLight(0x14b8a6, 2.0));  // Rim: teal
scene.add(new THREE.DirectionalLight(0xffffff, 1.0));  // Top
scene.add(new THREE.AmbientLight(0x334466, 0.6));
scene.add(new THREE.HemisphereLight(0x445588, 0x111111, 0.5));
```

Renderer: `antialias: true, alpha: false, toneMapping: ACESFilmic, exposure: 1.4`

**ВАЖНО:** GLB модели требуют HTTP-сервер (`python3 -m http.server 8765`), file:// не работает из-за CORS. Бесплатные GLB на CDN: Poly.pizza (`https://static.poly.pizza/[uuid].glb`).

#### Scroll-driven видео (Apple-style)

```javascript
// Без библиотек — чистый JS
const video = document.querySelector('video');
window.addEventListener('scroll', () => {
  const scrollFraction = window.scrollY / (document.body.scrollHeight - window.innerHeight);
  video.currentTime = scrollFraction * video.duration;
});
```

#### Image sequence (Apple альтернатива)

```javascript
// Canvas + предзагруженные кадры
const canvas = document.querySelector('canvas');
const ctx = canvas.getContext('2d');
const frames = [];
for (let i = 1; i <= 60; i++) {
  const img = new Image();
  img.src = `frames/frame-${String(i).padStart(3,'0')}.webp`;
  frames.push(img);
}
window.addEventListener('scroll', () => {
  const index = Math.floor(scrollFraction * (frames.length - 1));
  ctx.drawImage(frames[index], 0, 0, canvas.width, canvas.height);
});
```

#### Animated backgrounds (Linear-style)

```javascript
// Dot grid на canvas
const canvas = document.querySelector('#dot-grid');
const ctx = canvas.getContext('2d');
// Рисуем сетку точек, при mousemove подсвечиваем ближайшие
```

#### Glassmorphism карточки

```css
.glass-card {
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
}
```

### Шаг 4: Генерация

Создать **один self-contained HTML файл** со всем inline:
- CSS через Tailwind + `<style>` для кастомных анимаций
- JS через CDN + `<script>` для логики
- SVG иконки inline (Lucide)
- Placeholder изображения через `https://placehold.co/` или Unsplash

**Правила генерации:**
1. Файл должен работать при открытии в браузере (no build step)
2. Responsive: mobile-first, breakpoints sm/md/lg
3. Smooth scroll: `html { scroll-behavior: smooth }`
4. Нет эмодзи — только SVG иконки
5. CSS custom properties для цветов (легко менять)
6. Семантический HTML (section, article, nav, footer)
7. Каждая секция = отдельный `<section>` с id
8. CTA = `<a href="mailto:...">` или `<a href="#contact">`
9. Изображения: `loading="lazy"`, alt-text
10. Favicn: inline SVG data URI

**Имя файла:** `landing-[style]-[date].html`
**Расположение:** текущая рабочая директория

### Шаг 5: Открыть и итерировать

```bash
# Без 3D — просто открыть файл
open -a "Arc" landing-*.html

# С 3D GLB — запустить HTTP сервер
cd /path/to/project && python3 -m http.server 8765 &
open -a "Arc" "http://localhost:8765/landing-*.html"
```

После открытия — спросить:

> Открыл в Arc. Что поправить?
> - Цвета?
> - Тексты?
> - Порядок секций?
> - Добавить/убрать секцию?
> - Анимации?

Итерировать через Edit tool — не переписывать файл целиком.

---

## ШРИФТОВЫЕ ПРЕСЕТЫ (по вайбу)

| Вайб | Heading | Body | Mono |
|------|---------|------|------|
| Premium dark | Playfair Display 700 | Inter 400 | -- |
| SaaS developer | Inter 600 | Inter 400 | JetBrains Mono |
| Playful | DM Serif Display 400i | DM Sans 400 | Space Mono |
| Enterprise | Space Grotesk 700 | Source Sans 3 400 | Space Mono |
| Automotive | Bebas Neue 400 | Inter 400 | -- |
| Minimal | Instrument Serif 400i | Instrument Sans 400 | -- |
| Editorial | Fraunces 700 | Source Serif 4 400 | -- |

Все доступны через Google Fonts CDN.

---

## ЦВЕТОВЫЕ ПРЕСЕТЫ

| Вайб | BG | Text | Accent | Secondary |
|------|-----|------|--------|-----------|
| Dark premium | #09090b | #fafafa | #3b82f6 | #a1a1aa |
| SaaS dark | #0a0a0b | #e4e4e7 | #7c3aed→#3b82f6 gradient | #52525b |
| Playful | #fffcec | #1a1a1a | #3139fb | #fb3a4d |
| Automotive | #000000 | #ffffff | #ffac00 | #a3a3a3 |
| Enterprise B&W | #ffffff | #151515 | #000000 | #737373 |
| Industrial | #09090b | #d4d4d8 | #14b8a6 | #f97316 |

---

## ПАТТЕРНЫ СЕКЦИЙ (копируемые блоки)

### Hero variants

**A) Headline + video (Lightweight/DreamBooth)**
```
[gradient-bg-glow]
  [container max-w-7xl mx-auto grid 2-col]
    [left: label + h1 gradient-text + p + CTA button]
    [right: video-placeholder 16:10 aspect with play icon]
```

**B) Centered headline (Apple/Linear)**
```
[full-viewport-height flex-center]
  [text-center]
    [label uppercase tracking-wider text-sm]
    [h1 text-6xl font-bold gradient-text]
    [p text-xl text-muted max-w-2xl]
    [CTA button mt-8]
```

**C) 3D orbit with scroll chapters (Lightweight)**
```
[#canvas-3d position:fixed inset:0 z-index:1]
[.scroll-content position:relative z-index:10]
  [.hero 100vh flex align-center pointer-events:none]
    [.hero-content left-aligned: label + h1 gradient + p + CTA]
  [.scroll-chapter 100vh each, glassmorphic .chapter-text cards]
    [chapter-label uppercase + h2 + p, fade in/out on scroll]
  [.scroll-chapter ...]
  [.scroll-chapter ...]
```
Hero text **остаётся видимым** при скролле. Chapter texts fade in/out индивидуально через ScrollTrigger.

### Social proof variants

**A) Logo bar** — 4-6 logos in flex row, grayscale, opacity 0.5
**B) Quote cards** — 3 columns, photo + quote + name
**C) Stats row** — 3-4 numbers with labels (e.g. "500+ clients")

### CTA variants

**A) Centered with glow** — radial gradient bg, h2 + p + button centered
**B) Split with image** — left text + CTA, right photo
**C) Sticky bottom bar** — fixed to bottom on mobile, fades in after scroll

---

## БЫСТРЫЕ КОМАНДЫ

Если пользователь говорит:
- "как Lightweight" / "dark premium" → Пресет 1 + GSAP + опционально Three.js
- "как Linear" / "SaaS dark" → Пресет 2 + dot grid canvas + gradient text
- "как Arc" / "playful" → Пресет 3 + SVG waves + scale-hover buttons
- "как Rivian" / "automotive" → Пресет 4 + GSAP parallax + snap scroll
- "как Apple" / "cinematic" → Пресет 5 + scroll-driven video
- "как Varjo" / "enterprise" → Пресет 6 + clean grid + mono font
- "как Nothing" / "product slides" → Пресет 7 + fullscreen swiper
- "как Matterport" / "SaaS PLG" → Пресет 8 + pricing table + accordion
- "быстрый лендинг" / "MVP" → Minimal: hero + 3 features + CTA

---

## ЧЕКЛИСТ ПЕРЕД ОТДАЧЕЙ

- [ ] Файл открывается в браузере (без 3D — без сервера; с 3D GLB — через HTTP)
- [ ] Если GLB: запустить `python3 -m http.server 8765` в папке проекта
- [ ] Mobile responsive (проверить при 375px)
- [ ] Нет эмодзи
- [ ] CTA работает (mailto: или якорь)
- [ ] Все секции имеют id (для навигации)
- [ ] Цвета через CSS custom properties
- [ ] Плавный скролл
- [ ] Ленивая загрузка изображений
- [ ] GSAP/Three.js грузятся с CDN без ошибок
- [ ] Если 3D: canvas fixed, content z-index выше canvas

---

## ПРИМЕРЫ ЗАПРОСОВ

```
/vibe-landing как Linear, продукт — SaaS для HR, CTA — "Start Free Trial"
/vibe-landing как Lightweight но без 3D, для промышленного оборудования
/vibe-landing playful, для мобильного приложения, тексты из COPY.md
/vibe-landing https://example.com — скопируй стиль, контент мой
/vibe-landing быстрый лендинг для воркшопа, дата 15 марта
```
