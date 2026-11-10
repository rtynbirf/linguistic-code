"""
Linguistic Code v19 «TETRAPTYCH» — полиматический синтез 12 мнений + 4 новации.

8 слоёв:
1. CAVE (Ловушка 0-5): 560px навсегда через min() — не @media
2. SCRIPTORIUM (Манифест 6): 740px текст + 840px epistemic-gap + контемплятивная маргиналия
3. ARIADNE THREAD: Ghost Rail СПРАВА (не слева!), hover→220px с заголовками
4. BREATH: clamp() типографика + Progress Thread (тонкая линия сверху)
5. FOVEA: активный тезис резкий (opacity 1), остальные затухают (0.5)
6. MARGIN MEMORY: номер 01-33 как семантический маркер в самом тезисе (встроенный, не отдельная колонка)
7. EPHEMERAL NAVIGATOR: клавиша M → временная карта 6×6 → выбираешь → исчезает
8. ЭПИСТЕМИЧЕСКАЯ ПОДПИСЬ v19

Принципы (полиматический жест):
- Никакого sidebar слева (LTR: левое поле = якорь чтения, не панель)
- Никакого Submarine Index в углу (заменён на Ariadne Thread справа)
- Никакого переключателя режимов (нарушает тезис 12)
- Никакой карточной сетки (нарушает линейность)
- Ephemeral Navigator = навигация без интерфейса (существует только когда вызвана)
"""
import re
from pathlib import Path

SRC = Path('/home/z/my-project/download/linguistic-code-v18.1-final.html')
DST = Path('/home/z/my-project/download/linguistic-code-v19-tetraptych.html')

html = SRC.read_text(encoding='utf-8')

# ============================================================
# ПАТЧ 1: id="thesis-NN" для всех accordion-item
# ============================================================
counter = [0]
def add_thesis_id(match):
    counter[0] += 1
    return f'<div class="accordion-item" id="thesis-{counter[0]:02d}">'
html = re.sub(r'<div class="accordion-item">', add_thesis_id, html)
assert counter[0] == 33, f"Expected 33, got {counter[0]}"

