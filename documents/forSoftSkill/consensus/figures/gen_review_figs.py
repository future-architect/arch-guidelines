"""レビュー技術のページの図（B〜D）を SVG で書き出す。

python3 figures/gen_review_figs.py で images/review_*.svg を作る。
配色は相手の理解の段階の図（gen_reaction_stages.py）に揃える。
"""
from pathlib import Path

import gen_reaction_stages as rs
from gen_step_flow import MARGIN, char_w, wrap

W = rs.W
GAP, PAD, LINE = rs.GAP, rs.PAD, rs.LINE
BLUE, PALE, HEAD, INK = rs.BLUE, rs.PALE, rs.HEAD, rs.INK
MID = "#c9dbe8"
text = rs.text
OUT = Path(__file__).parents[1] / "images"


def page(H, o):
    head = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" width="{W}" height="{H:.0f}" font-family="Noto Sans CJK JP, sans-serif">',
            f'  <rect width="{W}" height="{H:.0f}" fill="#ffffff"/>']
    return "\n".join(head + o + ["</svg>", ""])


def lines_at(x, y, s, size, width, fill=INK, weight=400, anchor="start", lh=None):
    lh = lh or size * 1.6
    ls = wrap(s, size, width)
    return [text(x, y + lh * k, l, size, weight, fill, anchor) for k, l in enumerate(ls)], len(ls)



# ---- C: 指導上のアンチパターンの一覧 -------------------------------------

# どの成果物に対しても効かないので、成果物ではなく問題点の型で束ねる。
# レビューは指摘対象（What）と伝え方（How）の2軸で漏れなく分ける。
# 番号は本文の見出し①〜⑤。番号なしの行は直前の番号と同じ見出しに含まれる
# (場面, 軸, 問題点, [声掛けの例], 発生しやすい段階)。段階は STAGES_C の順の 0/1
ROWS_C = [
    ("作業指示", "-", "手続きの順を崩す", ["①「まず導入から書いて」", "「比較表は省いて、結論1枚で」"], [1, 0, 0, 0]),
    ("レビュー", "指摘対象\n（What）", "細部から直させる", ["②「ここは◯評価じゃなくて△が良いのでは？」"], [0, 1, 0, 0]),
    ("レビュー", "伝え方\n（How）", "抽象的な言葉で指摘する", ["③「で、論点は何？」", "④「仮説は何？」"], [0, 1, 1, 1]),
    ("レビュー", "伝え方\n（How）", "目指すべき状態だけを伝える", ["⑤「相手目線で考えて」", "「相手がその上司に説得できるように書いて」", "「もっと分かりやすく」"], [0, 1, 1, 1]),
]
# 見極め方の図の段階を縮めた名前。比較表より前はレビューで見ないので、③〜⑤は比較表から
STAGES_C = ["案出し", "比較表", "推奨案", "ドラフト"]


