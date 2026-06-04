# -*- coding: utf-8 -*-
"""
강의안 레이아웃 카탈로그 (파라미터화).
각 함수는 Deck 인스턴스를 받아 슬라이드 1장을 추가한다.
색을 지정하지 않으면 코랄/틸/앰버를 자동 순환한다.

사용:
    from builder import Deck
    import layouts as L
    d = Deck(brand="9WAY · 미래인재연구소")
    L.cover(d, title="...", subtitle="...")
    ...
    d.save("out.pptx")
"""
import tokens as T
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from helpers import (px, pt, rgb, rect, oval, text, bullets, line_div, vline,
                     diag, spike_mark, add_table, _apply_run)

LX = 80
CW = T.SLIDE_W_PX - LX * 2
SW = T.SLIDE_W_PX
ACCENTS = ["primary", "accent_teal", "accent_amber"]


def _accent(i, color=None):
    return color if color else ACCENTS[i % len(ACCENTS)]


def _header(slide, eyebrow, title, title_token="display_md",
            title_weight="SemiBold", y=58):
    if eyebrow:
        text(slide, LX, y, CW, 22, eyebrow.upper(), type_token="caption_upper",
             color="muted")
    text(slide, LX, y + 26, CW, 64, title, type_token=title_token,
         color="ink", weight=title_weight)


def _chip(slide, x, y, label, active=False, size=13):
    w = 30 + len(label) * (size * 0.98)
    rect(slide, x, y, w, 32, fill="primary" if active else "surface_card",
         radius=999)
    text(slide, x, y, w, 32, label, type_token="caption",
         color="on_primary" if active else "ink", align="center",
         valign="middle", size_px=size)
    return w


# ===========================================================================
# 표지 / 섹션 / 메시지
# ===========================================================================
def cover(deck, title, subtitle="", eyebrow="", brand="", title2=None,
          title2_color="primary", meta=""):
    """표지. title2를 주면 2번째 줄을 강조색으로."""
    s = deck.add("canvas")
    if brand:
        text(s, LX, 56, 400, 30, brand, type_token="title_lg", color="ink",
             weight="ExtraBold", valign="middle")
    if eyebrow:
        text(s, SW - LX - 420, 60, 420, 20, eyebrow.upper(),
             type_token="caption_upper", color="muted", align="right")
    rect(s, LX, 256, 64, 6, fill="primary", radius=3)
    if title2:
        text(s, LX, 278, 1040, 90, title, type_token="display_xl",
             color="ink", weight="Light")
        text(s, LX, 372, 1040, 90, title2, type_token="display_xl",
             color=title2_color, weight="ExtraBold")
    else:
        text(s, LX, 300, 1040, 150, title, type_token="display_xl",
             color="ink", weight="Light", line_spacing=1.08)
    if subtitle:
        text(s, LX, 502, 900, 40, subtitle, type_token="display_sm",
             color="muted", weight="Light")
    if meta:
        text(s, LX, 662, CW, 20, meta, type_token="body_sm", color="muted_soft")
    return s


def section_divider(deck, number, title, subtitle="", dark=True):
    """섹션 전환. 큰 번호 + 제목."""
    s = deck.add("surface_dark" if dark else "surface_cream_strong")
    tc = "on_dark" if dark else "ink"
    sc = "on_dark_soft" if dark else "muted"
    if number:
        text(s, LX, 150, 600, 300, str(number), type_token="display_xl",
             color="primary", weight="Black", size_px=240)
        tx, ty = 560, 300
    else:
        tx, ty = LX, 320
    rect(s, tx, ty - 22 if number else 288, 64, 6, fill="primary", radius=3)
    text(s, tx, ty + 8 if number else 332, 680, 70, title,
         type_token="display_lg", color=tc, weight="Light")
    if subtitle:
        text(s, tx, (ty + 88) if number else 432, 680, 40, subtitle,
             type_token="display_sm", color=sc, weight="Light")
    deck.footer(s, dark=dark)
    return s


