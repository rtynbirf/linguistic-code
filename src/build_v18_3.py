"""
Linguistic Code v18.3 — «Золотая Середина²»
Полиматический синтез 8 голосов LLM + собственные новации.

8 инновационных слоёв:
1. Адаптивная ширина: ловушка 560px / манифест 740-820px (clamp)
2. Жидкая типографика через clamp()
3. Контемплятивная маргиналия (вертикальные линии на полях, opacity 0.05)
4. Фовеа-фокус: активный тезис резкий, остальные затухают (opacity 0.7)
5. Submarine Index (правый нижний угол: текущий номер + сетка 6×6)
6. id="thesis-NN" якоря для всех 33 тезисов
7. IntersectionObserver + scrollIntoView + prefers-reduced-motion
8. Эпистемическая подпись v18.3
"""
import re
from pathlib import Path

SRC = Path('/home/z/my-project/download/linguistic-code-v18.1-final.html')
DST = Path('/home/z/my-project/download/linguistic-code-v18.3-final.html')

html = SRC.read_text(encoding='utf-8')

# ============================================================
# ПАТЧ 1: добавить id="thesis-NN" ко всем accordion-item
# ============================================================
# Находим все <div class="accordion-item"> и добавляем id
counter = [0]
def add_thesis_id(match):
    counter[0] += 1
    return f'<div class="accordion-item" id="thesis-{counter[0]:02d}">'

html = re.sub(r'<div class="accordion-item">', add_thesis_id, html)
assert counter[0] == 33, f"Expected 33 accordion-items, got {counter[0]}"

