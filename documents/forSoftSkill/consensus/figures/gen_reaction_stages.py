"""相手の理解度と、段階ごとによく出る相手の悪い反応・良い反応の図を SVG で書き出す。

python3 figures/gen_reaction_stages.py で images/reaction_stages.svg を作る。
配色と見た目は心構えの図（gen_mindset_map.py）に揃える。
"""
from html import escape
from pathlib import Path

from gen_step_flow import MARGIN, wrap

W = 1560
GAP = 14
LINE = 1.5
PAD = 26
ROW_H = 34
HEAD_H = 44
STAGE_W = 270
TIP = 26
COL_HEADS = ["悪い反応", "良い反応"]

BLUE, PALE, HEAD, INK = "#2b5f83", "#e4eef5", "#adc7dc", "#1b2026"

# 段階はサイモンの意思決定モデル（Intelligence → Design → Choice）に対応させている
# 良い反応は、同じ行の悪い反応の裏返しにしている
STAGES = [
    (("目的の理解", "Intelligence"), "今何が問題で、何を解決しないといけないか", [
        ("①「それは私に聞かれても」", "「それなら△△さんにも入ってもらったほうがいいですね」"),
        ("②「迷子になりました。私は何をしたらよいのでしょうか？」", "「つまり、今日は〇〇を決めたいということですね」"),
    ]),
    (("案の理解", "Design"), "取りうる案と、それぞれのメリット、リスクや懸念", [
        ("③「何となくは分かりましたが、ちゃんと理解できなかった」", "「A案だと、うちの運用チームの負担はどうなりますか」"),
        ("④「他の代替案はないのでしょうか？」", "「なぜこの構成になるのですか」"),
    ]),
    (("選択の理解", "Choice"), "選択で迷うポイントと、トレードオフの構造", [
        ("⑤「どういう基準で選べば良いか難しいです」", "「今回はその観点は重視していない」"),
        ("⑥「あなたたちならどれを選びますか？」", "「B案のその弱みは、運用でカバーできそうですね」"),
    ]),
]


def text(x, y, s, size, weight=400, fill="#ffffff", anchor="start"):
    w = ' font-weight="700"' if weight == 700 else ""
    return f'  <text x="{x:.1f}" y="{y:.1f}" font-size="{size}"{w} fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>'


def comment(x, y, c, width):
    # 番号付きのセリフは、折り返した2行目を番号の幅だけ字下げする
    indent = 20 if c[0] in "①②③④⑤⑥⑦⑧⑨" else 0
    o = []
    for k, line in enumerate(wrap(c[1:] if indent else c, 20, width - indent)):
        if k == 0 and indent:
            o.append(text(x, y + 28 + ROW_H * k, c[0], 20, fill=INK))
        o.append(text(x + indent, y + 28 + ROW_H * k, line, 20, fill=INK))
    return o, k + 1


def pairs_block(x, y, colw, pairs):
    o, cy = [], y
    # 悪い反応と裏返しの良い反応を同じ行にそろえる
    for pair in pairs:
        n = 1
        for i, c in enumerate(pair):
            lines, k = comment(x + colw * i + PAD + 4, cy, c, colw - PAD - 24)
            o += lines
            n = max(n, k)
        cy += ROW_H * n + 6
    return o, cy - 6 - y


def badge(x, y, h, label, desc):
    # ホームベース形を縦に積み、相手の理解が上の段階から順に進むことを表す
    ja, en = label
    w = STAGE_W
    o = [f'  <polygon points="{x},{y} {x + w},{y} {x + w},{y + h - TIP} {x + w / 2},{y + h} {x},{y + h - TIP}" fill="{PALE}"/>']
    lines = wrap(desc, 17, w - 40)
    body = 30 + 26 + 28 * len(lines)
    ty = y + (h - TIP - body) / 2 + 26
    o.append(text(x + w / 2, ty, ja, 24, 700, INK, "middle"))
    o.append(text(x + w / 2, ty + 28, en, 17, 700, BLUE, "middle"))
    for k, l in enumerate(lines):
        o.append(text(x + w / 2, ty + 62 + 28 * k, l, 17, fill=BLUE, anchor="middle"))
    return o, body + TIP + 20


def svg():
    sx = MARGIN
    gx = sx + STAGE_W + GAP
    colw = (W - MARGIN - gx) / 2
    gy = MARGIN + HEAD_H * 2 + GAP
    hs = []
    for label, desc, pairs in STAGES:
        _, ph = pairs_block(0, 0, colw, pairs)
        _, bh = badge(0, 0, 0, label, desc)
        hs.append(max(ph + PAD * 2, bh) + GAP)
    H = gy + sum(hs) - GAP + MARGIN

    o = [f'  <rect x="{sx}" y="{MARGIN}" width="{STAGE_W}" height="{HEAD_H * 2 + GAP / 2}" fill="{HEAD}"/>',
         text(sx + STAGE_W / 2, MARGIN + HEAD_H + 10, "相手の理解度", 19, 700, INK, "middle"),
         f'  <rect x="{gx}" y="{MARGIN}" width="{W - MARGIN - gx:.1f}" height="{HEAD_H}" fill="{HEAD}"/>',
         text((gx + W - MARGIN) / 2, MARGIN + 30, "相手の反応", 19, 700, INK, "middle")]
    for i, head in enumerate(COL_HEADS):
        x = gx + colw * i
        o.append(f'  <rect x="{x + (GAP / 2 if i else 0):.1f}" y="{MARGIN + HEAD_H + GAP / 2}" width="{colw - GAP / 2:.1f}" height="{HEAD_H}" fill="{HEAD}"/>')
        o.append(text(x + colw / 2, MARGIN + HEAD_H + GAP / 2 + 30, head, 19, 700, INK, "middle"))

    y = gy
    for i, ((label, desc, pairs), h) in enumerate(zip(STAGES, hs)):
        o += badge(sx, y, h - GAP, label, desc)[0]
        ph = pairs_block(0, 0, colw, pairs)[1]
        o += pairs_block(gx, y + (h - GAP - ph) / 2 - 8, colw, pairs)[0]
        if i:
            o.append(f'  <line x1="{gx:.1f}" y1="{y - GAP / 2:.1f}" x2="{W - MARGIN:.1f}" y2="{y - GAP / 2:.1f}" stroke="{BLUE}" stroke-width="{LINE}"/>')
        y += h

    head = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" width="{W}" height="{H:.0f}" font-family="Noto Sans CJK JP, sans-serif">',
            f'  <rect width="{W}" height="{H:.0f}" fill="#ffffff"/>']
    return "\n".join(head + o + ["</svg>", ""])


if __name__ == "__main__":
    out = (Path(__file__).parents[1] / "images" / "reaction_stages.svg")
    out.write_text(svg(), encoding="utf-8")
    print(out)
