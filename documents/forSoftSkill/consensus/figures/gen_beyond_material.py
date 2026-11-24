"""ベテランの視点「合意は資料を出した後の会話で決まる」の図。

相手の価値判断は三角形のピラミッドで、頂点に目指す姿がある（頂点はボックスから少しだけ出す）。資料が紐づけるのは、技術判断を従属させる
1段上の価値判断だけ。自分たちと相手はまずそこで話し、それを土台に頂点の目指す姿を話す。
"""
from pathlib import Path

W, H = 1000, 750
CROP_TOP = 128                        # 目指す姿より上の空白を切る
BLUE, INK, SUB, ORANGE, GRAY = "#2b5f83", "#1b2026", "#4a5568", "#b5562a", "#6a7179"

PYR_BOTTOM_Y = 540                    # 相手の価値判断のピラミッドの底辺
APEX_OUT = 22                         # 頂点がボックスの上端から出る高さ
TOP = (370, 170, 260, 128)             # 目指す姿。ピラミッドの頂点はこの上端から少し出す
MID = (280, 410, 440, 110)            # 今回の判断に効く価値判断
TECH = (280, 600, 440, 110)


def box(x, y, w, h, name, body, fill, stroke, dashed=False, note=None):
    dash = ' stroke-dasharray="9 7"' if dashed else ""
    out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"{dash}/>'
           f'<text x="{x + 28}" y="{y + 46}" font-size="26" font-weight="700" fill="{INK}">{name}</text>'
           f'<text x="{x + 28}" y="{y + 78}" font-size="18" fill="{SUB}">{body}</text>')
    if note:
        out += f'<text x="{x + 28}" y="{y + 108}" font-size="16" fill="{ORANGE}">{note}</text>'
    return out


def pill(cx, cy, label, fill):
    return (f'<rect x="{cx - 64}" y="{cy - 24}" width="128" height="48" rx="24" fill="{fill}"/>'
            f'<text x="{cx}" y="{cy + 8}" font-size="22" font-weight="700" fill="#ffffff" text-anchor="middle">{label}</text>')


def arrow(x1, y1, x2, y2, color, marker, width=3, dashed=False):
    dash = ' stroke-dasharray="8 6"' if dashed else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{dash} marker-end="url(#{marker})"/>'


def text_lines(x, y0, texts, color, anchor="start", size=17, step=26, bold=True):
    body = "".join(f'<text x="{x}" y="{y0 + i * step}">{t}</text>' for i, t in enumerate(texts))
    weight = ' font-weight="700"' if bold else ""
    return f'<g font-size="{size}"{weight} fill="{color}" text-anchor="{anchor}">{body}</g>'


def main():
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {CROP_TOP} {W} {H - CROP_TOP}" width="{W}" height="{H - CROP_TOP}" font-family="Noto Sans CJK JP, sans-serif">',
        "<defs>"
        + "".join(
            f'<marker id="{i}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
            for i, c in (("ab", BLUE), ("ao", ORANGE), ("ag", GRAY))
        )
        + "</defs>",
        f'<rect y="{CROP_TOP}" width="{W}" height="{H - CROP_TOP}" fill="#ffffff"/>',
    ]

    mx, my, mw, mh = MID
    tx, ty, tw, th = TECH
    cx = mx + mw / 2

    gx, gy, gw, gh = TOP
    apex_y = gy - APEX_OUT
    # 底辺は資料の範囲の枠の内側に収める
    half = mw / 2 + 30 - 12
    parts.append(f'<path d="M{cx} {apex_y} L{cx + half} {PYR_BOTTOM_Y} L{cx - half} {PYR_BOTTOM_Y} Z" '
                 f'fill="#e4eef5" stroke="#a6c6da" stroke-width="2" stroke-linejoin="round"/>')
    parts.append(f'<text x="{cx - 22}" y="{gy + gh + 80}" font-size="16" letter-spacing="1" fill="{BLUE}" text-anchor="end">相手の価値判断</text>')
    parts.append(box(*TOP, "目指す姿", "そもそも何のためか", "#ffffff", "#a6c6da", dashed=True, note="資料では仮に定めている"))

    parts.append(box(*MID, "今回の判断の優先度", "何を優先し、何を諦めるか", "#ffffff", "#a6c6da"))
    parts.append(box(*TECH, "技術判断", "どの案を採るか", "#fbfaf7", "#c9d1da"))

    # 技術判断は1段上の価値判断に従属する
    parts.append(arrow(cx, my + mh + 6, cx, ty - 8, GRAY, "ag"))
    parts.append(f'<text x="{cx + 14}" y="{(my + mh + ty) // 2 + 6}" font-size="16" font-weight="700" fill="{GRAY}">従属させる</text>')

    # 資料の範囲は、技術判断と1段上の価値判断だけ
    top, bottom = my - 16, ty + th + 16
    parts.append(f'<rect x="{mx - 30}" y="{top}" width="{mw + 60}" height="{bottom - top}" rx="20" fill="none" stroke="{BLUE}" stroke-width="2.5" stroke-dasharray="4 6"/>')
    parts.append(text_lines(mx - 44, bottom - 40, ["資料の範囲"], BLUE, anchor="end", size=18))

    # 目指す姿が見えたら、今回の判断の軸を見つめ直す
    y_hi, y_lo = gy + gh + 8, my - 22
    parts.append(arrow(cx, y_hi, cx, y_lo, BLUE, "ab", 4))
    parts.append(text_lines(cx + 16, (y_hi + y_lo) // 2 + 6, ["判断軸を見つめ直す"], BLUE))

    # アクター: 今回の判断の優先度とは同じ高さで向き合い、頂点の目指す姿は斜め上に見上げる
    act_y = my + mh / 2
    lx, rx = 70, W - 70
    parts.append(pill(lx, act_y, "自分たち", GRAY))
    parts.append(pill(rx, act_y, "相手", BLUE))
    parts.append(arrow(lx + 40, act_y - 26, gx - 6, gy + gh / 2, GRAY, "ag", dashed=True))
    parts.append(arrow(lx + 66, act_y, mx - 6, act_y, GRAY, "ag"))
    parts.append(arrow(rx - 40, act_y - 26, gx + gw + 6, gy + gh / 2, BLUE, "ab", dashed=True))
    parts.append(arrow(rx - 66, act_y, mx + mw + 6, act_y, BLUE, "ab"))
    parts.append(text_lines(24, gy + 52, ["「もともと、やりたいことは", "何だったんでしょうか？」"], ORANGE))
    parts.append(text_lines(rx, gy + 65, ["改めて考える"], BLUE, anchor="middle"))

    parts.append("</svg>")
    (Path(__file__).parents[1] / "images" / "beyond_material.svg").write_text("\n".join(parts), encoding="utf-8")


if __name__ == "__main__":
    main()