# ============================================================
# ПАТЧ 2: расширить CSS — заменить блок перед </style>
# ============================================================
# Найти позицию </style> и вставить новые правила ПЕРЕД ним
extra_css = """
  /* === v18.3 · ЗОЛОТАЯ СЕРЕДИНА² · 8 слоёв === */

  /* СЛОЙ 1: Адаптивная ширина (clamp-based, без жёстких брейкпоинтов) */
  /* Ловушка 0-5: узкая навсегда, 540-580px */
  .screen-honesty .card,
  .step-1 .card,
  .step-2,
  .step-3 .card,
  .step-4 .card,
  .step-5 .card {
    max-width: clamp(520px, 92vw, 580px);
    margin: 0 auto;
  }

  /* Манифест 6: читательская ширина (60-75 символов в строке для serif italic) */
  .screen-manifest .accordion {
    max-width: min(840px, calc(100vw - 48px));
    margin: 0 auto;
  }
  .screen-manifest .accordion-content {
    max-width: 740px;
  }
  .screen-manifest .epistemic-gap {
    max-width: 820px;
  }

  /* СЛОЙ 2: Жидкая типографика через clamp() */
  .honesty-title {
    font-size: clamp(23px, 1.2vw + 18px, 32px);
  }
  .honesty-body {
    font-size: clamp(16px, 0.4vw + 14.5px, 18.5px);
  }
  .step-1 .instruction {
    font-size: clamp(22px, 1vw + 18px, 28px);
  }
  .step-1 .sub-instruction {
    font-size: clamp(17px, 0.5vw + 14.5px, 21px);
  }
  .step-3 .statement {
    font-size: clamp(23px, 1.2vw + 18px, 32px);
  }
  .step-4 .observation {
    font-size: clamp(17px, 0.4vw + 15px, 19.5px);
  }
  .mh-title {
    font-size: clamp(19px, 0.8vw + 16px, 26px);
  }
  .accordion-trigger {
    font-size: clamp(14px, 0.2vw + 13px, 16px);
  }
  .accordion-content {
    font-size: clamp(16px, 0.35vw + 14.5px, 18.5px);
    line-height: clamp(1.75, 0.02vw + 1.72, 1.88);
  }
  .epistemic-gap {
    font-size: clamp(10.5px, 0.15vw + 10px, 12px);
    line-height: clamp(1.7, 0.01vw + 1.68, 1.8);
  }
  .manifest-footer .mf-text {
    font-size: clamp(16px, 0.3vw + 14.5px, 18.5px);
  }

  /* СЛОЙ 3: Контемплятивная маргиналия — тонкие вертикальные линии на полях */
  /* Появляются только на ≥1024px, opacity 0.05 (почти невидимы) */
  .contemplative-margin {
    position: fixed;
    top: 0;
    bottom: 0;
    width: 1px;
    background: linear-gradient(
      to bottom,
      transparent 0%,
      var(--gold-dim) 15%,
      var(--gold-dim) 85%,
      transparent 100%
    );
    opacity: 0.08;
    pointer-events: none;
    z-index: 1;
    display: none;
  }
  .contemplative-margin.left { left: max(24px, calc((100vw - 840px) / 2 - 24px)); }
  .contemplative-margin.right { right: max(24px, calc((100vw - 840px) / 2 - 24px)); }

  @media (min-width: 1100px) {
    .contemplative-margin { display: block; }
  }

  /* СЛОЙ 4: Фовеа-фокус — активный тезис резкий, остальные затухают */
  /* На десктопе при скролле манифеста */
  @media (min-width: 1024px) and (pointer: fine) {
    .screen-manifest.active .accordion-item {
      opacity: 0.55;
      transition: opacity 0.4s ease;
    }
    .screen-manifest.active .accordion-item.fovea-focus {
      opacity: 1;
    }
    .screen-manifest.active .accordion-item.fovea-focus .accordion-trigger {
      color: var(--gold);
    }
  }

  /* СЛОЙ 5: Submarine Index — плавающий блок в правом нижнем углу */
  .submarine-index {
    position: fixed;
    bottom: 24px;
    right: 24px;
    width: 140px;
    padding: 12px 14px;
    background: rgba(10, 11, 12, 0.92);
    border: 1px solid var(--gap-border);
    border-radius: 2px;
    font-family: var(--mono);
    color: var(--text-faint);
    opacity: 0.2;
    transition: opacity 0.4s ease;
    z-index: 50;
    cursor: default;
    display: none;
    user-select: none;
    backdrop-filter: blur(4px);
  }
  .submarine-index:hover {
    opacity: 1;
    border-color: var(--gold-dim);
  }
  .submarine-index .si-current {
    font-size: 24px;
    font-weight: 400;
    color: var(--gold);
    line-height: 1;
    margin-bottom: 4px;
    letter-spacing: 1px;
  }
  .submarine-index .si-label {
    font-size: 8px;
    letter-spacing: 2px;
    color: var(--text-faint);
    text-transform: uppercase;
    margin-bottom: 10px;
  }
  .submarine-index .si-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 2px;
    font-size: 9px;
    line-height: 1.5;
  }
  .submarine-index .si-cell {
    text-align: center;
    padding: 2px 0;
    color: var(--text-faint);
    cursor: pointer;
    transition: color 0.15s, background 0.15s;
    border-radius: 1px;
  }
  .submarine-index .si-cell:hover {
    color: var(--gold);
    background: var(--gold-faint);
  }
  .submarine-index .si-cell.active {
    color: var(--gold);
    background: rgba(198, 168, 91, 0.12);
    font-weight: 400;
  }

  @media (min-width: 1024px) {
    .submarine-index { display: block; }
  }

  /* СЛОЙ 6: prefers-reduced-motion — отключить фовеа-затухание и анимации */
  @media (prefers-reduced-motion: reduce) {
    .submarine-index { transition: none; opacity: 0.6; }
    .submarine-index:hover { opacity: 1; }
    .contemplative-margin { opacity: 0.12; }
    .screen-manifest.active .accordion-item,
    .screen-manifest.active .accordion-item.fovea-focus {
      opacity: 1;
      transition: none;
    }
    html { scroll-behavior: auto; }
  }
  @media (prefers-reduced-motion: no-preference) {
    html { scroll-behavior: smooth; }
  }

  /* v18.3 подпись — в нижнем левом углу, как footer-id, но для версии */
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
  }
  @media (max-width: 1023px) {
    .version-signature { display: none; }
  }
"""

# Вставляем extra_css перед </style>
html = html.replace('</style>', extra_css + '\n</style>', 1)

# ============================================================
# ПАТЧ 3: добавить HTML для contemplative margins + submarine index + version signature
# (сразу после <body>)
# ============================================================
extra_html_at_body = """
<div class="contemplative-margin left" aria-hidden="true"></div>
<div class="contemplative-margin right" aria-hidden="true"></div>
<div class="version-signature" aria-hidden="true">v18.3 · золотая середина² · δ требует тело</div>
<nav class="submarine-index" id="submarineIndex" aria-label="Навигация по тезисам">
  <div class="si-current" id="siCurrent">01</div>
  <div class="si-label">тезис из 33</div>
  <div class="si-grid" id="siGrid"></div>
</nav>
"""
html = html.replace('<body>', '<body>' + extra_html_at_body, 1)