def stage_cells(x, w, y, h, on):
    o = []
    cw = w / len(on)
    for k, f in enumerate(on):
        o.append(f'  <rect x="{x + cw * k + 2:.1f}" y="{y}" width="{cw - 4:.1f}" height="{h}" fill="{PALE if f else '#f4f6f8'}"/>')
        if f:
            o.append(text(x + cw * k + cw / 2, y + h / 2 + 9, "●", 24, 700, BLUE, "middle"))
    return o


def fig_c():
    o = []
    widths = [120, 190, 230, 560]
    widths.append(W - 2 * MARGIN - sum(widths) - GAP * 4)
    xs = [MARGIN]
    for w in widths[:-1]:
        xs.append(xs[-1] + w + GAP)
    heads = ["場面", "軸", "問題点", "アンチパターンな声掛け"]
    y = MARGIN
    # 段階の列は上段の見出しで束ね、ほかの列の見出しは2段分の高さにする
    hh = rs.HEAD_H * 2 + 4
    for x, w, h in zip(xs, widths, heads):
        o.append(f'  <rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{hh}" fill="{HEAD}"/>')
        o.append(text(x + w / 2, y + hh / 2 + 7, h, 19, 700, INK, "middle"))
    o.append(f'  <rect x="{xs[4] + 2:.1f}" y="{y}" width="{widths[4] - 4:.1f}" height="{rs.HEAD_H}" fill="{HEAD}"/>')
    o.append(text(xs[4] + widths[4] / 2, y + 30, "発生しやすい成果物の段階", 19, 700, INK, "middle"))
    sw = widths[4] / len(STAGES_C)
    for k, name in enumerate(STAGES_C):
        x = xs[4] + sw * k
        o.append(f'  <rect x="{x + 2:.1f}" y="{y + rs.HEAD_H + 4}" width="{sw - 4:.1f}" height="{rs.HEAD_H}" fill="{HEAD}"/>')
        o.append(text(x + sw / 2, y + rs.HEAD_H + 34, name, 18, 700, INK, "middle"))
    y += hh + GAP

    size, lh, pad = 18, 30, 18
    spans = {0: {}, 1: {}}
    for i, (scene, axis, kind, examples, on) in enumerate(ROWS_C):
        ex = [l for e in examples for l in wrap(e, size, widths[3] - 2 * pad)]
        kd = wrap(kind, 19, widths[2] - 2 * pad)
        rh = max(len(ex), len(kd), 2) * lh + 2 * pad  # 1行の行も2行分にして高さをそろえる
        if i:
            o.append(f'  <line x1="{xs[3]:.1f}" y1="{y - GAP / 2:.1f}" x2="{W - MARGIN:.1f}" y2="{y - GAP / 2:.1f}" stroke="{BLUE}" stroke-width="{LINE}"/>')
        o.append(f'  <rect x="{xs[2]:.1f}" y="{y}" width="{widths[2]:.1f}" height="{rh}" fill="{PALE}"/>')
        ty = y + rh / 2 - (len(kd) - 1) * lh / 2 + 7
        o += [text(xs[2] + widths[2] / 2, ty + lh * j, l, 19, 700, INK, "middle") for j, l in enumerate(kd)]
        ty = y + rh / 2 - (len(ex) - 1) * lh / 2 + 6
        for j, l in enumerate(ex):
            indent = size if l[0] not in "①②③④⑤⑥" else 0
            o.append(text(xs[3] + pad + indent, ty + lh * j, l, size, 700, INK))
        o += stage_cells(xs[4], widths[4], y, rh, on)
        for k, key in [(0, scene), (1, (scene, axis))]:
            s0, _ = spans[k].get(key, (y, 0))
            spans[k][key] = (s0, y + rh)
        y += rh + GAP
    for k, fill in [(0, MID), (1, "#d6e4ef")]:
        for key, (s0, s1) in spans[k].items():
            label = key if k == 0 else key[1]
            cw = widths[k]
            o.append(f'  <rect x="{xs[k]:.1f}" y="{s0}" width="{cw:.1f}" height="{s1 - s0:.1f}" fill="{fill}"/>')
            ls = [l for part in label.split("\n") for l in wrap(part, 19, cw - 24)]
            ty = (s0 + s1) / 2 - (len(ls) - 1) * 14 + 7
            o += [text(xs[k] + cw / 2, ty + 28 * j, l, 19, 700, INK, "middle") for j, l in enumerate(ls)]
    return page(y - GAP + MARGIN, o)


# ---- B: 見極め方①〜④の位置づけ -------------------------------------------

GREY, GREY_INK = "#eef1f4", "#7a8793"
STAGES_B = ["案出しと調査", "比較表", "推奨案", "資料のドラフト"]
# (見出し番号, 文言, 成果物の列)
CHECKS_B = [("②", "観点の妥当性を見る", 1), ("③", "落としどころを語れるか", 2), ("④", "目的を言葉にさせる", 3)]


def fig_b():
    o = []
    n = len(STAGES_B)
    cw = (W - 2 * MARGIN) / n
    tip = 28
    y = MARGIN
    o.append(text(MARGIN, y + 20, "メンバーの成果物", 18, 700, BLUE))
    y += 36
    ch = 78
    for i, name in enumerate(STAGES_B):
        x = MARGIN + cw * i
        x2 = x + cw - 8
        notch = tip if i else 0
        pts = f"{x},{y} {x2 - tip},{y} {x2},{y + ch / 2} {x2 - tip},{y + ch} {x},{y + ch} {x + notch},{y + ch / 2}"
        fill, ink = (GREY, GREY_INK) if i == 0 else (PALE, INK)
        o.append(f'  <polygon points="{pts}" fill="{fill}"/>')
        o.append(text(x + notch + (cw - 8 - tip - notch) / 2, y + ch / 2 + 8, name, 22, 700, ink, "middle"))
    top = y
    y += ch + 64
    o.append(text(MARGIN, y - 18, "レビュアーが見ること", 18, 700, BLUE))

    bh = 84
    o.append(f'  <rect x="{MARGIN}" y="{y}" width="{cw - 30}" height="{bh}" fill="{GREY}"/>')
    o.append(text(MARGIN + (cw - 30) / 2, y + bh / 2 + 8, "見ない", 21, 700, GREY_INK, "middle"))
    for num, label, col in CHECKS_B:
        x = MARGIN + cw * col + 14
        w = cw - 36
        o.append(f'  <rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{bh}" rx="8" fill="#ffffff" stroke="{BLUE}" stroke-width="2"/>')
        o.append(text(x + 20, y + bh / 2 + 8, num, 24, 700, BLUE))
        o.append(text(x + 54, y + bh / 2 + 8, label, 20, 700, INK))

    # ①は、比較表が出てきた境目に引く線として置く
    bx = MARGIN + cw - 4
    o.append(f'  <line x1="{bx}" y1="{top - 10}" x2="{bx}" y2="{y + bh + 10}" stroke="{BLUE}" stroke-width="3" stroke-dasharray="8 6"/>')
    pill = "①指導の出発点"
    pw = 20 * len(pill) + 36
    py = top + ch + 14
    o.append(f'  <rect x="{bx - pw / 2}" y="{py}" width="{pw}" height="36" rx="18" fill="{BLUE}"/>')
    o.append(text(bx, py + 25, pill, 20, 700, "#ffffff", "middle"))

    # 最初のレビューは②③まで。④はドラフトができてから
    y += bh + 24
    for (c0, c1, label) in [(1, 2, "最初のレビュー"), (3, 3, "ドラフトの後")]:
        x0 = MARGIN + cw * c0 + 14
        x1 = MARGIN + cw * (c1 + 1) - 22
        o.append(f'  <path d="M{x0},{y} v12 H{x1} v-12" fill="none" stroke="{BLUE}" stroke-width="2"/>')
        o.append(text((x0 + x1) / 2, y + 42, label, 18, 700, BLUE, "middle"))
    return page(y + 42 + MARGIN, o)


# ---- D: 覚悟の分解を、見分ける問いからの振り分けつきの階段で -----------------

QUESTION_D = "「これは何のために作ったんだっけ」「どこに落としたいと思っている？」"
QUESTION_D2 = "「どこまで出すつもりだった？」"
# (段の名前, 状態, 打ち手)。①は指示する側、②〜④はメンバーの側の不足。高い段ほど決めるまでが近い
STEPS = [
    ("①作業範囲の不理解", "推奨案まで出すことを期待されていると思っていない", "役割分担を明確に定義する"),
    ("②知識不足", "ゴールイメージと道筋が見えていない", "ゴールの完成形と、\nそこまでの活動の並びを見せる"),
    ("③相手視点の不足", "相手の業務や予算の事情を考えていない", "相手が何に困り、何で評価されるかを伝える"),
    ("④自信不足", "分かっていても、自分の意見を持てない", "仮説は外れてよいと伝え、\nレビュアーの仮の推奨に賛否を言わせる"),
]


def q_box(cx, y, s, h=60):
    w = sum(char_w(c, 21) for c in s) + 64
    return [f'  <rect x="{cx - w / 2:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="10" fill="{BLUE}"/>',
            text(cx, y + h / 2 + 8, s, 21, 700, "#ffffff", "middle")]


def chip(x0, x1, y, s, h=84):
    o = [f'  <rect x="{x0:.1f}" y="{y}" width="{x1 - x0:.1f}" height="{h}" rx="8" fill="#ffffff" stroke="{BLUE}" stroke-width="2"/>']
    ls = wrap(s, 19, x1 - x0 - 40)
    ty = y + h / 2 - (len(ls) - 1) * 14 + 7
    return o + [text((x0 + x1) / 2, ty + 28 * k, l, 19, 400, INK, "middle") for k, l in enumerate(ls)]


def branch(top_x, y0, xs, y1):
    # 答え方は問いの結果なので矢印にせず、問いの中央から枝分かれさせる
    mid = (y0 + y1) / 2
    o = [f'  <line x1="{top_x:.1f}" y1="{y0}" x2="{top_x:.1f}" y2="{mid}" stroke="{BLUE}" stroke-width="2.5"/>',
         f'  <line x1="{min(xs):.1f}" y1="{mid}" x2="{max(xs):.1f}" y2="{mid}" stroke="{BLUE}" stroke-width="2.5"/>']
    return o + [f'  <line x1="{x:.1f}" y1="{mid}" x2="{x:.1f}" y2="{y1}" stroke="{BLUE}" stroke-width="2.5"/>' for x in xs]


def arrow(x, y0, y1):
    return [f'  <line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y1 - 10}" stroke="{BLUE}" stroke-width="2.5"/>',
            f'  <polygon points="{x - 7:.1f},{y1 - 12} {x:.1f},{y1} {x + 7:.1f},{y1 - 12}" fill="{BLUE}"/>']


def fig_d():
    o = []
    n = len(STEPS)
    sw = (W - 2 * MARGIN - GAP * (n - 1)) / n
    col = [MARGIN + (sw + GAP) * i for i in range(n)]
    cx = [c + sw / 2 for c in col]
    chip_h = 84

    y = MARGIN
    o += q_box(W / 2, y, QUESTION_D)
    q1b = y + 60
    r1 = q1b + 64
    a_cx = (col[0] + col[1] + sw) / 2
    o += branch(W / 2, q1b, [a_cx, cx[2], cx[3]], r1)
    nw = sum(char_w(c, 19) for c in "出てこない") + 120
    o += chip(a_cx - nw / 2, a_cx + nw / 2, r1, "出てこない", chip_h)
    o += chip(col[2] + 10, col[2] + sw - 10, r1, "答えは返るが、理由が技術の話だけ", chip_h)
    o += chip(col[3] + 10, col[3] + sw - 10, r1, "すらすら出るが、自分ならどれを選ぶかに答えられない", chip_h)

    q2y = r1 + chip_h + 40
    o += arrow(a_cx, r1 + chip_h, q2y)
    o += q_box(a_cx, q2y, QUESTION_D2)
    r2 = q2y + 60 + 64
    o += branch(a_cx, q2y + 60, [cx[0], cx[1]], r2)
    o += chip(col[0] + 10, col[0] + sw - 10, r2, "調査までだと思っていた", chip_h)
    o += chip(col[1] + 10, col[1] + sw - 10, r2, "推奨案まで出すつもりだった", chip_h)

    base_h, rise = 300, 64
    floor = r2 + chip_h + 50 + base_h + rise
    heights = [base_h + rise * i for i in range(n)]
    fills = [PALE, MID, HEAD, BLUE]
    for i, (name, state, act) in enumerate(STEPS):
        h = heights[i]
        top = floor - h
        start = r2 + chip_h if i < 2 else r1 + chip_h
        o += arrow(cx[i], start, top)
        fg = "#ffffff" if i == n - 1 else INK
        sub = "#ffffff" if i == n - 1 else BLUE
        o.append(f'  <rect x="{col[i]:.1f}" y="{top:.1f}" width="{sw:.1f}" height="{h}" fill="{fills[i]}"/>')
        o.append(text(col[i] + 24, top + 44, name, 26, 700, fg))
        ls, k = lines_at(col[i] + 24, top + 88, state, 19, sw - 48, fg, lh=30)
        o += ls
        o.append(text(col[i] + 24, top + 88 + 30 * k + 14, "レビュアーの打ち手", 16, 700, sub))
        o += lines_at(col[i] + 24, top + 88 + 30 * k + 46, act, 19, sw - 48, fg, lh=30)[0]

    # ①は役割を渡すレビュアーの側、②〜④はメンバーの側に原因がある
    by = floor + 18
    for c0, c1, label in [(0, 0, "指示不足"), (1, 3, "能力不足")]:
        x0 = col[c0] + 8
        x1 = col[c1] + sw - 8
        o.append(f'  <path d="M{x0:.1f},{by} v12 H{x1:.1f} v-12" fill="none" stroke="{BLUE}" stroke-width="2"/>')
        o.append(text((x0 + x1) / 2, by + 46, label, 20, 700, BLUE, "middle"))
    return page(by + 46 + MARGIN + 8, o)


if __name__ == "__main__":
    outs = {
        "review_b_stages.svg": fig_b(),
        "review_c_questions.svg": fig_c(),
        "review_d_ladder.svg": fig_d(),
    }
    for name, s in outs.items():
        (OUT / name).write_text(s, encoding="utf-8")
        print(OUT / name)