def statement(deck, lines, bg="surface_cream_strong"):
    """큰 중앙 메시지 디바이더."""
    s = deck.add(bg)
    dark = bg == "surface_dark"
    for i in range(5):
        oval(s, SW / 2 - 44 + i * 22, 196, 10, 10, fill="primary")
    text(s, LX, 270, CW, 200, lines, type_token="display_lg",
         color="on_dark" if dark else "ink", align="center",
         line_spacing=1.25, valign="middle")
    line_div(s, SW / 2 - 120, 520, 240, color="primary", weight=2)
    deck.footer(s, dark=dark)
    return s


def quote(deck, quote_text, author="", bg="surface_cream_strong"):
    """인용/명언."""
    s = deck.add(bg)
    text(s, LX, 150, 200, 120, "“", type_token="display_xl",
         color="primary", weight="Black", size_px=150)
    text(s, LX, 290, 1040, 180, quote_text, type_token="display_lg",
         color="ink", weight="Light", line_spacing=1.3)
    if author:
        text(s, LX, 500, 700, 30, author, type_token="title_md", color="muted")
    deck.footer(s)
    return s


# ===========================================================================
# 학습 / 개념
# ===========================================================================
def objectives(deck, title, goals, eyebrow="Learning Objectives"):
    """체크리스트형 학습 목표. goals: [str]."""
    s = deck.add("canvas")
    _header(s, eyebrow, title)
    y = 200
    for g in goals:
        rect(s, LX, y, 36, 36, fill="primary", radius=8)
        text(s, LX, y, 36, 36, "✓", type_token="title_md",
             color="on_primary", align="center", valign="middle")
        text(s, LX + 56, y, 980, 36, g, type_token="title_md", color="ink",
             valign="middle", weight="Regular")
        y += 70
    text(s, 900, 200, 300, 320, str(len(goals)), type_token="display_xl",
         color="surface_card", weight="Black", size_px=300, align="right")
    deck.footer(s)
    return s


def concept(deck, term, definition, formula="", example="",
            eyebrow="Key Concept"):
    """핵심 개념: 큰 용어 + 정의 + (공식) + (예시 다크 콜아웃)."""
    s = deck.add("canvas")
    text(s, LX, 90, 200, 24, eyebrow.upper(), type_token="caption_upper",
         color="primary")
    text(s, LX, 130, 700, 120, term, type_token="display_xl", color="ink",
         weight="Black", size_px=104)
    text(s, LX, 270, 760, 110, definition, type_token="title_lg", color="body",
         weight="Regular", line_spacing=1.5)
    if formula:
        rect(s, LX, 400, 760, 90, fill="surface_card", radius=12)
        text(s, LX, 400, 760, 90, formula, type_token="display_sm",
             color="ink", align="center", valign="middle", weight="SemiBold")
    if example:
        rect(s, 880, 130, CW - (880 - LX), 360, fill="surface_dark", radius=12)
        text(s, 912, 162, 280, 24, "예시", type_token="caption_upper",
             color="accent_amber")
        text(s, 912, 196, 280, 280, example, type_token="body_md",
             color="on_dark_soft", line_spacing=1.6)
    deck.footer(s)
    return s


def question(deck, question_text, sub=""):
    """풀코랄 빅 퀘스천."""
    s = deck.add("primary")
    text(s, LX, 110, 200, 100, "?", type_token="display_xl",
         color="on_primary", weight="Black", size_px=140)
    text(s, LX, 280, 1040, 220, question_text, type_token="display_xl",
         color="on_primary", weight="Light", line_spacing=1.15, size_px=64)
    if sub:
        text(s, LX, 630, 800, 30, sub, type_token="title_md",
             color="on_primary", weight="Regular")
    return s