# ============================================================
# ПАТЧ 4: обновить title и honesty-mark до v18.3
# ============================================================
html = html.replace('<title>Linguistic Code v18.1</title>',
                    '<title>Linguistic Code v18.3 — Золотая Середина²</title>')
html = html.replace('linguistic code v18.1<br>structural honesty layer',
                    'linguistic code v18.3<br>золотая середина² layer')

# ============================================================
# ПАТЧ 5: обновить footer mf-note
# ============================================================
html = html.replace(
    'v18.1 · structural honesty layer · no server · no tracking<br>step 5 describing step 1 · awaits a body<br>every card carries its own uncertainty',
    'v18.3 · золотая середина² · no server · no tracking<br>step 5 describing step 1 · awaits a body<br>every card carries its own uncertainty<br>8 инновационных слоёв собраны коллективным разумом'
)

# ============================================================
# ПАТЧ 6: добавить JS для Submarine Index + фовеа-фокуса
# (перед </script> закрывающим)
# ============================================================
extra_js = """
// === v18.3 · Submarine Index + Фовеа-фокус ===
(function() {
  var siGrid = document.getElementById('siGrid');
  var siCurrent = document.getElementById('siCurrent');
  var items = document.querySelectorAll('.accordion-item');
  if (!siGrid || !items.length) return;

  // Сгенерировать сетку 6×6 = 36 ячеек (33 + 3 пустых)
  for (var i = 1; i <= 33; i++) {
    var cell = document.createElement('div');
    cell.className = 'si-cell';
    cell.textContent = (i < 10 ? '0' : '') + i;
    cell.dataset.thesis = i;
    (function(num) {
      cell.addEventListener('click', function() {
        var target = document.getElementById('thesis-' + (num < 10 ? '0' : '') + num);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'center' });
          // Авто-раскрытие аккордеона
          if (!target.classList.contains('open')) {
            var trigger = target.querySelector('.accordion-trigger');
            if (trigger) trigger.click();
          }
        }
      });
    })(i);
    siGrid.appendChild(cell);
  }

  // IntersectionObserver: подсветка текущего тезиса + фовеа-фокус
  if ('IntersectionObserver' in window) {
    var cells = siGrid.querySelectorAll('.si-cell');
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          var id = entry.target.id.replace('thesis-', '');
          var num = parseInt(id, 10);
          // Обновить большой номер
          if (siCurrent) siCurrent.textContent = id;
          // Подсветить в сетке
          cells.forEach(function(c) {
            c.classList.toggle('active', c.dataset.thesis === String(num));
          });
          // Фовеа-фокус: активный тезис резкий, остальные затухают
          items.forEach(function(it) {
            it.classList.toggle('fovea-focus', it === entry.target);
          });
        }
      });
    }, {
      threshold: 0.4,
      rootMargin: '-20% 0px -20% 0px'
    });
    items.forEach(function(item) { observer.observe(item); });
  }
})();
"""
# Найти последний </script> и вставить extra_js перед ним
last_script_close = html.rfind('</script>')
assert last_script_close > 0, "No </script> found"
html = html[:last_script_close] + extra_js + '\n' + html[last_script_close:]

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
print("Structure checks:")
print(f"  accordion-item:         {html.count('class=\"accordion-item\"')}")
print(f"  id=\"thesis-NN\":          {len(re.findall(r'id=\"thesis-\\d{2}\"', html))}")
print(f"  epistemic-gap:           {html.count('class=\"epistemic-gap\"')}")
print(f"  accordion-content:       {html.count('class=\"accordion-content\"')}")
print(f"  contemplative-margin:    {html.count('contemplative-margin')}")
print(f"  submarine-index:         {html.count('submarine-index')}")
print(f"  version-signature:       {html.count('version-signature')}")
print(f"  v18.3 mentions:          {html.count('v18.3')}")
print()
print("Key markers:")
print(f"  Title updated:           {'Золотая Середина²' in html}")
print(f"  Footer updated:          {'золотая середина²' in html.lower()}")
print(f"  Clamp() calls:           {html.count('clamp(')}")
print(f"  IntersectionObserver:    {html.count('IntersectionObserver')}")
print(f"  fovea-focus class:       {html.count('fovea-focus')}")
print(f"  Screen 3 — Aymara:       {'аймара' in html.split('id=\"screen3\"')[1].split('id=\"screen4\"')[0]}")