# ============================================================
# ПАТЧ 2: CSS — 8 слоёв TETRAPTYCH
# ============================================================
css = """
  /* === v19 · TETRAPTYCH · 8 слоёв === */

  /* СЛОЙ 1: CAVE — Ловушка (0-5), 560px навсегда через min() */
  .screen-honesty .card,
  .step-1 .card,
  .step-2,
  .step-3 .card,
  .step-4 .card,
  .step-5 .card {
    max-width: min(560px, calc(100vw - 48px));
    margin-inline: auto;
  }

  /* СЛОЙ 2: SCRIPTORIUM — Манифест (6), 740px+840px */
  .screen-manifest .accordion {
    max-width: min(840px, calc(100vw - 48px));
    margin-inline: auto;
  }
  .screen-manifest .accordion-content { max-width: 740px; }
  .screen-manifest .epistemic-gap { max-width: 820px; }

  /* Контемплятивная маргиналия — тонкие вертикальные линии */
  .contemplative-margin {
    position: fixed;
    top: 0; bottom: 0;
    width: 1px;
    background: linear-gradient(to bottom,
      transparent 0%, var(--gold-dim) 15%,
      var(--gold-dim) 85%, transparent 100%);
    opacity: 0.08;
    pointer-events: none;
    z-index: 1;
    display: none;
  }
  .contemplative-margin.left  { left:  max(24px, calc((100vw - 840px) / 2 - 24px)); }
  .contemplative-margin.right { right: max(24px, calc((100vw - 840px) / 2 - 24px)); }
  @media (min-width: 1100px) { .contemplative-margin { display: block; } }

  /* СЛОЙ 3: ARIADNE THREAD — Ghost Rail СПРАВА, hover→220px */
  .ariadne-thread {
    position: fixed;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 44px;
    max-height: calc(100vh - 80px);
    overflow-y: auto;
    overflow-x: hidden;
    background: rgba(14, 16, 17, 0.7);
    backdrop-filter: blur(6px);
    border-left: 1px solid var(--surface-2);
    border-radius: 6px 0 0 6px;
    padding: 12px 0;
    z-index: 50;
    opacity: 0.18;
    transition: width 0.35s ease, opacity 0.35s ease, background 0.35s;
    scrollbar-width: none;
    display: none;
  }
  .ariadne-thread::-webkit-scrollbar { display: none; }
  .ariadne-thread:hover {
    width: 240px;
    opacity: 1;
    background: rgba(14, 16, 17, 0.96);
    border-left-color: var(--gold-dim);
  }
  .ariadne-item {
    display: flex;
    align-items: baseline;
    gap: 10px;
    padding: 5px 12px;
    color: var(--text-faint);
    cursor: pointer;
    white-space: nowrap;
    text-decoration: none;
    transition: color 0.15s, background 0.15s;
    font-family: var(--mono);
    font-size: 10px;
    line-height: 1.5;
  }
  .ariadne-item:hover { color: var(--gold); background: var(--gold-faint); }
  .ariadne-item.active { color: var(--gold); }
  .ariadne-item.active .ariadne-num { color: var(--gold); }
  .ariadne-num { flex: 0 0 24px; color: var(--text-dim); }
  .ariadne-title {
    opacity: 0;
    transition: opacity 0.25s 0.1s;
    font-size: 10px;
    overflow: hidden;
    text-overflow: ellipsis;
    font-family: var(--sans);
    color: var(--text-dim);
  }
  .ariadne-thread:hover .ariadne-title { opacity: 1; }
  @media (min-width: 1280px) { .ariadne-thread { display: block; } }

  /* СЛОЙ 4: BREATH — Progress Thread + clamp() типографика */
  .progress-thread {
    position: fixed;
    top: 0;
    left: 0;
    width: 0%;
    height: 2px;
    background: linear-gradient(to right,
      var(--gold-dim) 0%, var(--gold) 100%);
    z-index: 1000;
    transition: width 0.1s ease;
    display: none;
  }
  @media (min-width: 1024px) { .progress-thread { display: block; } }

  .honesty-title { font-size: clamp(23px, 1.2vw + 18px, 32px); }
  .honesty-body  { font-size: clamp(16px, 0.4vw + 14.5px, 18.5px); }
  .step-1 .instruction { font-size: clamp(22px, 1vw + 18px, 28px); }
  .step-1 .sub-instruction { font-size: clamp(17px, 0.5vw + 14.5px, 21px); }
  .step-3 .statement { font-size: clamp(23px, 1.2vw + 18px, 32px); }
  .step-4 .observation { font-size: clamp(17px, 0.4vw + 15px, 19.5px); }
  .mh-title { font-size: clamp(19px, 0.8vw + 16px, 26px); }
  .accordion-trigger { font-size: clamp(14px, 0.2vw + 13px, 16px); }
  .accordion-content {
    font-size: clamp(16px, 0.35vw + 14.5px, 18.5px);
    line-height: clamp(1.75, 0.02vw + 1.72, 1.88);
  }
  .epistemic-gap {
    font-size: clamp(10.5px, 0.15vw + 10px, 12px);
    line-height: clamp(1.7, 0.01vw + 1.68, 1.8);
  }
  .manifest-footer .mf-text { font-size: clamp(16px, 0.3vw + 14.5px, 18.5px); }

  /* СЛОЙ 5: FOVEA — активный тезис резкий, остальные затухают */
  @media (min-width: 1024px) and (pointer: fine) {
    .screen-manifest.active .accordion-item {
      opacity: 0.5;
      transition: opacity 0.4s ease;
    }
    .screen-manifest.active .accordion-item.fovea-focus {
      opacity: 1;
    }
    .screen-manifest.active .accordion-item.fovea-focus .accordion-trigger {
      color: var(--gold);
    }
  }

  /* СЛОЙ 6: MARGIN MEMORY — номер как семантический маркер в тезисе */
  /* Усиляем существующий .num — делаем его более заметным на десктопе */
  @media (min-width: 1024px) {
    .accordion-trigger .num {
      font-size: clamp(11px, 0.15vw + 10px, 13px);
      color: var(--gold-dim);
      font-weight: 400;
    }
  }

  /* СЛОЙ 7: EPHEMERAL NAVIGATOR — клавиша M */
  .ephemeral-map {
    position: fixed;
    inset: 0;
    background: rgba(10, 11, 12, 0.92);
    backdrop-filter: blur(8px);
    z-index: 200;
    display: none;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.25s;
  }
  .ephemeral-map.open {
    display: flex;
    opacity: 1;
  }
  .ephemeral-map-inner {
    text-align: center;
    max-width: 480px;
    padding: 0 24px;
  }
  .ephemeral-map-label {
    font-family: var(--mono);
    font-size: 9px;
    letter-spacing: 3px;
    color: var(--text-faint);
    text-transform: uppercase;
    margin-bottom: 24px;
  }
  .ephemeral-map-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 4px;
    font-family: var(--mono);
  }
  .ephemeral-map-cell {
    padding: 12px 4px;
    color: var(--text-dim);
    cursor: pointer;
    font-size: 14px;
    transition: color 0.15s, background 0.15s;
    border-radius: 2px;
  }
  .ephemeral-map-cell:hover {
    color: var(--gold);
    background: var(--gold-faint);
  }
  .ephemeral-map-cell.active {
    color: var(--gold);
    background: rgba(198, 168, 91, 0.15);
  }
  .ephemeral-map-hint {
    font-family: var(--mono);
    font-size: 9px;
    color: var(--text-faint);
    margin-top: 24px;
    letter-spacing: 1px;
  }

  /* СЛОЙ 8: version-signature */
  .version-signature {
    position: fixed;
    bottom: 20px;
    left: 24px;
    font-family: var(--mono);
    font-size: 8px;
    letter-spacing: 1px;
    color: var(--text-faint);
    opacity: 0.4;
    z-index: 40;
    pointer-events: none;
    display: none;
  }
  @media (min-width: 1024px) { .version-signature { display: block; } }

  /* prefers-reduced-motion */
  @media (prefers-reduced-motion: reduce) {
    .ariadne-thread { transition: none; opacity: 0.5; }
    .ariadne-thread:hover { opacity: 1; }
    .contemplative-margin { opacity: 0.12; }
    .screen-manifest.active .accordion-item,
    .screen-manifest.active .accordion-item.fovea-focus {
      opacity: 1;
      transition: none;
    }
    .ephemeral-map { transition: none; }
    html { scroll-behavior: auto; }
  }
  @media (prefers-reduced-motion: no-preference) {
    html { scroll-behavior: smooth; }
  }
"""
html = html.replace('</style>', css + '\n</style>', 1)

