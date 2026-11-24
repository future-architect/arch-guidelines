"""Appendix「一般的な合意形成術との関係」の図。ハーバード流交渉術の4原則と、本書の手続き1〜9 の対応。

python3 figures/gen_harvard_map.py で images/harvard_map.svg を作る。配色は gen_reaction_stages.py に揃える。
"""
from pathlib import Path

from gen_review_figs import page, lines_at, text, BLUE, PALE, INK, HEAD, MARGIN, W

GREY, GREY_INK = "#eef1f4", "#7a8793"
STEPS = ["だれと合意するか", "落としどころ", "案出し", "観点ごとの評価", "評価軸の組み替え",
         "コンセプト別の選択肢", "ストーリーと伝え方", "反応を引き出し合意", "クロージング"]
# (原則, 補足, {手続き番号: セルの文}) 。セルの文が空なら ● だけ
ROWS = [
    ("人と問題を分ける", "", {1: "", 7: "7-1", 8: "8-1"}),
    ("立場ではなく利害に注目する", "", {2: "2-1"}),
    ("複数の選択肢を用意する", "", {3: ""}),
    ("客観的な基準を使う", "", {4: "", 5: "", 6: ""}),
]


def fig():
    o = []
    gap = 6
    lw = 300
    n = len(STEPS)
    cw = (W - 2 * MARGIN - lw - gap * n) / n
    xs = [MARGIN + lw + gap + (cw + gap) * i for i in range(n)]
    y = MARGIN
    hh = 104
    # 見出しは手続きの行と区別するため背景を付けず、4原則の列の直上に寄せる
    o.append(text(MARGIN + 4, y + hh - 12, "ハーバード流交渉術の4原則", 18, 700, BLUE))
    tip = 14
    for i, (x, s) in enumerate(zip(xs, STEPS)):
        # 手続きは順に踏むのでホームベース型でつなぐ。4原則は流れではないので下の行に置く
        x2 = x + cw + gap - 2
        notch = tip if i else 0
        pts = f"{x:.1f},{y} {x2 - tip:.1f},{y} {x2:.1f},{y + hh / 2} {x2 - tip:.1f},{y + hh} {x:.1f},{y + hh} {x + notch:.1f},{y + hh / 2}"
        o.append(f'  <polygon points="{pts}" fill="{HEAD}"/>')
        cx = x + (cw + gap - 2 + notch - tip) / 2
        o.append(text(cx, y + 30, f"手続き{i + 1}", 15, 700, BLUE, "middle"))
        ls, _ = lines_at(cx, y + 58, s, 15, cw - 22, weight=700, anchor="middle")
        o += ls
    y += hh + gap
    rh = 70
    for r, (name, sub, cells) in enumerate(ROWS):
        last = False
        # 4原則は上から下へつながるホームベース型で並べる
        tipv = 22
        notch = 0
        x1, xr, yb = MARGIN, MARGIN + lw, y + rh + gap - 2
        pts = (f"{x1},{y} {x1 + lw / 2},{y + notch} {xr},{y} {xr},{yb - tipv} "
               f"{x1 + lw / 2},{yb} {x1},{yb - tipv}")
        o.append(f'  <polygon points="{pts}" fill="{HEAD}"/>')
        ink = GREY_INK if last else INK
        if sub:
            o.append(text(MARGIN + 16, y + 30, name, 18, 700, ink))
            o.append(text(MARGIN + 16, y + 55, sub, 15, 400, ink))
        else:
            o.append(text(MARGIN + 16, y + (rh - tipv + gap) / 2 + 6, name, 18, 700, ink))
        for i, x in enumerate(xs):
            on = (i + 1) in cells
            fill = (GREY if last else PALE) if on else "#f7f9fa"
            o.append(f'  <rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="{rh}" fill="{fill}"/>')
            if on:
                mark = cells[i + 1]
                color = GREY_INK if last else BLUE
                if mark:
                    o.append(text(x + cw / 2, y + rh / 2 + 7, mark, 19, 700, color, "middle"))
                else:
                    o.append(text(x + cw / 2, y + rh / 2 + 9, "●", 24, 700, color, "middle"))
        y += rh + gap
    return page(y - gap + MARGIN, o)


if __name__ == "__main__":
    out = Path(__file__).parents[1] / "images" / "harvard_map.svg"
    out.write_text(fig(), encoding="utf-8")
    print(out)
