"""心構え4つの関係図（内部・外部 × 結論・根拠の4象限）を SVG で書き出す。

python3 figures/gen_mindset_map.py で images/mindset_map.svg を作る。
配色は手続きの流れ図（gen_step_flow.py）に揃える。
"""
from html import escape
from pathlib import Path

from gen_step_flow import MARGIN, wrap

W = 1200
ROW_HEAD = 52
COL_HEAD = 46
GAP = 10
LINE = 2.5
PAD = 28

BLUE, PALE, INK = "#2b5f83", "#e4eef5", "#1b2026"

COL_HEADS = ["内部（自分たち）", "外部（相手）"]
ROW_HEADS = ["結論", "根拠"]
# 象限ごとに ((ラベル, 英語), [(心構え, 入れ子の心構え or None)])。番号は心構えの表の行順に合わせる
QUADS = [
    [(("設計判断", "Design Decision"), [("①決めきる覚悟を持ち、推奨案を仮説として持つ", None)]),
     (("リスク受容", "Risk Acceptance"), [("③相手も不確実性の中で決めている", None)])],
    [(("検証", "Verification"), [("②技術の評価の正しさは自分たちの責任領域", None)]),
     (("妥当性確認", "Validation"), [("④相手の言葉に翻訳するのは自分たちの仕事", None)])],
]


def text(x, y, s, size, weight=400, fill="#ffffff", anchor="start"):
    w = ' font-weight="700"' if weight == 700 else ""
    return f'  <text x="{x:.1f}" y="{y:.1f}" font-size="{size}"{w} fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>'


def quad(x, y, qw, label, items):
    ja, en = label
    lw = 22 * len(ja) + 36
    o = [f'  <rect x="{x + PAD:.1f}" y="{y + PAD:.1f}" width="{lw}" height="40" rx="20" fill="{BLUE}"/>',
         text(x + PAD + lw / 2, y + PAD + 28, ja, 22, 700, "#ffffff", "middle"),
         text(x + PAD + lw + 14, y + PAD + 27, en, 19, 700, BLUE)]
    cy = y + PAD + 40 + 8
    for main, sub in items:
        for line in wrap(main, 20, qw - 2 * PAD):
            cy += 32
            o.append(text(x + PAD, cy, line, 20, fill=INK))
        if sub:
            # 包含は └ で見せる。2行目以降は └ の幅だけ字下げする
            for k, line in enumerate(wrap(sub, 20, qw - 2 * PAD - 26)):
                cy += 32
                if k == 0:
                    o.append(text(x + PAD, cy, "└", 20, fill=INK))
                o.append(text(x + PAD + 26, cy, line, 20, fill=INK))
    return o, cy - y + PAD


def svg():
    gx = MARGIN + ROW_HEAD + GAP
    gw = W - MARGIN - gx
    qw = gw / 2
    gy = MARGIN + COL_HEAD + GAP
    # 同じ行の象限は高さを揃えて格子に見せる
    hs = [max(quad(0, 0, qw, *q)[1] for q in row) for row in QUADS]
    gh = sum(hs)
    H = gy + gh + MARGIN

    o = []
    for i, label in enumerate(COL_HEADS):
        x = gx + qw * i
        o.append(f'  <rect x="{x + (GAP / 2 if i else 0):.1f}" y="{MARGIN}" width="{qw - GAP / 2:.1f}" height="{COL_HEAD}" fill="{PALE}"/>')
        o.append(text(x + qw / 2, MARGIN + 31, label, 19, 700, INK, "middle"))
    y = gy
    for i, (label, h) in enumerate(zip(ROW_HEADS, hs)):
        top = y + (GAP / 2 if i else 0)
        hh = h - GAP / 2
        o.append(f'  <rect x="{MARGIN}" y="{top:.1f}" width="{ROW_HEAD}" height="{hh:.1f}" fill="{PALE}"/>')
        # 1字ずつ縦に積む。writing-mode は SVG から PNG への変換で崩れるため
        ty = top + hh / 2 - 15 * (len(label) - 1) + 7
        for k, c in enumerate(label):
            o.append(text(MARGIN + ROW_HEAD / 2, ty + 30 * k, c, 21, 700, INK, "middle"))
        y += h

    y = gy
    for row, h in zip(QUADS, hs):
        for i, q in enumerate(row):
            o += quad(gx + qw * i, y, qw, *q)[0]
        y += h
    o.append(f'  <line x1="{gx + qw:.1f}" y1="{gy:.1f}" x2="{gx + qw:.1f}" y2="{gy + gh:.1f}" stroke="{BLUE}" stroke-width="{LINE}"/>')
    o.append(f'  <line x1="{gx:.1f}" y1="{gy + hs[0]:.1f}" x2="{gx + gw:.1f}" y2="{gy + hs[0]:.1f}" stroke="{BLUE}" stroke-width="{LINE}"/>')

    head = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" width="{W}" height="{H:.0f}" font-family="Noto Sans CJK JP, sans-serif">',
            f'  <rect width="{W}" height="{H:.0f}" fill="#ffffff"/>']
    return "\n".join(head + o + ["</svg>", ""])


if __name__ == "__main__":
    out = (Path(__file__).parents[1] / "images" / "mindset_map.svg")
    out.write_text(svg(), encoding="utf-8")
    print(out)