# ============================================================
# ПАТЧ 3: HTML — все элементы после <body>
# ============================================================
body_extra = """
<div class="contemplative-margin left" aria-hidden="true"></div>
<div class="contemplative-margin right" aria-hidden="true"></div>
<div class="progress-thread" id="progressThread" aria-hidden="true"></div>
<div class="version-signature" aria-hidden="true">v19 · тетраптих · δ требует тело</div>

<nav class="ariadne-thread" id="ariadneThread" aria-label="Навигация по тезисам">
  <!-- генерируется JS -->
</nav>

<div class="ephemeral-map" id="ephemeralMap" role="dialog" aria-modal="true" aria-label="Карта тезисов">
  <div class="ephemeral-map-inner">
    <div class="ephemeral-map-label">33 тезиса · нажми или закрой клавишей M / Esc</div>
    <div class="ephemeral-map-grid" id="ephemeralGrid"></div>
    <div class="ephemeral-map-hint">M — открыть · Esc / M — закрыть</div>
  </div>
</div>
"""
html = html.replace('<body>', '<body>' + body_extra, 1)

# ============================================================
# ПАТЧ 4: title + honesty-mark + footer
# ============================================================
html = html.replace('<title>Linguistic Code v18.1</title>',
                    '<title>Linguistic Code v19 — Тетраптих</title>')
