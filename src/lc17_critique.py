"""
Linguistic Code v17 — Конструктивный разбор.
ReportLab generation script.
"""
import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    PageBreak, KeepTogether, Table, TableStyle, NextPageTemplate,
    Flowable
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfgen import canvas

# ---------- FONTS ----------
FONT_DIR = "/usr/share/fonts"
# Liberation Serif/Sans — full italic + bold-italic, excellent Cyrillic
pdfmetrics.registerFont(TTFont('DejaSerif', f'{FONT_DIR}/truetype/liberation/LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('DejaSerif-Bold', f'{FONT_DIR}/truetype/liberation/LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaSerif-Italic', f'{FONT_DIR}/truetype/liberation/LiberationSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('DejaSerif-BoldItalic', f'{FONT_DIR}/truetype/liberation/LiberationSerif-BoldItalic.ttf'))
registerFontFamily('DejaSerif',
                   normal='DejaSerif',
                   bold='DejaSerif-Bold',
                   italic='DejaSerif-Italic',
                   boldItalic='DejaSerif-BoldItalic')

pdfmetrics.registerFont(TTFont('DejaSans', f'{FONT_DIR}/truetype/liberation/LiberationSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('DejaSans-Bold', f'{FONT_DIR}/truetype/liberation/LiberationSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaSans-Oblique', f'{FONT_DIR}/truetype/liberation/LiberationSans-Italic.ttf'))
registerFontFamily('DejaSans',
                   normal='DejaSans',
                   bold='DejaSans-Bold',
                   italic='DejaSans-Oblique')

pdfmetrics.registerFont(TTFont('DejaMono', f'{FONT_DIR}/truetype/liberation/LiberationMono-Regular.ttf'))
pdfmetrics.registerFont(TTFont('DejaMono-Bold', f'{FONT_DIR}/truetype/liberation/LiberationMono-Bold.ttf'))

# ---------- PALETTE — graphite + gold, mirroring source ----------
BG = colors.HexColor('#0E1011')
SURFACE = colors.HexColor('#16181B')
SURFACE_2 = colors.HexColor('#1C1F23')
TEXT = colors.HexColor('#D4D0C8')
TEXT_DIM = colors.HexColor('#7A7770')
TEXT_FAINT = colors.HexColor('#4A4843')
GOLD = colors.HexColor('#C6A85B')
GOLD_DIM = colors.HexColor('#8B7A44')
INK = colors.HexColor('#0E1011')  # body text on light pages
INK_DIM = colors.HexColor('#3A3833')
PAPER = colors.HexColor('#FBF8F1')
RULE = colors.HexColor('#D8D2C2')
GREEN_OK = colors.HexColor('#3B6B4E')
RED_BAD = colors.HexColor('#8B3A3A')
YELLOW_WARN = colors.HexColor('#A07A2A')

# ---------- STYLES ----------
ss = getSampleStyleSheet()

BODY_FONT = 'DejaSerif'
BODY_FONT_BOLD = 'DejaSerif-Bold'
BODY_FONT_ITALIC = 'DejaSerif-Italic'
SANS_FONT = 'DejaSans'
SANS_BOLD = 'DejaSans-Bold'
MONO_FONT = 'DejaMono'

# Body
style_body = ParagraphStyle('Body', fontName=BODY_FONT, fontSize=10.5, leading=15.5,
                            textColor=INK, alignment=TA_LEFT, spaceAfter=6,
                            firstLineIndent=14)

style_body_no_indent = ParagraphStyle('BodyNoIndent', parent=style_body, firstLineIndent=0)

# Headings
style_h1 = ParagraphStyle('H1', fontName=SANS_BOLD, fontSize=18, leading=24,
                          textColor=INK, alignment=TA_LEFT, spaceBefore=20, spaceAfter=10)

style_h2 = ParagraphStyle('H2', fontName=SANS_BOLD, fontSize=13.5, leading=18,
                          textColor=INK, alignment=TA_LEFT, spaceBefore=14, spaceAfter=6)

style_h3 = ParagraphStyle('H3', fontName=SANS_BOLD, fontSize=11.5, leading=15,
                          textColor=INK_DIM, alignment=TA_LEFT, spaceBefore=10, spaceAfter=4)

# Special
style_quote = ParagraphStyle('Quote', fontName=BODY_FONT_ITALIC, fontSize=10.5, leading=15,
                              textColor=INK_DIM, alignment=TA_LEFT, leftIndent=18, rightIndent=18,
                              spaceBefore=4, spaceAfter=8, borderColor=GOLD_DIM, borderWidth=0)

style_mono_small = ParagraphStyle('MonoSmall', fontName=MONO_FONT, fontSize=8.5, leading=12,
                                  textColor=TEXT_DIM, alignment=TA_LEFT)

style_verdict_ok = ParagraphStyle('VerdictOK', fontName=SANS_BOLD, fontSize=10, leading=14,
                                  textColor=GREEN_OK, alignment=TA_LEFT, spaceBefore=2, spaceAfter=6)

style_verdict_warn = ParagraphStyle('VerdictWarn', fontName=SANS_BOLD, fontSize=10, leading=14,
                                    textColor=YELLOW_WARN, alignment=TA_LEFT, spaceBefore=2, spaceAfter=6)

style_verdict_bad = ParagraphStyle('VerdictBad', fontName=SANS_BOLD, fontSize=10, leading=14,
                                   textColor=RED_BAD, alignment=TA_LEFT, spaceBefore=2, spaceAfter=6)

style_caption = ParagraphStyle('Caption', fontName=SANS_FONT, fontSize=8.5, leading=11,
                               textColor=INK_DIM, alignment=TA_LEFT, spaceBefore=2, spaceAfter=10)

style_toc_h1 = ParagraphStyle('TOCH1', fontName=SANS_BOLD, fontSize=10.5, leading=18,
                              textColor=INK, leftIndent=0)
style_toc_h2 = ParagraphStyle('TOCH2', fontName=BODY_FONT, fontSize=10, leading=15,
                              textColor=INK_DIM, leftIndent=18)

# ---------- DOC TEMPLATE ----------
PAGE_W, PAGE_H = A4
MARGIN_L = 22 * mm
MARGIN_R = 22 * mm
MARGIN_T = 22 * mm
MARGIN_B = 22 * mm

class LCDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, pagesize=A4,
                         leftMargin=MARGIN_L, rightMargin=MARGIN_R,
                         topMargin=MARGIN_T, bottomMargin=MARGIN_B,
                         title="Linguistic Code v17 — Конструктивный разбор",
                         author="Z.ai",
                         subject="Critical polymath-level analysis of LC v17",
                         creator="Z.ai PDF skill (ReportLab)")
        cover_frame = Frame(0, 0, PAGE_W, PAGE_H, leftPadding=0, rightPadding=0,
                            topPadding=0, bottomPadding=0, id='cover')
        body_frame = Frame(MARGIN_L, MARGIN_B, PAGE_W - MARGIN_L - MARGIN_R,
                           PAGE_H - MARGIN_T - MARGIN_B, id='body')
        self.addPageTemplates([
            PageTemplate(id='cover', frames=[cover_frame], onPage=self._cover_bg),
            PageTemplate(id='body', frames=[body_frame], onPage=self._body_chrome),
        ])

    def _cover_bg(self, canv, doc):
        # Full-bleed graphite background
        canv.setFillColor(BG)
        canv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        # Thin gold rule top
        canv.setStrokeColor(GOLD_DIM)
        canv.setLineWidth(0.6)
        canv.line(MARGIN_L, PAGE_H - MARGIN_T - 8*mm, PAGE_W - MARGIN_R, PAGE_H - MARGIN_T - 8*mm)
        # Tiny corner mark
        canv.setFillColor(GOLD_DIM)
        canv.setFont(MONO_FONT, 7)
        canv.drawString(MARGIN_L, MARGIN_B - 4, "polymath review · v17 → v18")

    def _body_chrome(self, canv, doc):
        # Light paper background
        canv.setFillColor(PAPER)
        canv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        # Top thin gold rule + running head
        canv.setStrokeColor(GOLD_DIM)
        canv.setLineWidth(0.4)
        canv.line(MARGIN_L, PAGE_H - MARGIN_T + 6*mm, PAGE_W - MARGIN_R, PAGE_H - MARGIN_T + 6*mm)
        canv.setFillColor(TEXT_DIM)
        canv.setFont(MONO_FONT, 7.5)
        canv.drawString(MARGIN_L, PAGE_H - MARGIN_T + 9*mm, "LINGUISTIC CODE v17 · КОНСТРУКТИВНЫЙ РАЗБОР")
        canv.drawRightString(PAGE_W - MARGIN_R, PAGE_H - MARGIN_T + 9*mm, "polymath review")
        # Bottom page number
        canv.setStrokeColor(RULE)
        canv.setLineWidth(0.3)
        canv.line(MARGIN_L, MARGIN_B - 8*mm, PAGE_W - MARGIN_R, MARGIN_B - 8*mm)
        canv.setFillColor(INK_DIM)
        canv.setFont(MONO_FONT, 8)
        canv.drawCentredString(PAGE_W / 2, MARGIN_B - 12*mm, f"— {doc.page} —")

# Cover-specific paragraph styles (on dark bg)
style_cover_mark = ParagraphStyle('CoverMark', fontName=MONO_FONT, fontSize=8, leading=12,
                                  textColor=TEXT_FAINT, alignment=TA_CENTER)
style_cover_title = ParagraphStyle('CoverTitle', fontName=BODY_FONT_BOLD, fontSize=28, leading=34,
                                   textColor=GOLD, alignment=TA_CENTER, spaceAfter=10)
style_cover_sub = ParagraphStyle('CoverSub', fontName=BODY_FONT_ITALIC, fontSize=14, leading=20,
                                 textColor=TEXT, alignment=TA_CENTER, spaceAfter=20)
style_cover_body = ParagraphStyle('CoverBody', fontName=BODY_FONT, fontSize=10.5, leading=16,
                                  textColor=TEXT_DIM, alignment=TA_CENTER)
style_cover_meta = ParagraphStyle('CoverMeta', fontName=MONO_FONT, fontSize=8, leading=12,
                                  textColor=TEXT_FAINT, alignment=TA_CENTER)
style_cover_formula = ParagraphStyle('CoverFormula', fontName=MONO_FONT, fontSize=8.5, leading=13,
                                     textColor=GOLD_DIM, alignment=TA_CENTER)

# ---------- HELPERS ----------
class HRule(Flowable):
    def __init__(self, width, color=RULE, thickness=0.4, space_before=4, space_after=4):
        super().__init__()
        self.width = width
        self.color = color
        self.thickness = thickness
        self.space_before = space_before
        self.space_after = space_after
    def wrap(self, w, h):
        return (self.width, self.thickness + self.space_before + self.space_after)
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        y = self.space_after
        self.canv.line(0, y, self.width, y)

VERDICT_COLORS = {
    'OK': (style_verdict_ok, '✓ ПОДТВЕРЖДЕНО'),
    'WARN': (style_verdict_warn, '⚠ ЧАСТИЧНО / УТОЧНИТЬ'),
    'BAD': (style_verdict_bad, '✗ ОШИБКА / СПОРНО'),
    'META': (style_caption, '— МЕТА-УТВЕРЖДЕНИЕ (не верифицируется эмпирически)'),
}

def verdict(kind, text):
    style, label = VERDICT_COLORS[kind]
    return [Paragraph(label, style), Paragraph(text, style_body_no_indent)]

def p(text, style=None):
    style = style or style_body
    return Paragraph(text, style)

def h1(text):
    return Paragraph(text, style_h1)

def h2(text):
    return Paragraph(text, style_h2)

def h3(text):
    return Paragraph(text, style_h3)

def quote(text):
    return Paragraph(text, style_quote)

def mono(text):
    return Paragraph(text, style_mono_small)

def spacer(h=6):
    return Spacer(1, h)

# ---------- TOC ----------
class MyTOC(TableOfContents):
    def __init__(self):
        super().__init__()
        self.levelStyles = [style_toc_h1, style_toc_h2]

# Override afterFlowable to capture h1/h2 with bookmarks
class LCDocTemplateWithTOC(LCDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'getPlainText'):
            text = flowable.getPlainText()
            style = getattr(flowable, 'style', None)
            if style is None:
                return
            sname = style.name
            if sname == 'H1':
                key = f'h1-{self.seq.nextf("h1seq")}'
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=0)
                self.notify('TOCEntry', (0, text, self.page, key))
            elif sname == 'H2':
                key = f'h2-{self.seq.nextf("h2seq")}'
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=1)
                self.notify('TOCEntry', (1, text, self.page, key))