def takeaways(deck, title, items, eyebrow="Key Takeaways"):
    """핵심 N가지. items: [(title, desc)] (최대 4)."""
    s = deck.add("canvas")
    _header(s, eyebrow, title)
    n = min(len(items), 4)
    cw = (CW - (n - 1) * 24) / n
    for i in range(n):
        t, desc = items[i]
        color = _accent(i)
        x = LX + i * (cw + 24)
        text(s, x, 210, cw, 90, f"{i+1:02d}", type_token="display_xl",
             color=color, weight="ExtraBold", size_px=60)
        line_div(s, x, 300, 48, color=color, weight=3)
        text(s, x, 324, cw, 40, t, type_token="title_lg", color="ink")
        text(s, x, 372, cw, 150, desc, type_token="body_md", color="muted",
             line_spacing=1.55)
    deck.footer(s)
    return s


# ===========================================================================
# 카드 / 통계
# ===========================================================================
def three_up(deck, title, cards, eyebrow=""):
    """3-up 피처 카드. cards: [(title, body[, color])]."""
    s = deck.add("canvas")
    _header(s, eyebrow, title)
    cw = (CW - 48) / 3
    for i, c in enumerate(cards[:3]):
        t, body = c[0], c[1]
        color = _accent(i, c[2] if len(c) > 2 else None)
        x = LX + i * (cw + 24)
        rect(s, x, 200, cw, 300, fill="surface_card", radius=12)
        oval(s, x + 28, 228, 48, 48, fill=color)
        text(s, x + 28, 294, cw - 56, 56, t, type_token="title_lg",
             color="ink", line_spacing=1.2)
        text(s, x + 28, 360, cw - 56, 130, body, type_token="body_md",
             color="body", line_spacing=1.55)
    deck.footer(s)
    return s


def stat_cards(deck, title, stats, eyebrow=""):
    """통계 카드. stats: [(number, label, desc[, color])]."""
    s = deck.add("canvas")
    _header(s, eyebrow, title)
    n = min(len(stats), 4)
    cw = (CW - (n - 1) * 24) / n
    for i in range(n):
        st = stats[i]
        num, label, desc = st[0], st[1], st[2]
        color = _accent(i, st[3] if len(st) > 3 else None)
        x = LX + i * (cw + 24)
        rect(s, x, 210, cw, 320, fill="surface_card", radius=12)
        text(s, x + 28, 238, cw - 56, 70, num, type_token="display_lg",
             color=color, size_px=52, weight="ExtraBold")
        text(s, x + 28, 320, cw - 56, 30, label, type_token="title_md",
             color="ink")
        line_div(s, x + 28, 356, 40, color=color, weight=3)
        text(s, x + 28, 372, cw - 56, 140, desc, type_token="body_md",
             color="muted", line_spacing=1.5)
    deck.footer(s)
    return s


def big_stat(deck, number, pre="", post="", note=""):
    """단일 빅 통계."""
    s = deck.add("canvas")
    if pre:
        text(s, LX, 160, CW, 40, pre, type_token="display_sm", color="muted",
             align="center", weight="Light")
    text(s, LX, 220, CW, 200, number, type_token="display_xl", color="primary",
         align="center", weight="Black", size_px=190)
    if post:
        text(s, LX, 450, CW, 40, post, type_token="display_sm", color="ink",
             align="center")
    if note:
        text(s, LX, 510, CW, 24, note, type_token="body_sm",
             color="muted_soft", align="center")
    deck.footer(s)
    return s


# ===========================================================================
# 표 / 프로세스 / 타임라인
# ===========================================================================
def comparison_table(deck, title, data, highlight_col=None, eyebrow="",
                     header_color="dark", label_col=True, intro=""):
    """비교 표(네이티브). data: 2D 리스트(첫 행=헤더).
    header_color: 'dark' | 'coral'. highlight_col: 강조 열 인덱스."""
    s = deck.add("canvas")
    _header(s, eyebrow, title)
    y = 200
    if intro:
        text(s, LX, 144, CW, 36, intro, type_token="body_md", color="muted",
             size_px=14)
        y = 210
    hf, hc = ("primary", "on_primary") if header_color == "coral" else \
             ("surface_dark", "on_dark")
    n = len(data[0])
    add_table(s, LX, y, CW, min(360, 64 * len(data)), data,
              col_widths=[CW / n] * n, header_fill=hf, header_color=hc,
              highlight_col=highlight_col, label_col=label_col)
    deck.footer(s)
    return s