html = html.replace('linguistic code v18.1<br>structural honesty layer',
                    'linguistic code v19<br>тетраптих layer')
html = html.replace(
    'v18.1 · structural honesty layer · no server · no tracking<br>step 5 describing step 1 · awaits a body<br>every card carries its own uncertainty',
    'v19 · тетраптих · no server · no tracking<br>step 5 describing step 1 · awaits a body<br>8 слоёв: cave · scriptorium · ariadne · breath · fovea · margin · ephemeral · signature'
)

# ============================================================
# ПАТЧ 5: JavaScript
# ============================================================
js = """
// === v19 · TETRAPTYCH · JS ===
(function() {
  var items = document.querySelectorAll('.accordion-item');
  if (!items.length) return;

  // --- Ariadne Thread: генерация 33 пунктов с заголовками ---
  var ariadne = document.getElementById('ariadneThread');
  if (ariadne) {
    items.forEach(function(item, i) {
      var num = (i + 1 < 10 ? '0' : '') + (i + 1);
      var titleEl = item.querySelector('.accordion-trigger > span:nth-child(2)');
      var title = titleEl ? titleEl.textContent.trim() : '';
      // Сокращаем до 4 слов
      var words = title.split(/\\s+/).slice(0, 4).join(' ');
      if (words.length > 32) words = words.slice(0, 30) + '…';

      var a = document.createElement('a');
      a.className = 'ariadne-item';
      a.href = '#thesis-' + num;
      a.dataset.thesis = num;
      a.innerHTML = '<span class="ariadne-num">' + num + '</span>' +
                    '<span class="ariadne-title">' + words + '</span>';
      a.addEventListener('click', function(e) {
        e.preventDefault();
        var target = document.getElementById('thesis-' + num);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'center' });
          if (!target.classList.contains('open')) {
            var trig = target.querySelector('.accordion-trigger');
            if (trig) trig.click();
          }
        }
      });
      ariadne.appendChild(a);
    });
  }

  // --- IntersectionObserver: подсветка + фовеа ---
  if ('IntersectionObserver' in window) {
    var ariadneItems = document.querySelectorAll('.ariadne-item');
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          var id = entry.target.id.replace('thesis-', '');
          // Ariadne
          ariadneItems.forEach(function(a) {
            a.classList.toggle('active', a.dataset.thesis === id);
            if (a.dataset.thesis === id) {
              // Скроллим ariadne, чтобы активный был виден
              var rect = a.getBoundingClientRect();
              var parent = a.parentElement.getBoundingClientRect();
              if (rect.top < parent.top || rect.bottom > parent.bottom) {
                a.scrollIntoView({ block: 'nearest' });
              }
            }
          });
          // Fovea
          items.forEach(function(it) {
            it.classList.toggle('fovea-focus', it === entry.target);
          });
          // Ephemeral map active
          document.querySelectorAll('.ephemeral-map-cell').forEach(function(c) {
            c.classList.toggle('active', c.dataset.thesis === id);
          });
        }
      });
    }, { threshold: 0.45, rootMargin: '-15% 0px -15% 0px' });
    items.forEach(function(item) { observer.observe(item); });
  }

  // --- Progress Thread ---
  var progress = document.getElementById('progressThread');
  if (progress) {
    var updateProgress = function() {
      var scrollTop = window.scrollY;
      var docHeight = document.documentElement.scrollHeight - window.innerHeight;
      var p = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      progress.style.width = p + '%';
    };
    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
  }

  // --- Ephemeral Navigator: клавиша M ---
  var ephemeralMap = document.getElementById('ephemeralMap');
  var ephemeralGrid = document.getElementById('ephemeralGrid');
  if (ephemeralMap && ephemeralGrid) {
    // Генерация ячеек 6×6
    for (var i = 1; i <= 33; i++) {
      var num = (i < 10 ? '0' : '') + i;
      var cell = document.createElement('div');
      cell.className = 'ephemeral-map-cell';
      cell.textContent = num;
      cell.dataset.thesis = num;
      (function(n) {
        cell.addEventListener('click', function() {
          var target = document.getElementById('thesis-' + n);
          if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'center' });
            if (!target.classList.contains('open')) {
              var trig = target.querySelector('.accordion-trigger');
              if (trig) trig.click();
            }
          }
          closeMap();
        });
      })(num);
      ephemeralGrid.appendChild(cell);
    }
    var openMap = function() { ephemeralMap.classList.add('open'); };
    var closeMap = function() { ephemeralMap.classList.remove('open'); };
    document.addEventListener('keydown', function(e) {
      // Не открываем, если пользователь печатает в текстовом поле
      var tag = (e.target.tagName || '').toLowerCase();
      if (tag === 'input' || tag === 'textarea') return;
      if (e.key === 'm' || e.key === 'M' || e.key === 'ь' || e.key === 'Ь') {
        if (ephemeralMap.classList.contains('open')) closeMap();
        else openMap();
      } else if (e.key === 'Escape' && ephemeralMap.classList.contains('open')) {
        closeMap();
      }
    });
    // Клик по фону — закрыть
    ephemeralMap.addEventListener('click', function(e) {
      if (e.target === ephemeralMap) closeMap();
    });
  }
})();
"""
last_script_close = html.rfind('</script>')
assert last_script_close > 0
html = html[:last_script_close] + js + '\n' + html[last_script_close:]