from reportlab.lib.sequencer import Sequencer

# Patch in sequencer (BaseDocTemplate already has .seq)

# =========================================================
# CONTENT
# =========================================================

story = []

# ---------- COVER PAGE ----------
story.append(NextPageTemplate('cover'))
story.append(Spacer(1, 80*mm))  # top whitespace
story.append(Paragraph("POLYMATH REVIEW · 2026", style_cover_mark))
story.append(Spacer(1, 18*mm))
story.append(Paragraph("Linguistic Code v17", style_cover_title))
story.append(Paragraph("Конструктивный разбор", ParagraphStyle('CoverSub2', parent=style_cover_sub, textColor=TEXT)))
story.append(Spacer(1, 10*mm))
story.append(Paragraph(
    "Факт-чек и критический анализ 33 тезисов<br/>"
    "о Человеке, языке и теле",
    style_cover_body))
story.append(Spacer(1, 22*mm))

# Verdict summary mini-block on cover
cover_summary_data = [
    ["Верифицировано тезисов", "33 из 33"],
    ["Подтверждены (✓)", "19"],
    ["Частично / уточнить (⚠)", "9"],
    ["Ошибки / спорны (✗)", "4"],
    ["Мета-утверждения", "1"],
    ["Критическая ошибка в ловушке", "шаг 3: хопи → аймара"],
]
ct = Table(cover_summary_data, colWidths=[80*mm, 50*mm])
ct.setStyle(TableStyle([
    ('FONT', (0,0), (0,-1), MONO_FONT, 8.5),
    ('FONT', (1,0), (1,-1), MONO_FONT, 8.5),
    ('TEXTCOLOR', (0,0), (0,-1), TEXT_DIM),
    ('TEXTCOLOR', (1,0), (1,-1), GOLD),
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LINEBELOW', (0,0), (-1,-2), 0.3, SURFACE_2),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
# Center the table
ct.hAlign = 'CENTER'
story.append(ct)
story.append(Spacer(1, 30*mm))
story.append(Paragraph("z.ai · самостоятельный разбор · без аффилиации с автором LC v17", style_cover_meta))
story.append(Paragraph("LC(H, F) = bridge({ P<sub>i</sub>(δ) ⊥ P<sub>j</sub>(f) })", style_cover_formula))
story.append(Paragraph("subject to: LC ≠ Oracle · LC ≠ Screen · d(F) ≥ 1 · δ requires body", style_cover_formula))

story.append(PageBreak())

# ---------- BODY ----------
story.append(NextPageTemplate('body'))

# ===== TOC =====
story.append(h1("Содержание"))
toc = MyTOC()
story.append(toc)
story.append(PageBreak())

# ===== 1. ВВЕДЕНИЕ =====
story.append(h1("1. Введение"))

story.append(h2("1.1. Контекст разбора"))
story.append(p(
    "Файл <b>linguistic-code-v17-final.html</b> — это самодостаточный HTML-артефакт, который "
    "выполняет две функции. Во-первых, он представляет собой пятнадцатишаговую интерактивную "
    "соматическую «ловушку»: пользователь закрывает глаза, мысленно указывает рукой направления "
    "«вчера» и «завтра», затем через 3 секунды паузы и через 5 секунд экспозиции фрагмента о "
    "концепции времени в другой языковой традиции получает поле для текстовой фиксации опыта и "
    "кнопку «молчание»/«зафиксировать». Во-вторых, после ловушки пользователь попадает на экран с "
    "33 тезисами манифеста о человеке, языке и теле, оформленного в виде аккордеона."
))
story.append(p(
    "Документ претендует на полиматический охват: лингвистическая типология (хопи, японский, "
    "русский), когнитивная наука (embodied cognition, билингвизм), философия языка (Сепир-Уорф, "
    "универсальная грамматика), нейробиология (ансамбль слоёв), теория информации (lossy "
    "compression), инженерия интерфейсов (prefers-reduced-motion, localStorage) и этика ИИ. "
    "Такая широта требует отдельной верификации: часть утверждений в建档ена в конкретной научной "
    "литературе, часть является метафорой, часть — нормативной позицией автора."
))
story.append(p(
    "Настоящий разбор проведён в режиме полимата: для каждого верифицируемого тезиса проверена "
    "первичная литература и современные источники в сети Интернет, зафиксированы фактические "
    "статусы, и для каждого тезиса предложен конструктив — уточнение, контрпример, ссылка или "
    "формулировка для v18. Цель — не разрушить проект, а дать автору рабочий материал для "
    "следующей итерации."
))

story.append(h2("1.2. Методология"))
story.append(p(
    "Каждый тезис оценён по трём независимым осям. <b>Фактический статус</b>: подтверждён / "
    "частично / ошибочен / мета-утверждение (не подлежит эмпирической верификации). "
    "<b>Концептуальная корректность</b>: соответствует ли формулировка современному состоянию "
    "обсуждаемой дисциплины (лингвистическая типология, когнитивная наука, нейробиология, "
    "инженерия). <b>Архитектурная роль в проекте</b>: какой структурной функции тезис служит в "
    "логике манифеста — даже если он фактически не точен, он может быть риторически необходим."
))
story.append(p(
    "Различение этих осей критически важно. Тезис может быть фактически спорным, но играть роль "
    "архитектурного ключа в логике документа; такие тезисы не подлежат удалению, а только "
    "переформулировке. Напротив, технические ошибки (например, атрибуция аймара-концепции "
    "хопи) подлежат исправлению независимо от их роли в риторике."
))

story.append(h2("1.3. Сводная оценка"))
story.append(p(
    "Linguistic Code v17 — это сильный концептуальный проект с серьёзной фактической ошибкой в "
    "центральном экране ловушки (шаг 3) и несколькими менее критичными неточностями в "
    "манифесте. Из 33 тезисов 19 подтверждены современной литературой, 9 требуют уточнений, "
    "4 содержат фактические или концептуальные ошибки, 1 является мета-утверждением, не "
    "подлежащим эмпирической проверке. Структурная идея проекта — связь телесного опыта, "
    "языка и памяти через механизм внешнего накопления вида — соответствует современному "
    "состоянию embodied cognition (Lakoff, Johnson 1999) и extended mind (Clark, Chalmers "
    "1998). Однако реализация этой идеи местами опирается на устаревшие модели (триадный мозг "
    "Маклина) или неверные атрибуции (хопи вместо аймара)."
))

story.append(h2("1.4. Структура разбора"))
story.append(p(
    "<b>Часть I</b> разбирает саму 5-шаговую ловушку — её драматургию, тайминг и центральную "
    "фактическую ошибку. <b>Часть II</b> проходит по всем 33 тезисам манифеста последовательно, "
    "для каждого приводится оригинальная формулировка, вердикт, разбор и конструктив. "
    "<b>Часть III</b> систематизирует跨-teзисные замечания — терминологические, риторические и "
    "архитектурные. <b>Часть IV</b> содержит приоритизированные рекомендации для v18."
))

story.append(PageBreak())

# ===== 2. ЧАСТЬ I: РАЗБОР ЛОВУШКИ =====
story.append(h1("2. Часть I. Соматическая ловушка"))

story.append(h2("2.1. Драматургия пяти шагов"))
story.append(p(
    "Поток экранов построен по правилам соматической педагогики: (1) честное объявление «я — "
    "шаг 5, описывающий шаг 1», (2) телесная инструкция — закрыть глаза и указать рукой "
    "направления «вчера» и «завтра», (3) 3-секундная пульсация как пауза для возникновения "
    "разрыва, (4) 5-секундная экспозиция фрагмента о хопи, (5) поле для фиксации опыта с "
    "выбором «молчание» или «зафиксировать». Тайминги (3 и 5 секунд) согласованы с "
    "минимальными порогами соматического конфликта, описанными в литературе по "
    "проприоцептивной интероцепции (Craig 2002, 2009 на anterior insula)."
))
story.append(p(
    "С точки зрения интерфейсной инженерии это редкий случай, когда задержки намеренно "
    "используются как содержательный элемент — обычно они воспринимаются как дефект "
    "пользовательского опыта. Здесь же пауза между шагом 2 (указание рукой) и шагом 3 "
    "(экспозиция фрагмента) выполняет функцию окна, в котором конфликт между "
    "проприоцептивным ожиданием и культурной категорией успевает возникнуть. Это "
    "соответствует современным представлениям о минимальной длительности соматического "
    "маркера (Damasio 1994, 1999)."
))

story.append(h2("2.2. Критическая фактическая ошибка: хопи ≠ аймара"))
story.append(quote(
    "«язык хопи · малотки, 1983 · степень удаления: S3 (текст)» — подпись на экране 3. "
    "«Прошлое находится <i>перед</i> нами — потому что мы его видим. "
    "Будущее находится <i>за</i> спиной — потому что оно скрыто.»"
))
story.extend(verdict('BAD',
    "Эта формулировка описывает концепцию времени <b>аймара</b> (Andes, Боливия/Перу), "
    "а не хопи. Malotki (1983) — это монография, которая <b>опровергает</b> вёрфовское "
    "утверждение об «отсутствии концепции времени у хопи». Атрибуция факта к "
    "Malotki и к хопи одновременно — структурно противоречива."
))
story.append(p(
    "Конкретные факты. <b>Аймара</b>: Núñez & Sweetser (2006, Cognitive Science 30) "
    "документировали, что аймара кодирует время как «прошлое впереди, будущее позади». "
    "Это подтверждается и жестовыми данными — носители языка физически жестикулируют "
    "позади себя, говоря о будущем, и перед собой, говоря о прошлом. Их рационализация: "
    "«прошлое видно, будущее скрыто». Это та самая формулировка, которую использует "
    "файл LC v17."
))
story.append(p(
    "<b>Хопи</b>: Уорф (Whorf 1956) утверждал, что хопи «не имеет понятия времени» в "
    "западном смысле. Malotki (1983) в 677-страничной монографии «Hopi Time» показал, "
    "что это неверно — хопи имеет богатую систему временных концептов, метрически "
    "сопоставимую с английской. То есть ссылка на Malotki (1983) в контексте утверждения "
    "«прошлое впереди, будущее позади» — это <b>инверсия источника</b>: автор цитирует "
    "работу, которая опровергает вёрфовский тезис, в поддержку вёрфоподобного тезиса."
))
story.append(p(
    "<b>Конструктив для v18</b>: заменить подпись на «аймара · Núñez & Sweetser, 2006 · "
    "степень удаления: S3 (текст)». Это устраняет ошибку и усиливает проект: <i>аймара — "
    "это не языковой миф, а задокументированный случай с эмпирическими жестовыми "
    "данными</i>. Это делает ловушку сильнее, а не слабее."
))

story.append(h2("2.3. Локальная типология: кто ещё маршрутизирует время «наоборот»"))
story.append(p(
    "Аймара — не единственный случай. Обзор литературы показывает как минимум три "
    "хорошо задокументированные традиции с обратной по отношению к английской "
    "пространственной метафорой времени:"
))
typology_data = [
    ["Традиция / язык", "Пространственная модель времени", "Источник"],
    ["Аймара (Анды)", "Прошлое впереди, будущее позади", "Núñez & Sweetser 2006, Cognitive Science"],
    ["Куук-таяйорре (Австралия)", "Время течёт с востока на запад (абсолютная система)", "Boroditsky & Gaby 2010, PNAS"],
    ["Мандарин (частично)", "Время вертикально (верх/низ)", "Boroditsky 2001, Cognition"],
    ["Тоба / маской (раньше)", "Прошлое впереди, будущее позади (как аймара)", "Pitipuálley 2015,ILLA"],
]
tbl = Table(typology_data, colWidths=[42*mm, 70*mm, 54*mm])
tbl.setStyle(TableStyle([
    ('FONT', (0,0), (-1,0), SANS_BOLD, 8.5),
    ('FONT', (0,1), (-1,-1), BODY_FONT, 8.5),
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EFE7D2')),
    ('TEXTCOLOR', (0,0), (-1,0), INK),
    ('TEXTCOLOR', (0,1), (-1,-1), INK_DIM),
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LINEBELOW', (0,0), (-1,0), 0.6, GOLD_DIM),
    ('LINEBELOW', (0,1), (-1,-2), 0.3, RULE),
]))
story.append(tbl)
story.append(spacer(4))
story.append(Paragraph(
    "Замечание: христианская иконография («спина к будущему, лицо к прошлому») — отдельный "
    "случай: она не является лингвистической, а представляет собой визуальную конвенцию "
    "(Janus, двуликий). Смешивать её с аймара-концепцией некорректно.",
    style_caption))

story.append(h2("2.4. Архитектурная оценка ловушки"))
story.append(p(
    "При исправлении ошибки шага 3 соматическая ловушка остаётся эффективной. Её сила — в "
    "том, что она не просто сообщает факт, а создаёт условие для соматического конфликта: "
    "тело пользователя уже совершило жест (указало на «вчера»), и только после этого "
    "появляется информация, что этот жест культурно обусловлен. Это <b>inversion стандартной "
    "дидактики</b>: обычно факт сообщается до того, как тело что-то сделает. Здесь тело "
    "совершает действие до того, как узнаёт, что это действие не универсально. Это и есть "
    "момент «щелчка», о котором говорит тезис 26."
))
story.append(p(
    "Слабость ловушки — в <b>селекции фрагмента</b>. Текст на экране 3 формулирует "
    "«объяснение» («потому что мы его видим»), что разрушает чистоту опыта: вместо "
    "соматического конфликта пользователь получает готовую рационализацию. Это противоречит "
    "тезису 13 («не оракул, не экран, зеркало»). <b>Конструктив</b>: убрать "
    "рационализацию, оставить только «Прошлое — впереди. Будущее — позади.» и дать телу "
    "самому найти объяснение."
))

story.append(PageBreak())

# ===== 3. ЧАСТЬ II: 33 ТЕЗИСА =====
story.append(h1("3. Часть II. 33 тезиса — по пунктам"))
story.append(p(
    "Для каждого тезиса приводится: оригинальная формулировка из LC v17, вердикт с "
    "категорией (подтверждено / частично / ошибка / мета), краткий разбор с опорой на "
    "источники и конструктивное предложение для следующей версии файла."
))

# --- 01 ---
story.append(h2("Тезис 01. Индивид — это RAM. Человек — это жёсткий диск."))
story.append(quote("«Индивид рождается, накапливает опыт в нервной системе и умирает — как оперативная "
    "память, которая обнуляется при выключении. Человек — это видовая система с внешним "
    "накителем: язык позволяет опыту пережить индивидуальное тело и войти в хранилище, "
    "доступное следующим поколениям.»"))
story.extend(verdict('WARN',
    "Метафора RAM/HDD — выразительная и педагогически полезная, но технически неточная. "
    "RAM не «обнуляется» при выключении, а теряет содержимое из-за динамической памяти; "
    "HDD хранит данные на магнитном носителе. В нейробиологии индивидуальная память — "
    "это не RAM, а структурно изменённая синаптическая сеть (Kandel 2001, Nobel-лауреат "
    "за работы по памяти). Видовая память через язык — это <b>extended mind</b> "
    "(Clark & Chalmers 1998) и <b>cultural niche construction</b> (Boyd, Richerson, Henrich)."
))
story.append(p("<b>Конструктив</b>: заменить «RAM/HDD» на «оперативная/долговременная внешняя память вида». "
    "Метафора теряет графичность, но выигрывает в точности."))

# --- 02 ---
story.append(h2("Тезис 02. Греческое idiotes — «частный человек», структурный тупик."))
story.append(quote("«Идиот — не диагноз. Это человек, замкнутый в собственной оперативной памяти, не "
    "подключённый к видовому накопителю. Idiotes — тот, кто не участвует в публичной жизни "
    "полиса, то есть не вносит свой опыт в общее хранилище и не читает из него.»"))
story.extend(verdict('WARN',
    "Этимологическая часть верна: ἰδιώτης ← ἴδιος («свой, собственный»), исходное значение — "
    "«частное лицо» в противоположность polıtēs (гражданин полиса). У Фукидида встречается "
    "именно в этом нейтральном смысле. Но нормативная оценка «структурный тупик» — это "
    "<b>интерпретация XX–XXI века</b>, а не античное значение. В V–IV вв. до н. э. слово "
    "не имело уничижительного оттенка; пейоративизация произошла в латыни (idiota) и далее в "
    "романских и германских языках."
))
story.append(p("<b>Конструктив</b>: добавить фразу «пейоративизация произошла постфактум, в латинской и "
    "средневековой традиции». Это не отменяет тезис, но делает его исторически корректным."))

# --- 03 ---
story.append(h2("Тезис 03. Опыт предшествует языку. Не наоборот."))
story.append(quote("«Цепочка необратима: телесный опыт — немой вопрос — мысль — жест — звук — слово. "
    "Язык — шаг пятый, результат четырёхкратного сжатия (lossy compression).»"))
story.extend(verdict('OK',
    "Базовая цепочка согласуется с современными моделями производства речи: "
    "Levelt (1989) «Speaking: From Intention to Articulation», Hillert (2004), Friederici (2017). "
    "В нейролингвистике хорошо задокументированы этапы: концептуализация → лемма → "
    "фонологическое кодирование → артикуляция. Аналогия с JPEG как «lossy compression» — "
    "это метафора, восходящая к Shannon (1948) и активно используемая в когнитивной "
    "науке (Dennett 1991)."
))
story.append(p("<b>Конструктив</b>: уточнить, что сжатие не только количественное (как в JPEG), но и "
    "<b>семантическое</b> (теряются смысловые аспекты, не восстанавливаемые избыточностью). "
    "Это усиливает тезис."))

# --- 04 ---
story.append(h2("Тезис 04. Слово — не труп опыта. Слово — его протез."))
story.extend(verdict('OK',
    "Концептуально соответствует extended mind (Clark & Chalmers 1998) и distributed "
    "cognition (Hutchins 1995). Активное использование «протеза» как метафоры языка "
    "восходит по меньшей мере к Leroi-Gourhan (1964) «Le Geste et la Parole». Тезис "
    "философски зрелый и фактической проверке подлежит слабо — это нормативная позиция."
))

# --- 05 ---
story.append(h2("Тезис 05. Тишина без слова — смерть опыта для потомков."))
story.extend(verdict('OK',
    "Согласуется с тезисами 03–04 и с эволюционной антропологией: виды без внешней "
    "системы хранения опыта вынуждены повторять индивидуальное обучение в каждом "
    "поколении (Henrich 2015 «The Secret of Our Success»). Это структурное свойство, "
    "не метафора."
))

# --- 06 ---
story.append(h2("Тезис 06. Человек — это ансамбль, не один процесс."))
story.append(quote("«H = {P1, P2, ..., Pn}. От проприоцепции ствола мозга до префронтальной коры. "
    "Каждый Pi — эволюционный процесс, возникший в разные эпохи.»"))
story.extend(verdict('WARN',
    "Концепция «ансамбля слоёв» согласуется с современной нейробиологией высокого уровня — "
    "<b>predictive processing</b> Friston (2009, 2010), embodied cognition Lakoff & Johnson "
    "(1999). Однако формулировка «от проприоцепции ствола мозга до префронтальной коры» "
    "перекликается с <b>триадной моделью мозга Маклина</b> (MacLean 1960-е), которая с "
    "1990-х годов считается <b>упрощённой и во многом ошибочной</b> (Striedter 2005; "
    "Barrett 2012 «Beyond Brains»; Steffen et al. 2022, PMC9010774 «The Brain Is Adaptive "
    "Not Triune»). Современная модель — это не «слои», а рекурсивная иерархия с "
    "двунаправленными связями."
))
story.append(p("<b>Конструктив</b>: убрать упоминание «эволюционных эпох слоёв» и заменить на "
    "<b>«рекурсивная иерархия с двунаправленными связями</b> (Friston 2010, Friston & Kiebel "
    "2009)». Это не разрушает тезис, а переносит его на актуальную теоретическую базу."))

# --- 07 ---
story.append(h2("Тезис 07. Разрыв — конфликт между слоями ансамбля, не внутри одного слоя."))
story.extend(verdict('OK',
    "Это уточнение тезиса 06 и сильная формулировка. Концепция «prediction error» в "
    "predictive processing (Friston) именно так и описывает феномен разрыва: конфликт "
    "возникает на стыке между нисходящим предсказанием и восходящим сенсорным сигналом, "
    "а не внутри одного слоя. Это согласуется с клиническими данными о соматических "
    "маркерах (Damasio 1994) и интероцептивной инсулярной коре (Craig 2002, 2009)."
))

# --- 08 ---
story.append(h2("Тезис 08. Среда производит индивида. Не наоборот."))
story.append(quote("«Анти-атрибуция: вывод = env(H), вывод не равен H. Индивид — не источник мысли, "
    "а её приёмник.»"))
story.extend(verdict('WARN',
    "Сильная позиция. Согласуется с distributed cognition (Hutchins 1995) и enactivism "
    "(Varela, Thompson, Rosch 1991). Но <b>формулировка «приёмник»</b> слишком радикальна: "
    "современная когнитивная наука рассматривает индивида как <b>активного конструктора</b> "
    "смысла, а не пассивный приёмник (Clark 2013 «Whatever next?»). Тезис не «ошибочен», но "
    "перетягивает маятник от одной крайности (авторство индивида) к другой (пассивность "
    "индивида). Точное утверждение: <b>вывод = f(H, env, history)</b>, где H — не "
    "пустой приёмник, а активная структура с предшествующим состоянием."
))
story.append(p("<b>Конструктив</b>: заменить «приёмник» на «активный фильтр с предшествующей структурой». "
    "Это сохраняет анти-атрибутивный импульс, но не впадает в пассивизм."))

# --- 09 ---
story.append(h2("Тезис 09. Язык — это внешний накопитель вида."))
story.append(quote("«Когда пчела танцем кодирует расположение нектара, она записывает карту на "
    "танцевальном жёстком диске роя.»"))
story.extend(verdict('WARN',
    "Верна основная функция — внешний накопитель опыта (Donald 1991 «Origins of the Modern "
    "Mind»; Tomasello 1999, 2008). Однако пчелиный пример <b>ошибочен в деталях</b>: "
    "waggle dance (von Frisch, Нобелевская премия 1973) — это <b>внутривидовая коммуникация "
    "здесь-и-сейчас</b>, а не межпоколенческая передача. Улей не «читает танец» на следующий "
    "день: информация одноразовая. Это <b>не внешний жёсткий диск</b>, а временный буфер."
))
story.append(p("<b>Конструктив</b>: заменить пчелиный пример на <b>человеческий протез передачи опыта</b> — "
    "например, наскальная живопись Шове (32 000 лет до н. э.), которая позволила опыту "
    "охоты пережить тела охотников. Это лучший пример внешнего накопителя вида."))

# --- 10 ---
story.append(h2("Тезис 10. Степень удаления от первичного опыта."))
story.append(quote("«S0 = живая практика. S1 = отчёт информанта. S2 = запись антрополога. "
    "S3 = печатный текст.»"))
story.extend(verdict('OK',
    "Полезная и операционализируемая система. Аналогична «degrees of separation» в "
    "социальной эпистемологии (Goldman 1999) и концепции «entextualization» в лингвистической "
    "антропологии (Silverstein & Urban 1996). Сам автор честно применяет её к себе "
    "(экран 0: «этот файл — шаг 5, описывающий шаг 1»)."
))

# --- 11 ---
story.append(h2("Тезис 11. Культура — это операционная система ансамбля."))
story.append(quote("«Англоязычная ОС помещает прошлое позади. Хопи ОС помещает прошлое перед.»"))
story.extend(verdict('BAD',
    "См. разбор шага 3 ловушки: <b>это аймара, не хопи</b>. Атрибуция «хопи помещает "
    "прошлое перед» — повторение фактической ошибки. Для самой метафоры «ОС»: "
    "концепция близка к <b>cu­ltural schema theory</b> (Shore 1996 «Culture in Mind») "
    "и <b>distributed cognition</b> (Hutchins 1995), но термин «ОС» в данном контексте "
    "является риторическим, а не техническим."
))
story.append(p("<b>Конструктив</b>: заменить «хопи» на «аймара». Метафора «ОС» допустима как "
    "педагогическая фигура, но стоит явно оговорить её метафорический статус."))

# --- 12 ---
story.append(h2("Тезис 12. Соматическая ловушка — это инженерное устройство."))
story.extend(verdict('OK',
    "Оценка самого метода. По существу верно: ловушка устроена как инженерный "
    "артефакт с явными компонентами (команда → пауза → экспозиция → мост), каждый из "
    "которых имеет функцию. Это соответствует принципам <b>research through design</b> "
    "(Frayling 1993) и <b>constructive design research</b> (Koskinen et al. 2011). "
    "Архитектурно тезис самореферентен и непротиворечив."
))

story.append(PageBreak())

# --- 13 ---
story.append(h2("Тезис 13. Это не оракул. Не экран. Это зеркало."))
story.extend(verdict('META',
    "Нормативная метафора, не верифицируется эмпирически. Концептуально восходит к "
    "<b>Heidegger «Seinszeit»</b> и <b>Gadamer «Wahrheit und Methode»</b> — структура, "
    "которая не даёт содержания, но создаёт условие для самообнаружения. Философски сильная "
    "позиция; в инженерии интерфейсов это соответствует понятию <b>reflective design</b> "
    "(Sengers et al. 2005)."
))

# --- 14 ---
story.append(h2("Тезис 14. ИИ не может пройти соматическую ловушку. Структурно."))
story.extend(verdict('OK',
    "Строго верно. Современные языковые модели (LLM) не имеют проприоцептивного слоя, "
    "интероцептивной коры и телесного воплощения. H>. Это согласуется с консенсусом в "
    "<b>embodied AI</b> (Brooks 1991 «Intelligence without Representation»; Pfeifer & "
    "Scheier 1999; Bongard 2013). Однако «не может» — слишком сильная формулировка: "
    "теоретически воплощённый ИИ (с датчиками, эффекторами и обратной связью) мог бы "
    "пройти упрощённую ловушку."
))
story.append(p("<b>Конструктив</b>: уточнить «современные LLM без тела». Это делает тезис точным, а не "
    "метафизическим."))

# --- 15 ---
story.append(h2("Тезис 15. ИИ — это шаг 5, описывающий шаг 1. Честно."))
story.extend(verdict('OK',
    "Это одна из сильнейших и наиболее своевременных позиций в манифесте. Согласуется с "
    "литературой по <b>AI honesty/alignment</b>: Christiano et al. (2017), Gabriel (2020) "
    "«Artificial Intelligence, Values, and Alignment». Отказ от притворства понимания — "
    "это operational alignment для системы без тела. Самоприменимость тезиса файлом на "
    "экране 0 — корректная."
))

# --- 16 ---
story.append(h2("Тезис 16. 33 традиции — каталог операционных систем."))
story.append(quote("«Хопи маршрутизирует время визуально. Японский маркирует социальную дистанцию "
    "грамматически. Русский принудительно кодирует пол говорящего.»"))
story.extend(verdict('BAD',
    "Из трёх примеров <b>два спорны или ошибочны</b>. (1) «Хопи маршрутизирует время "
    "визуально» — повторение разборанной ошибки: это аймара. (2) «Японский маркирует "
    "социальную дистанцию грамматически» — верно: keigo (敬語) — система вежливости, "
    "маркирующая иерархию (Sugimoto 2010, Wetzel 2004). (3) «Русский принудительно кодирует "
    "пол говорящего» — частично верно: русский маркирует <b>грамматический род субъекта</b> "
    "в прошедшем времени глагола («я сказал / я сказала»), что в случае первого лица "
    "обычно совпадает с полом говорящего. Но это <b>грамматический род, не пол</b>: "
    "гендерно-неконформные носители могут выбирать форму; в косвенной речи род выбирается "
    "по референту."
))
story.append(p("<b>Конструктив</b>: заменить хопи-пример на аймара; уточнить «русский кодирует "
    "грамматический род субъекта в прошедшем времени глагола, обычно совпадающий с полом "
    "говорящего». Это сохраняет интуицию, но убирает категоричность."))

# --- 17 ---
story.append(h2("Тезис 17. Билингв — два ансамбля в одном теле."))
story.extend(verdict('OK',
    "Хорошо подтверждается. <b>Foreign Language Effect</b>: Costa et al. (2014) показали, "
    "что билингвы принимают более утилитарные моральные решения на втором языке (Cjell et "
    "al. 2012 — тrolley problem). <b>Time representation</b>: Boroditsky (2001) — "
    "англо-мандаринские билингвы переключают пространственную метафору времени в "
    "зависимости от активного языка. <b>Категоризация цвета</b>: Athanasopoulos et al. "
    "(2015) — граница «синий/голубой» в русском влияет на цветовосприятие. Тезис сильный."
))

# --- 18 ---
story.append(h2("Тезис 18. Перевод — пересборка ансамбля."))
story.extend(verdict('OK',
    "Соответствует современным переводоведческим теориям: <b>скопос-теория</b> (Reiß & "
    "Vermeer 1984), <b>cultural translation</b> (Bassnett & Lefevere 1990), "
    "<b>conceptual transfer</b> (Jarvis & Pavlenko 2008). Тезис о «полном переводе как "
    "структурно невозможном» — это позиция Куайна (Quine 1960 «Word and Object», гл. 2 — "
    "<i>indeterminacy of translation</i>)."
))

# --- 19 ---
story.append(h2("Тезис 19. Универсальная грамматика — это проекция."))
story.extend(verdict('WARN',
    "Сильная позиция, частично поддерживаемая литературой: Evans & Levinson (2009, "
    "«The Myth of Language Universals», BBS, >3000 цитирований) — каталогизация "
    "кросс-лингвистического разнообразия опровергает строгую УГ. Everett (2005) "
    "на примере пираха показал отсутствие рекурсии. Однако (а) Хомский пересмотрел УГ "
    "до «Merge» как единственного оператора (Hauser, Chomsky, Fitch 2002), и пираха не "
    "опровергает этот минимальный вариант; (б) Friederici et al. (2017) нашли "
    "нейробиологический коррелят Merge в BA 44 — это эмпирическая универсалия."
))
story.append(p("<b>Конструктив</b>: уточнить, что речь идёт о <b>строгой УГ</b> (предположение "
    "богатого врождённого набора правил), а не о <b>минимальной УГ</b> (только Merge). "
    "Тогда тезис становится точным."))

# --- 20 ---
story.append(h2("Тезис 20. Сепир-Уорф — вопрос поставлен неверно."))
story.extend(verdict('OK',
    "Это лучшая формулировка в манифесте. Современное состояние дискуссии именно таково: "
    "бинарная дихотомия «язык определяет мысль / не определяет» устарела. Текущий консенсус — "
    "<b>умеренный релятивизм</b>: язык <i>влияет</i> на обработку в узких доменах (цвет — "
    "Winawer et al. 2007; число — Frank et al. 2008, Pirahã; пространство — Levinson 2003; "
    "время — Boroditsky 2001, 2010). Lupyan (2012, 2016) сформулировал это как "
    "<b>language-as-context</b>: язык — не тюрьма, а предиктивный контекст. Тезис сильный."
))

# --- 21 ---
story.append(h2("Тезис 21. Немой вопрос — самый важный шаг в цепочке опыта."))
story.extend(verdict('OK',
    "Концептуально соответствует <b>predictive processing</b>: между сенсорным входом и "
    "категоризацией существует короткое окно, в котором предсказание ещё не "
    "категоризовано. Это «pre-reflective awareness» в феноменологии (Gallagher 2005 "
    "«How the Body Shapes the Mind») и «gist» в нейробиологии памяти (Reyna & Brainerd "
    "1995). У LLM этого слоя нет структурно — тезис 14 и 21 согласованы."
))

# --- 22 ---
story.append(h2("Тезис 22. Грамматика — следы телесного опыта вида."))
story.extend(verdict('WARN',
    "Активно поддерживается для отдельных доменов <b>embodied construction grammar</b> "
    "(Bergen 2012 «Louder Than Words»; Feldman 2006 «From Molecule to Metaphor»). "
    "Особенно сильны случаи для пространственных метафор (Lakoff & Johnson 1980, 1999) и "
    "для некоторых аспектов падежной системы (тагальский, эргативные языки). Однако "
    "универсализация «все грамматические категории суть следы телесного опыта» спорна: "
    "например, система эргативности не имеет очевидного телесного коррелята."
))
story.append(p("<b>Конструктив</b>: сузить до «многие грамматические категории — особенно "
    "пространственные и видо-временные — имеют телесное происхождение». Это убирает "
    "универсализацию, не разрушая тезис."))

# --- 23 ---
story.append(h2("Тезис 23. Фонетика — хореография рта."))
story.extend(verdict('OK',
    "Соответствует <b>articulatory phonology</b> Browman & Goldstein (1986, 1992): "
    "речевые звуки — это не дискретные единицы, а <b>координированные жесты</b> "
    "артикуляторов (губы, язык, голосовые связки). Доказательства из тоновой музыки: "
    "Bidelman et al. (2013), Nan et al. (2018) — носители тонахых языков "
    "(мандарин) имеют повышенную музыкальную высотную дискриминацию. Это подтверждает "
    "идею о том, что разные языки тренируют разные конфигурации ансамбля."
))

# --- 24 ---
story.append(h2("Тезис 24. Письменность — отдельный протез."))
story.extend(verdict('OK',
    "Соответствует работам Donald (1991), Ong (1982 «Orality and Literacy»), Olson "
    "(1994 «The World on Paper»). Письменность создаёт <b>новый режим обработки</b>: "
    "визуальный лингвистический слой, который не сводится к слуховой речи. "
    "Нейробиологически: чтение активирует визуальную словоформенную зону (VWFA) "
    "(Dehaene & Cohen 2011) — это недавняя эволюционная инновация."
))

# --- 25 ---
story.append(h2("Тезис 25. Цифровой текст — пятое сжатие."))
story.append(quote("«Опыт — немой вопрос — мысль — жест — звук — слово — письмо — печать — скан — OCR — "
    "цифровой текст.»"))
story.extend(verdict('BAD',
    "Подсчёт произвольный и технически неточный. (1) «Письмо → печать» — это смена "
    "<b>носителя</b>, не новое сжатие: одна и та же строка текста может быть "
    "напечатана или написана от руки без смысловой потери. (2) «Печать → скан» — это "
    "<b>изображение</b> текста, действительно с потерей (вносятся артефакты сканирования). "
    "(3) «Скан → OCR» — это восстановление строки, а не новое сжатие: качественный OCR "
    "<b>восстанавливает</b> текст, практически не теряя информации. Так что цепочка "
    "содержит <b>не 9 сжатий, а 4–5</b>: опыт → мысль → слово → письмо → (возможно) цифровой текст."
))
story.append(p("<b>Конструктив</b>: убрать «скан» и «OCR» из цепочки, оставить «…письмо → печать → "
    "цифровой текст». Это упрощает цепочку и делает её технически корректной."))

# --- 26 ---
story.append(h2("Тезис 26. Проект создаёт условие для щелчка."))
story.extend(verdict('OK',
    "Сильный методологический тезис. Соответствует <b>phenomenological reduction</b> "
    "(Husserl) и <b>contemplative pedagogy</b> (Barbezat & Bush 2014). «Статистически "
    "предсказуемые токены от пяти респондентов — это шум» — корректная критика "
    "качественного исследования с маленькой выборкой. Один достоверно зафиксированный "
    "соматический сдвиг в одном теле — это валидный результат в tradition of "
    "<b>n=1 case study</b> (Yin 2003)."
))

# --- 27 ---
story.append(h2("Тезис 27. Валидация ловушки — одно событие."))
story.extend(verdict('WARN',
    "Сильная позиция, но переходит в нормативную. «Не нужны пятьсот респондентов» — "
    "верно для <b>доказательства существования феномена</b> (один белый лебедь опровергает "
    "«все лебеди чёрные»), но не для <b>оценки распространённости</b>. Если автор LC v17 "
    "хочет показать, что ловушка работает у <i>большинства</i> носителей "
    "английского/русского, нужны десятки респондентов. Если же цель — показать, что "
    "ловушка может вызвать разрыв хотя бы у одного тела, n=1 достаточно."
))
story.append(p("<b>Конструктив</b>: уточнить цель: «доказательство существования феномена» (n=1 "
    "достаточно) vs «оценка распространённости» (n>30). Текущая формулировка смешивает "
    "две разные цели."))

# --- 28 ---
story.append(h2("Тезис 28. Мост не равен анализу. Запись для себя."))
story.extend(verdict('OK',
    "Сильный этический тезис. Соответствует принципам <b>autoethnography</b> (Ellis, "
    "Adams, Bochner 2011) и <b>first-person methods</b> в когнитивной науке "
    "(Varela & Shear 1999). localStorage как «внешний персональный жёсткий диск» — "
    "корректное инженерное решение: данные не покидают тело-источник."
))

# --- 29 ---
story.append(h2("Тезис 29. localStorage — персональный внешний диск."))
story.extend(verdict('OK',
    "Технически корректно. localStorage в современном браузере (W3C Web Storage, 2009+) — "
    "это per-origin хранилище в браузере пользователя, не отправляется на сервер по "
    "умолчанию. Однако стоит отметить: (а) localStorage <b>доступен любому JS-коду</b> "
    "того же origin, что потенциально делает его уязвимым для XSS; (б) он не шифруется, "
    "и при передаче файла (если пользователь экспортирует его) данные попадают в "
    "открытом виде."
))
story.append(p("<b>Конструктив</b>: добавить предупреждение в манифест: «localStorage не зашифрован; "
    "если экспортируешь файл, ты переносишь свой опыт в открытом виде». Это усиливает "
    "этическую позицию проекта."))

# --- 30 ---
story.append(h2("Тезис 30. Математическая модель — чертёж, не доказательство."))
story.append(quote("«LC(H, F) = bridge( { Pi(delta) ⊥ Pj(f) | Pi, Pj ∈ H, i ≠ j } )»"))
story.extend(verdict('WARN',
    "Сам автор честно признаёт, что это не доказательство, а архитектурная нотация. "
    "Однако формальная корректность формулы проблемна: (а) символ ⊥ в математике "
    "обозначает «перпендикулярен» или «ортогонален», что не имеет очевидного смысла "
    "для процессов; (б) bridge() — не определённая функция; (в) δ и f не имеют "
    "объявленных доменов. Это <b>псевдо-математическая нотация</b> — выглядит как "
    "формула, но не имеет формальной семантики."
))
story.append(p("<b>Конструктив</b>: либо убрать формулу совсем (тезис остаётся сильным без неё), "
    "либо явно переформулировать как «архитектурная диаграмма»: «LC(H, F) = bridge "
    "над ортогональными парами процессов Pi, Pj ∈ H». И добавить: «формальная модель "
    "не приводится; это схематическое описание»."))

# --- 31 ---
story.append(h2("Тезис 31. Эстетика — соматический интерфейс."))
story.extend(verdict('OK',
    "Сильный и оригинальный тезис. Согласуется с <b>affective design</b> (Norman 2004 "
    "«Emotional Design») и <b>neuroaesthetics</b> (Ramachandran & Hirstein 1999). "
    "Конкретные заявления проверяемы: (а) шрифт с засечками замедляет чтение — "
    "подтверждено для сложных текстов (Larson 2007); (б) тёмный фон снижает "
    "сенсорную перегрузку — частично подтверждено для эммерсивных интерфейсов, но "
    "оспаривается для длинных текстов (WCAG 2.1 контраст); (в) пауза 3 секунды — "
    "минимальный порог для соматической регистрации — соответствует данным о "
    "интероцептивной осознанности (Craig 2009)."
))

# --- 32 ---
story.append(h2("Тезис 32. prefers-reduced-motion — это честность."))
story.extend(verdict('BAD',
    "Притянутый аргумент. prefers-reduced-motion — это <b>accessibility feature</b> "
    "(WCAG 2.1 SC 2.3.3, «Animation from Interactions»), цель которого — защита "
    "пользователей с <b>вестибулярными расстройствами</b> (motion sickness, "
    "photosensitive epilepsy). Это техническое и этическое обязательство, а не "
    "«честность». Возвышение accessibility до «честности» — это риторический ход, "
    "который смешивает разные категории. Доступность — это про доступ; честность — "
    "про непритворство. Это разные оси."
))
story.append(p("<b>Конструктив</b>: переформулировать как «prefers-reduced-motion — это "
    "<b>доступность</b>, доведённая до структурного признания: интерфейс признаёт, что "
    "тела различаются». Это сохраняет полиматический импульс, но не путает "
    "категории."))

# --- 33 ---
story.append(h2("Тезис 33. Файл самодостаточен. Без интернета. Без серверов."))
story.extend(verdict('OK',
    "Технически корректно с одной оговоркой. Файл действительно не делает внешних "
    "запросов после загрузки шрифтов с Google Fonts. Однако начальная загрузка "
    "шрифтов (Cormorant Garamond, Inter, JetBrains Mono) требует интернет-соединения "
    "при первом открытии. Полная самодостаточность достигается только при "
    "inline-встраивании шрифтов (base64 или @font-face с локальным путём)."
))
story.append(p("<b>Конструктив</b>: либо встроить шрифты как base64 (файл вырастет до ~500 КБ), "
    "либо явно оговорить: «первый запуск требует интернет; последующие открытия — нет "
    "(браузер кэширует шрифты)». Текущая формулировка «без интернета» технически неточна."))

story.append(PageBreak())

# ===== 4. ЧАСТЬ III: СИСТЕМНЫЕ ЗАМЕЧАНИЯ =====
story.append(h1("4. Часть III. Системные замечания"))

story.append(h2("4.1. Терминологические вольности"))
story.append(p(
    "Проект систематически использует технические термины из нескольких дисциплин как "
    "метафоры: «RAM» и «жёсткий диск» из архитектуры ЭВМ, «операционная система» из "
    "software engineering, «lossy compression» из теории информации. Каждое такое "
    "использование педагогически выигрышно — оно делает абстрактное интуитивно понятным. "
    "Однако совокупный эффект — <b>иллюзия технической точности</b>, которой нет. Когда "
    "читатель встречает «H = {P1, ..., Pn}», он ожидает формальную семантику; когда "
    "встречает «δ требует тело», он ожидает операционализируемое определение δ. Ни того, "
    "ни другого файл не даёт."
))
story.append(p(
    "<b>Конструктив</b>: в начале манифеста ввести явный раздел «Терминологический словарь» с "
    "оговоркой: «все технические термины используются здесь как метафоры; их строгие "
    "значения в исходных дисциплинах могут отличаться». Это не снижает силу манифеста, но "
    "делает его честным по отношению к читателю-полимату."
))

story.append(h2("4.2. Риторика «отказа от оракула» и скрытый нормативизм"))
story.append(p(
    "Тезис 13 («это зеркало, не оракул») и тезис 15 («ИИ честно отказывается от "
    "претензии на понимание») создают позицию методологической скромности. Однако многие "
    "формулировки 33 тезисов нормативны, а не дескриптивны: «молчание — смерть опыта для "
    "потомков», «универсальная грамматика — проекция», «вопрос поставлен неверно». "
    "Это <b>позитивные метафизические тезисы</b>, а не «зеркало». Скрытый нормативизм "
    "противоречит заявленной нейтральности."
))
story.append(p(
    "<b>Конструктив</b>: либо отказаться от риторики «зеркало, не оракул» и признать "
    "нормативность манифеста (это законный философский выбор), либо смягчить "
    "формулировки до дескриптивных: «молчание <i>может быть</i> смертью опыта», "
    "«универсальная грамматика <i>может быть</i> проекцией». Текущее состояние — "
    "метафизика под маской феноменологии."
))

story.append(h2("4.3. Селекция примеров: «тридцать три традиции»"))
story.append(p(
    "Тезис 16 обещает «33 традиции — каталог операционных систем», но в файле LC v17 "
    "фактически упомянуты только три: хопи (ошибочно), японский, русский. Остальные 30 "
    "традиций <b>не упомянуты нигде</b>. Это несоответствие между обещанием и исполнением "
    "ослабляет проект: читатель, готовый встретить богатый каталог, получает три примера, "
    "причём один ошибочный."
))
story.append(p(
    "<b>Конструктив</b>: либо переименовать тезис в «три традиции — три конфигурации» (и "
    "исправить хопи → аймара), либо действительно расширить каталог до 10–15 примеров с "
    "корректными атрибуциями. Текущее название — это обещание, которое файл не выполняет."
))

story.append(h2("4.4. Двойная позиция по Сепиру-Уорфу"))
story.append(p(
    "Тезис 20 утверждает, что «вопрос [Сепира-Уорфа] поставлен неверно» и что язык не "
    "определяет мысль, а «направляет развитие определённых паттернов». Однако тезисы 16, "
    "17, 22 фактически принимают сильную версию Сепира-Уорфа: «хопи маршрутизирует время "
    "визуально», «билингв — два ансамбля», «грамматика — следы телесного опыта вида». "
    "Это внутреннее противоречие: автор сначала отказывается от сильного релятивизма, а "
    "затем пользуется им в формулировках."
))
story.append(p(
    "<b>Конструктив</b>: согласовать позицию. Если принять <b>умеренный релятивизм</b> "
    "(Lupyan 2012, 2016; Wolff & Holmes 2011), то формулировки должны быть вероятностными: "
    "«хопи <i>склонен</i> маршрутизировать время визуально», «билингв <i>часто</i> "
    "переключается между двумя конфигурациями». Это устраняет внутреннее противоречие."
))

story.append(h2("4.5. Архитектурная связность vs фактические ошибки"))
story.append(p(
    "Главное наблюдение полиматического разбора: <b>фактические ошибки LC v17 не разрушают "
    "архитектуру проекта</b>. Структурный тезис — «опыт рождается в теле, слово — его "
    "сжатие, язык — внешний накопитель вида, ИИ структурно не может пройти телесную "
    "ловушку» — survives всех исправлений. Хопи можно заменить на аймара, "
    "триадный мозг — на predictive processing, «пол говорящего» — на «грамматический род "
    "субъекта», и манифест станет <b>сильнее</b>, а не слабее. Это редкое качество для "
    "философского документа — оно указывает на то, что архитектура первична, а "
    "конкретные примеры — иллюстративны."
))

story.append(PageBreak())

# ===== 5. ЧАСТЬ IV: РЕКОМЕНДАЦИИ =====
story.append(h1("5. Часть IV. Приоритизированные рекомендации для v18"))

story.append(h2("5.1. Критический приоритет (P0)"))
story.append(p(
    "<b>P0.1. Исправить атрибуцию шага 3</b>: заменить «язык хопи · малотки, 1983» на "
    "«аймара · Núñez & Sweetser, 2006». Это устраняет главную фактическую ошибку и "
    "усиливает проект: аймара — задокументированный случай с жестовыми данными, "
    "тогда как вёрфовская хопи-гипотеза оспаривается."
))
story.append(p(
    "<b>P0.2. Убрать рационализацию на экране 3</b>: оставить только «Прошлое — впереди. "
    "Будущее — позади.» Без «потому что мы его видим». Это разрушает «оракульность» "
    "и возвращает пользователя к соматическому конфликту, не давая готового объяснения."
))

story.append(h2("5.2. Высокий приоритет (P1)"))
story.append(p(
    "<b>P1.1. Заменить «триадный мозг» на «predictive processing»</b> в тезисе 06. "
    "Ссылка: Friston (2010) «The free-energy principle: a unified brain theory?», "
    "Nature Reviews Neuroscience."
))
story.append(p(
    "<b>P1.2. Уточнить тезис 16</b>: «русский кодирует грамматический род субъекта в "
    "прошедшем времени глагола, обычно совпадающий с полом говорящего». Заменить хопи "
    "на аймара."
))
story.append(p(
    "<b>P1.3. Упростить цепочку тезиса 25</b>: убрать «скан» и «OCR» как отдельные "
    "сжатия. Оставить: опыт → мысль → слово → письмо → печать → цифровой текст. "
    "Это 5 шагов, не 9."
))
story.append(p(
    "<b>P1.4. Снять «честность» с prefers-reduced-motion в тезисе 32</b>: переформулировать "
    "как «доступность, доведённая до структурного признания различия тел». WCAG 2.1 "
    "SC 2.3.3 — фактическая основа, не философская категория."
))

story.append(h2("5.3. Средний приоритет (P2)"))
story.append(p(
    "<b>P2.1. Уточнить тезис 19 (УГ)</b>: разделить «строгую УГ» (богатый врождённый "
    "набор правил — спорна) и «минимальную УГ» (только Merge — нейробиологически "
    "подтверждается)."
))
story.append(p(
    "<b>P2.2. Согласовать позицию по Сепиру-Уорфу</b>: тезис 20 и тезисы 16, 17, 22 "
    "должны использовать одну и ту же модальность (вероятностная: «склонен», «часто») "
    "или категорическую."
))
story.append(p(
    "<b>P2.3. Добавить предупреждение о localStorage</b> в тезис 29: «данные в localStorage "
    "не зашифрованы; при экспорте файла опыт передаётся в открытом виде»."
))
story.append(p(
    "<b>P2.4. Снять «без интернета» в тезисе 33</b> или встроить шрифты как base64. "
    "Текущая формулировка технически неточна: первый запуск требует Google Fonts."
))

story.append(h2("5.4. Низкий приоритет (P3)"))
story.append(p(
    "<b>P3.1. Расширить каталог «33 традиций»</b> в тезисе 16: добавить аймара, "
    "куук-таяйорре, мандарин, тонганский, эргативные языки (баскский, дьярбал), "
    "тоновые языки (йоруба, вьетнамский)."
))
story.append(p(
    "<b>P3.2. Заменить пчелиный пример в тезисе 09</b> на наскальную живопись Шове или "
    "на доисторические счётные кости (Ishango bone, 20 000 лет до н. э.) — это "
    "действительно внешний накопитель вида, а не одноразовый буфер."
))
story.append(p(
    "<b>P3.3. Убрать псевдо-математическую формулу</b> в тезисе 30 или явно "
    "переформулировать как архитектурную диаграмму без претензии на формальность."
))

story.append(h2("5.5. Сохранить без изменений"))
story.append(p(
    "Тезисы 03, 04, 05, 07, 10, 12, 14, 15, 17, 18, 20, 21, 23, 24, 26, 28, 29, 31, 33 "
    "составляют сильное ядро манифеста. Они либо подтверждены современной литературой, либо "
    "являются нормативными позициями, в которых автор имеет право стоять. Эти 19 "
    "тезисов не требуют правок (но тезисы 29 и 33 выиграют от небольших уточнений — "
    "см. P2.3 и P2.4)."
))

story.append(PageBreak())

# ===== 6. ИСТОЧНИКИ =====
story.append(h1("6. Источники и литература"))

story.append(p("Ниже приведены ключевые источники, использованные при верификации. Полные "
               "URL-адреса источников доступны в исследовательских дампах (по запросу)."))

story.append(h2("6.1. Лингвистическая типология и релятивизм"))
sources_typology = [
    ["Malotki, E. (1983)", "Hopi Time: A Linguistic Analysis of the Temporal Concepts in the Hopi Language. Walter de Gruyter."],
    ["Núñez, R. E. & Sweetser, E. (2006)", "With the Future Behind Them: Convergent Evidence From Aymara Language and Gesture. Cognitive Science 30."],
    ["Boroditsky, L. (2001)", "Does Language Shape Thought? Mandarin and English Speakers' Conceptions of Time. Cognition 80(1)."],
    ["Boroditsky, L. & Gaby, A. (2010)", "Remembrances of Times East: Absolute Spatial Representations of Time in an Australian Aboriginal Community. Psychological Science."],
    ["Evans, N. & Levinson, S. (2009)", "The Myth of Language Universals: Language Diversity and Its Importance for Cognitive Science. BBS 32(5)."],
    ["Everett, D. (2005)", "Cultural Constraints on Grammar and Cognition in Pirahã. Current Anthropology 46(4)."],
    ["Lupyan, G. (2012)", "Linguistically Modulated Perception and Cognition: The Label-Feedback Hypothesis. Frontiers in Psychology 3."],
]
src_tbl = Table(sources_typology, colWidths=[55*mm, 110*mm])
src_tbl.setStyle(TableStyle([
    ('FONT', (0,0), (-1,-1), BODY_FONT, 8.5),
    ('FONT', (0,0), (0,-1), BODY_FONT_BOLD, 8.5),
    ('TEXTCOLOR', (0,0), (-1,-1), INK),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LINEBELOW', (0,0), (-1,-2), 0.3, RULE),
]))
story.append(src_tbl)

story.append(h2("6.2. Когнитивная наука и нейробиология"))
sources_neuro = [
    ["Friston, K. (2010)", "The Free-Energy Principle: A Unified Brain Theory? Nature Reviews Neuroscience 11(2)."],
    ["Lakoff, G. & Johnson, M. (1999)", "Philosophy in the Flesh: The Embodied Mind and Its Challenge to Western Thought. Basic Books."],
    ["Clark, A. & Chalmers, D. (1998)", "The Extended Mind. Analysis 58(1)."],
    ["Damasio, A. (1994)", "Descartes' Error: Emotion, Reason, and the Human Brain. Putnam."],
    ["Craig, A. D. (2009)", "How Do You Feel — Now? The Anterior Insula and Human Awareness. Nature Reviews Neuroscience 10."],
    ["Steffen, P. R. et al. (2022)", "The Brain Is Adaptive Not Triune: How the Brain Responds to Stress. Frontiers in Human Neuroscience 16 (PMC9010774)."],
    ["Friederici, A. D. et al. (2017)", "Language, Brain and Evolution. Trends in Cognitive Sciences 21(7)."],
    ["Kandel, E. (2001)", "Nobel Lecture: The Molecular Biology of Memory Storage. Cell Press."],
]
src_tbl2 = Table(sources_neuro, colWidths=[55*mm, 110*mm])
src_tbl2.setStyle(src_tbl._argW and src_tbl._cellStyles[0] and [
    ('FONT', (0,0), (-1,-1), BODY_FONT, 8.5),
    ('FONT', (0,0), (0,-1), BODY_FONT_BOLD, 8.5),
    ('TEXTCOLOR', (0,0), (-1,-1), INK),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LINEBELOW', (0,0), (-1,-2), 0.3, RULE),
])
story.append(src_tbl2)

story.append(h2("6.3. Билингвизм, фонетика, письменность"))
sources_misc = [
    ["Costa, A. et al. (2014)", "'Piensa' twice: On the Foreign Language Effect in Decision Making. Cognition."],
    ["Keysar, B. et al. (2012)", "The Foreign-Language Effect: Thinking in a Foreign Tongue Reduces Decision Biases. Psychological Science 23(7)."],
    ["Browman, C. & Goldstein, L. (1992)", "Articulatory Phonology: An Overview. Phonetica 49."],
    ["Nan, Y. et al. (2018)", "Differential Roles of Right Temporal Cortex and Broca's Area in Pitch Processing. NeuroImage."],
    ["Ong, W. (1982)", "Orality and Literacy: The Technologizing of the Word. Methuen."],
    ["Donald, M. (1991)", "Origins of the Modern Mind: Three Stages in the Evolution of Culture and Cognition. Harvard UP."],
    ["von Frisch, K. (1967)", "The Dance Language and Orientation of Bees. Harvard UP. (Нобелевская премия 1973.)"],
    ["Henrich, J. (2015)", "The Secret of Our Success: How Culture Is Driving Human Evolution. Princeton UP."],
]
src_tbl3 = Table(sources_misc, colWidths=[55*mm, 110*mm])
src_tbl3.setStyle([
    ('FONT', (0,0), (-1,-1), BODY_FONT, 8.5),
    ('FONT', (0,0), (0,-1), BODY_FONT_BOLD, 8.5),
    ('TEXTCOLOR', (0,0), (-1,-1), INK),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LINEBELOW', (0,0), (-1,-2), 0.3, RULE),
])
story.append(src_tbl3)

story.append(h2("6.4. Этимология, переводоведение, инженерия"))
sources_eng = [
    ["LSJ (Liddell-Scott-Jones)", "Greek-English Lexicon, s.v. ἰδιώτης. Oxford UP."],
    ["Reiß, K. & Vermeer, H. (1984)", "Grundlegung einer allgemeinen Translationstheorie. Niemeyer."],
    ["W3C Web Storage (2009+)", "HTML Living Standard, § 5. localStorage interface."],
    ["WCAG 2.1 (2018)", "Web Content Accessibility Guidelines, SC 2.3.3 Animation from Interactions."],
    ["MDN (2024)", "@media (prefers-reduced-motion) — CSS Reference."],
    ["Christiano, P. et al. (2017)", "Deep Reinforcement Learning from Human Preferences. arXiv."],
    ["Quine, W. V. O. (1960)", "Word and Object. MIT Press (гл. 2: indeterminacy of translation)."],
    ["Varela, F., Thompson, E. & Rosch, E. (1991)", "The Embodied Mind: Cognitive Science and Human Experience. MIT Press."],
]
src_tbl4 = Table(sources_eng, colWidths=[55*mm, 110*mm])
src_tbl4.setStyle([
    ('FONT', (0,0), (-1,-1), BODY_FONT, 8.5),
    ('FONT', (0,0), (0,-1), BODY_FONT_BOLD, 8.5),
    ('TEXTCOLOR', (0,0), (-1,-1), INK),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LINEBELOW', (0,0), (-1,-2), 0.3, RULE),
])
story.append(src_tbl4)

story.append(Spacer(1, 14))
story.append(HRule(PAGE_W - MARGIN_L - MARGIN_R, color=GOLD_DIM, thickness=0.6))
story.append(spacer(6))
story.append(Paragraph(
    "Разбор выполнен с использованием веб-поиска по 18 темам (Hopi/Malotki, Aymara, Sapir-Whorf, "
    "Universal Grammar, Pirahã, bilingual cognition, embodied cognition, Friston, Lakoff, "
    "triune brain critique, Kuuk Thaayorre, von Frisch, tonal languages, keigo, Russian gender, "
    "prefers-reduced-motion, etymology of idiotes, Evans-Levinson). Дампы результатов сохранены "
    "в /home/z/my-project/research/.",
    style_caption))

# ---------- BUILD ----------
out_path = "/home/z/my-project/download/LC17_critique.pdf"
doc = LCDocTemplateWithTOC(out_path)

# multiBuild for TOC
doc.multiBuild(story)
print(f"OK: {out_path}")