def process(deck, title, steps, eyebrow="Process"):
    """가로 프로세스. steps: [(title, desc[, color])]."""
    s = deck.add("canvas")
    _header(s, eyebrow, title)
    n = len(steps)
    gap = 28
    cw = (CW - (n - 1) * gap) / n
    y = 280
    line_div(s, LX + cw / 2, y + 28, CW - cw, color="hairline", weight=2)
    for i, st in enumerate(steps):
        t, desc = st[0], st[1]
        color = _accent(i, st[2] if len(st) > 2 else None)
        x = LX + i * (cw + gap)
        oval(s, x + cw / 2 - 28, y, 56, 56, fill=color)
        text(s, x + cw / 2 - 28, y, 56, 56, str(i + 1), type_token="title_lg",
             color="on_dark" if color == "surface_dark" else "on_primary",
             align="center", valign="middle")
        text(s, x, y + 76, cw, 48, t, type_token="title_sm", color="ink",
             align="center", line_spacing=1.2)
        if desc:
            text(s, x, y + 128, cw, 80, desc, type_token="body_sm",
                 color="muted", align="center", line_spacing=1.4)
    deck.footer(s)
    return s


def vsteps(deck, title, steps, eyebrow="Process"):
    """세로 단계. steps: [(title, desc[, color])]."""
    s = deck.add("canvas")
    _header(s, eyebrow, title)
    y = 200
    vline(s, LX + 22, y + 22, (len(steps) - 1) * 100, color="hairline",
          weight=2)
    for i, st in enumerate(steps):
        t, desc = st[0], st[1]
        color = _accent(i, st[2] if len(st) > 2 else None)
        oval(s, LX, y, 44, 44, fill=color)
        text(s, LX, y, 44, 44, str(i + 1), type_token="title_md",
             color="on_dark" if color == "surface_dark" else "on_primary",
             align="center", valign="middle")
        text(s, LX + 76, y - 2, 400, 32, t, type_token="title_lg", color="ink")
        text(s, LX + 76, y + 30, 900, 30, desc, type_token="body_md",
             color="muted")
        y += 100
    deck.footer(s)
    return s


def timeline(deck, title, nodes, eyebrow="Timeline"):
    """가로 타임라인. nodes: [(label, title, sub)]."""
    s = deck.add("canvas")
    _header(s, eyebrow, title)
    y = 340
    line_div(s, LX, y, CW, color="hairline", weight=2)
    n = len(nodes)
    step = CW / (n - 1) if n > 1 else CW
    for i, (lab, t, sub) in enumerate(nodes):
        x = LX + i * step
        color = "primary" if i == n - 1 else "ink"
        oval(s, x - 9, y - 9, 18, 18, fill=color)
        above = (i % 2 == 0)
        ty = y - 130 if above else y + 28
        text(s, x - 110, ty, 220, 40, lab, type_token="display_sm",
             color=color, align="center", weight="ExtraBold")
        text(s, x - 110, ty + 44, 220, 26, t, type_token="title_sm",
             color="ink", align="center")
        if sub:
            text(s, x - 110, ty + 70, 220, 22, sub, type_token="body_sm",
                 color="muted", align="center", size_px=12)
    deck.footer(s)
    return s