# ============================================================
# СОХРАНИТЬ
# ============================================================
DST.write_text(html, encoding='utf-8')

# ============================================================
# ВАЛИДАЦИЯ
# ============================================================
print(f"✓ Saved: {DST}")
print(f"  Size: {len(html.encode('utf-8')):,} bytes")
print(f"  Lines: {html.count(chr(10)) + 1}")
print()
print("=== TETRAPTYCH STRUCTURE ===")
print(f"  accordion-item:          {html.count('class=\"accordion-item\"')}")
print(f"  id=\"thesis-XX\":           {len(re.findall(r'id=\"thesis-\\d{2}\"', html))}")
print(f"  epistemic-gap:            {html.count('class=\"epistemic-gap\"')}")
print(f"  ariadne-thread:           {html.count('ariadne-thread')}")
print(f"  ariadne-item:             {html.count('ariadne-item')}")
print(f"  contemplative-margin:     {html.count('contemplative-margin')}")
print(f"  progress-thread:          {html.count('progress-thread')}")
print(f"  ephemeral-map:            {html.count('ephemeral-map')}")
print(f"  ephemeral-map-cell:       {html.count('ephemeral-map-cell')}")
print(f"  version-signature:        {html.count('version-signature')}")
print(f"  fovea-focus:              {html.count('fovea-focus')}")
print(f"  v19 mentions:             {html.count('v19')}")
print(f"  clamp() calls:            {html.count('clamp(')}")
print(f"  IntersectionObserver:     {html.count('IntersectionObserver')}")
print()
print("=== KEY MARKERS ===")
print(f"  Title updated:               {'Тетраптих' in html}")
print(f"  Footer updated:              {'тетраптих' in html.lower()}")
print(f"  Screen 3 — Aymara:           {'аймара' in html.split('id=\"screen3\"')[1].split('id=\"screen4\"')[0]}")
print(f"  Reduced motion handler:      {'prefers-reduced-motion' in html}")
print()
print("=== ACADEMIC REFERENCES (sample) ===")
for ref in ['Kandel', 'Levelt', 'Libet', 'Bender', 'Hayakawa', 'Damasio', 'Craig',
            'Brooks', 'Christiano', 'Boroditsky', 'Lupyan', 'Bergen', 'Quine']:
    n = html.count(ref)
    print(f"  {ref:<14} {'✓' if n > 0 else '✗'} ({n})")
