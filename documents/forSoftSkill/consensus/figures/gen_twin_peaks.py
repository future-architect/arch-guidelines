"""技術評価と合意形成の2つの山を、若手とベテランがどちらから登るかの図を SVG で書き出す。

python3 figures/gen_twin_peaks.py で images/twin_peaks.svg を作る。
配色は失敗パターンの図（gen_reaction_stages.py）に揃える。
"""
import math
from html import escape
from pathlib import Path

W = 1400
MARGIN = 15
PANEL_H = 470
GAP = 30
PEAK_W, PEAK_H = 560, 300
LX, RX = 390, 1010

BLUE, PALE, DEEP, INK, ACCENT = "#2b5f83", "#e4eef5", "#c9dcea", "#1b2026", "#c0504d"

# 山は2段で同じ位置に置き、矢印の向きだけで登る順の違いを見せる
PANELS = [
    ("若手", "技術評価の山から登り、翻訳して合意形成の山へ向かう", "right", {
        "L": ("①", "技術評価の山", "手続き3〜4", "案を出し、観点ごとに評価する"),
        "R": ("②", "合意形成の山", "手続き6〜7", "選択肢とストーリーで合意する"),
    }, ("翻訳（手続き5）", "評価を相手の判断軸に組み替える", "So What?")),
    ("ベテラン", "合意形成の山から登り、技術評価の山で根拠を固める", "left", {
        "L": ("②", "技術評価の山", "手続き4", "主張を支えるファクトを確かめる"),
        "R": ("①", "合意形成の山", "手続き7", "相手がどこなら頷くかを先に決める"),
    }, ("遡る（手続き6→5）", "選択肢と評価軸が揃っているか確かめる", "Why So?")),
]


def text(x, y, s, size, weight=400, fill=INK, anchor="middle"):
    w = ' font-weight="700"' if weight == 700 else ""
    return f'  <text x="{x:.1f}" y="{y:.1f}" font-size="{size}"{w} fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>'


def mountain(cx, top, first, mark, name, proc, desc):
    base = top + PEAK_H
    # 先に登る山を濃くして、出発点を目で追えるようにする
    o = [f'  <polygon points="{cx},{top} {cx + PEAK_W / 2},{base} {cx - PEAK_W / 2},{base}" '
         f'fill="{DEEP if first else PALE}" stroke="{BLUE}" stroke-width="2"/>',
         text(cx, top + 165, f"{mark} {name}", 30, 700, BLUE),
         text(cx, top + 212, proc, 20, 700, INK),
         text(cx, top + 246, desc, 20, 400, INK)]
    return o


def arrow(y0, direction, label, sub, tag):
    top = y0 + 150
    x1, x2 = (LX + 40, RX - 40) if direction == "right" else (RX - 40, LX + 40)
    cy = y0 + 70
    o = [f'  <path d="M {x1} {top - 6} Q {(LX + RX) / 2} {cy - 30} {x2} {top - 6}" '
         f'fill="none" stroke="{ACCENT}" stroke-width="4"/>']
    # 矢じりは終点での接線（制御点から終点への向き）に合わせる
    qx, qy = (LX + RX) / 2, cy - 30
    tx, ty = x2, top - 6
    a = math.atan2(ty - qy, tx - qx)
    L, Hw = 30, 13
    bx0, by0 = tx - L * math.cos(a), ty - L * math.sin(a)
    px, py = -math.sin(a) * Hw, math.cos(a) * Hw
    o.append(f'  <polygon points="{tx + 8 * math.cos(a):.1f},{ty + 8 * math.sin(a):.1f} {bx0 + px:.1f},{by0 + py:.1f} {bx0 - px:.1f},{by0 - py:.1f}" fill="{ACCENT}"/>')
    bw, bh = 420, 72
    bx, by = (LX + RX) / 2 - bw / 2, cy - 22
    o.append(f'  <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="#ffffff" stroke="{ACCENT}" stroke-width="2.5"/>')
    o.append(text((LX + RX) / 2, by + 30, label, 24, 700, ACCENT))
    o.append(text((LX + RX) / 2, by + 58, sub, 18, 400, ACCENT))
    # 一般に知られた問いの名前を、箱の下に控えめに添える
    o.append(text((LX + RX) / 2, by + bh + 28, tag, 20, 700, ACCENT))
    return o


def panel(y0, who, summary, direction, peaks, arc):
    lw = 26 * len(who) + 40
    o = [f'  <rect x="{MARGIN}" y="{y0}" width="{lw}" height="44" rx="22" fill="{BLUE}"/>',
         text(MARGIN + lw / 2, y0 + 31, who, 24, 700, "#ffffff"),
         text(MARGIN + lw + 16, y0 + 30, summary, 21, 700, BLUE, "start")]
    o += arrow(y0, direction, *arc)
    top = y0 + 150
    for side, cx in (("L", LX), ("R", RX)):
        mark = peaks[side][0]
        o += mountain(cx, top, mark == "①", *peaks[side])
    gy = top + PEAK_H
    o.append(f'  <line x1="{MARGIN}" y1="{gy}" x2="{W - MARGIN}" y2="{gy}" stroke="{BLUE}" stroke-width="2"/>')
    return o


def svg():
    H = MARGIN * 2 + PANEL_H * 2 + GAP
    o = []
    y = MARGIN
    for i, p in enumerate(PANELS):
        if i:
            o.append(f'  <line x1="{MARGIN}" y1="{y - GAP / 2}" x2="{W - MARGIN}" y2="{y - GAP / 2}" stroke="{PALE}" stroke-width="2"/>')
        o += panel(y, *p)
        y += PANEL_H + GAP
    head = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Noto Sans CJK JP, sans-serif">',
            f'  <rect width="{W}" height="{H}" fill="#ffffff"/>']
    return "\n".join(head + o + ["</svg>", ""])


if __name__ == "__main__":
    out = (Path(__file__).parents[1] / "images" / "twin_peaks.svg")
    out.write_text(svg(), encoding="utf-8")
    print(out)