# ===========================================================================
# 프레임워크 / 가이드
# ===========================================================================
def matrix_2x2(deck, title, quads, note="", eyebrow="Framework",
               axis_label=""):
    """2x2 매트릭스. quads: 4개 [(label, sub[, color])] (좌상,우상,좌하,우하)."""
    s = deck.add("canvas")
    _header(s, eyebrow, title)
    cx, cy, sz, g = LX, 196, 218, 12
    pos = [(0, 0), (1, 0), (0, 1), (1, 1)]
    for i, q in enumerate(quads[:4]):
        label, sub = q[0], q[1]
        color = _accent(i, q[2] if len(q) > 2 else None)
        cxi, cyi = pos[i]
        x = cx + cxi * (sz + g)
        y = cy + cyi * (sz + g)
        rect(s, x, y, sz, sz, fill="surface_card", radius=12)
        oval(s, x + 22, y + 22, 14, 14, fill=color)
        text(s, x + 22, y + 44, sz - 44, 36, label, type_token="title_lg",
             color="ink")
        text(s, x + 22, y + 86, sz - 44, 60, sub, type_token="body_sm",
             color="muted", size_px=12)
    if axis_label:
        text(s, cx, cy + 2 * sz + g + 6, 2 * sz + g, 22, axis_label,
             type_token="caption_upper", color="muted_soft", align="center")
    if note:
        rx = cx + 2 * sz + g + 48
        rect(s, rx, 196, SW - LX - rx, 448, fill="surface_dark", radius=12)
        text(s, rx + 32, 232, 300, 30, "어떻게 읽나요?", type_token="title_md",
             color="on_dark")
        text(s, rx + 32, 282, SW - LX - rx - 64, 300, note,
             type_token="body_md", color="on_dark_soft", line_spacing=1.6)
    deck.footer(s)
    return s


def do_dont(deck, title, dos, donts, eyebrow="Guide"):
    """Do / Don't. dos·donts: [str]."""
    s = deck.add("canvas")
    _header(s, eyebrow, title)
    cw = (CW - 40) / 2
    for col, (head, items, color, mark) in enumerate([
            ("DO", dos, "success", "✓"),
            ("DON'T", donts, "error", "✕")]):
        x = LX + col * (cw + 40)
        rect(s, x, 200, cw, 340, fill="surface_card", radius=12)
        oval(s, x + 28, 228, 40, 40, fill=color)
        text(s, x + 28, 228, 40, 40, mark, type_token="title_md",
             color="on_primary", align="center", valign="middle")
        text(s, x + 84, 234, 300, 32, head, type_token="title_lg", color="ink",
             valign="middle", weight="ExtraBold")
        bullets(s, x + 28, 300, cw - 56, 220, items, type_token="body_md",
                color="body", marker="—", marker_color=color, gap_px=12)
    deck.footer(s)
    return s


def keyword_grid(deck, title, words, cols=3, eyebrow=""):
    """키워드 그리드. words: [str] 또는 [(label, color)]."""
    s = deck.add("canvas")
    _header(s, eyebrow, title)
    n = len(words)
    cw = (CW - (cols - 1) * 20) / cols
    ch = 110
    for i, w in enumerate(words):
        label, color = (w, _accent(i)) if isinstance(w, str) else \
                       (w[0], _accent(i, w[1]))
        c = i % cols
        r = i // cols
        x = LX + c * (cw + 20)
        y = 200 + r * (ch + 16)
        rect(s, x, y, cw, ch, fill="surface_card", radius=12)
        oval(s, x + 24, y + ch / 2 - 18, 36, 36, fill=color)
        text(s, x + 24, y + ch / 2 - 18, 36, 36, str(i + 1),
             type_token="title_sm", color="on_primary", align="center",
             valign="middle")
        text(s, x + 76, y, cw - 90, ch, label, type_token="title_lg",
             color="ink", valign="middle")
    deck.footer(s)
    return s


def checklist(deck, title, items, dark=True, eyebrow="Summary"):
    """요약 체크리스트."""
    s = deck.add("surface_dark" if dark else "canvas")
    tc = "on_dark" if dark else "ink"
    text(s, LX, 60, CW, 22, eyebrow.upper(), type_token="caption_upper",
         color="accent_amber" if dark else "primary")
    text(s, LX, 86, CW, 60, title, type_token="display_lg", color=tc,
         weight="Light")
    y = 200
    for it in items:
        rect(s, LX, y, 32, 32,
             fill="surface_dark_elevated" if dark else "surface_card",
             line="muted" if dark else None, radius=8)
        text(s, LX, y, 32, 32, "✓", type_token="body_md",
             color="accent_teal", align="center", valign="middle")
        text(s, LX + 52, y, 980, 32, it, type_token="title_md", color=tc,
             valign="middle", weight="Regular")
        y += 64
    deck.footer(s, dark=dark)
    return s


def worksheet(deck, title, prompts, eyebrow="Activity", action=""):
    """활동지(빈칸). prompts: [(label, hint)]."""
    s = deck.add("canvas")
    _header(s, eyebrow, title)
    y = 200
    for label, hint in prompts:
        text(s, LX, y, 200, 48, label, type_token="title_lg", color="ink",
             valign="middle")
        rect(s, LX + 200, y, 760, 48, fill="surface_soft", line="hairline",
             radius=8)
        text(s, LX + 216, y, 740, 48, hint, type_token="body_md",
             color="muted_soft", valign="middle")
        y += 84
    if action:
        rect(s, LX, y + 6, CW, 80, fill="primary", radius=12)
        text(s, LX + 24, y + 6, CW - 48, 80, action, type_token="title_md",
             color="on_primary", valign="middle")
    deck.footer(s)
    return s


# ===========================================================================
# 타이포 무드 (포스터 / 에디토리얼)
# ===========================================================================
def poster(deck, headline, eyebrow="", sub="", dark=True):
    """Black weight 임팩트 포스터."""
    s = deck.add("surface_dark" if dark else "primary")
    tc = "on_dark" if dark else "on_primary"
    if eyebrow:
        text(s, LX, 120, CW, 30, eyebrow.upper(), type_token="caption_upper",
             color="accent_amber" if dark else "on_primary")
    text(s, LX, 170, CW, 360, headline, type_token="display_xl", color=tc,
         weight="Black", size_px=140, line_spacing=1.0)
    rect(s, LX, 560, 64, 8, fill="primary" if dark else "canvas", radius=4)
    if sub:
        text(s, LX, 590, 900, 30, sub, type_token="title_md",
             color="on_dark_soft" if dark else "on_primary", weight="Light")
    deck.footer(s, dark=True)
    return s


def editorial(deck, headline, columns, eyebrow="Essay"):
    """Thin weight 매거진/에세이. columns: [str] (1~2개)."""
    s = deck.add("canvas")
    text(s, LX, 90, 200, 24, eyebrow.upper(), type_token="caption_upper",
         color="primary")
    text(s, LX, 130, 1040, 170, headline, type_token="display_lg", color="ink",
         weight="Thin", line_spacing=1.3, size_px=44)
    line_div(s, LX, 320, CW, color="hairline")
    cols = columns[:2]
    cw = (CW - 48) / len(cols) if cols else CW
    for i, body in enumerate(cols):
        text(s, LX + i * (cw + 48), 350, cw, 220, body, type_token="body_md",
             color="body", line_spacing=1.7)
    deck.footer(s)
    return s


# ===========================================================================
# 콘텐츠 일반
# ===========================================================================
def bullets_slide(deck, title, items, eyebrow="", marker="—"):
    """제목 + 불릿 리스트. items: [str] 또는 [(marker, str)]."""
    s = deck.add("canvas")
    _header(s, eyebrow, title)
    bullets(s, LX, 200, CW, 380, items, type_token="title_md", color="body",
            marker=marker, marker_color="primary", gap_px=16)
    deck.footer(s)
    return s


def two_col(deck, title, left, right, eyebrow=""):
    """2단 대비. left·right: (heading, body, fill, accent)."""
    s = deck.add("canvas")
    _header(s, eyebrow, title)
    gap = 40
    cw = (CW - gap) / 2
    for i, blk in enumerate([left, right]):
        heading, body = blk[0], blk[1]
        fill = blk[2] if len(blk) > 2 else ("surface_card" if i == 0
                                            else "surface_dark")
        accent = blk[3] if len(blk) > 3 else _accent(i)
        dark = fill == "surface_dark"
        x = LX + i * (cw + gap)
        rect(s, x, 200, cw, 340, fill=fill, radius=12)
        text(s, x + 32, 232, cw - 64, 36, heading, type_token="display_sm",
             color="on_dark" if dark else "ink")
        line_div(s, x + 32, 286, cw - 64,
                 color="surface_dark_elevated" if dark else "hairline")
        if isinstance(body, (list, tuple)):
            bullets(s, x + 32, 308, cw - 64, 220, body, type_token="body_md",
                    color="on_dark_soft" if dark else "body",
                    marker_color=accent, gap_px=10)
        else:
            text(s, x + 32, 308, cw - 64, 220, body, type_token="body_md",
                 color="on_dark_soft" if dark else "body", line_spacing=1.6)
    deck.footer(s)
    return s


# ===========================================================================
# 차트 (네이티브 · 편집 가능)
# ===========================================================================
def chart(deck, title, categories, series, kind="column", eyebrow="",
          note=""):
    """네이티브 차트. series: [(name, [values])]. kind: column|line|donut."""
    s = deck.add("canvas")
    _header(s, eyebrow, title)
    rect(s, LX, 196, CW, 392, fill="canvas", line="hairline", radius=12)
    data = CategoryChartData()
    data.categories = categories
    for name, vals in series:
        data.add_series(name, vals)
    ctype = {"column": XL_CHART_TYPE.COLUMN_CLUSTERED,
             "line": XL_CHART_TYPE.LINE_MARKERS,
             "donut": XL_CHART_TYPE.DOUGHNUT}[kind]
    gf = s.shapes.add_chart(ctype, px(LX + 24), px(218), px(CW - 48), px(348),
                            data)
    ch = gf.chart
    ch.font.name = T.FONT_BODY
    ch.font.size = pt(20)
    ch.font.color.rgb = rgb("muted")
    palette = ["primary", "accent_teal", "accent_amber", "surface_dark"]
    if kind == "donut":
        ch.has_legend = True
        ch.legend.position = XL_LEGEND_POSITION.RIGHT
        ch.legend.include_in_layout = False
        ch.has_title = False
        for pt_, col in zip(ch.plots[0].series[0].points, palette):
            pt_.format.fill.solid()
            pt_.format.fill.fore_color.rgb = rgb(col)
    else:
        ch.has_legend = len(series) > 1
        if ch.has_legend:
            ch.legend.position = XL_LEGEND_POSITION.TOP
            ch.legend.include_in_layout = False
        for sr, col in zip(ch.series, palette):
            if kind == "line":
                sr.format.line.color.rgb = rgb(col)
                sr.format.line.width = pt(2.5)
                sr.marker.format.fill.solid()
                sr.marker.format.fill.fore_color.rgb = rgb(col)
                sr.marker.format.line.color.rgb = rgb(col)
            else:
                sr.format.fill.solid()
                sr.format.fill.fore_color.rgb = rgb(col)
    if note:
        text(s, LX, 600, CW, 20, note, type_token="body_sm", color="muted_soft")
    deck.footer(s)
    return s


# ===========================================================================
# 마무리
# ===========================================================================
def closing(deck, title, sub="", contact=""):
    """코랄 CTA 클로징."""
    s = deck.add("canvas")
    rect(s, LX, 130, CW, 460, fill="primary", radius=16)
    bx = LX + 64
    text(s, bx, 240, 900, 100, title, type_token="display_xl",
         color="on_primary")
    if sub:
        text(s, bx, 370, 800, 40, sub, type_token="display_sm",
             color="on_primary", weight="Light")
    if contact:
        rect(s, bx, 446, 420, 52, fill="canvas", radius=8)
        text(s, bx, 446, 420, 52, contact, type_token="title_sm", color="ink",
             align="center", valign="middle")
    deck.footer(s)
    return s
