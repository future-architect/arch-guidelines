"""Appendix の図（観点の分解と行き先）を SVG で書き出す。

python3 figures/gen_appendix_figs.py で images/appendix_axis_route.svg を作る。
配色と折り返しは手続きの流れ図（gen_step_flow.py）に揃える。
"""
from html import escape
from pathlib import Path

from gen_step_flow import wrap

# ベテランの視点の流れ図と同じ幅。本文幅に縮めても文字が読める大きさに保つため
W = 1200
M = 16
INK = "#1b2026"
SUB = "#6a7179"
DARK = "#2b5f83"
FILL = "#e4eef5"
LINE = "#a6c6da"
PALE = "#fbfaf7"
GRAY = "#d7dce1"


def head(w, h):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="Noto Sans CJK JP, sans-serif">',
            '  <defs>',
            '    <marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">',
            f'      <path d="M0,0 L10,5 L0,10 z" fill="{DARK}"/>',
            '    </marker>',
            '  </defs>',
            f'  <rect width="{w}" height="{h}" fill="#ffffff"/>']


def text(o, x, y, s, size, weight=400, fill=INK, anchor="start"):
    o.append(f'  <text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>')


def box(o, x, y, w, h, fill=FILL, stroke=LINE, dash=False, rx=10):
    d = ' stroke-dasharray="6 4"' if dash else ""
    o.append(f'  <rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"{d}/>')


def arrow(o, x1, y1, x2, y2, label="", lx=None, ly=None):
    o.append(f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{DARK}" stroke-width="2.5" marker-end="url(#a)"/>')
    if label:
        text(o, lx, ly, label, 15, 700, DARK)


# 観点の分解と行き先 -------------------------------------------------------------

QUESTIONS = [
    ("案を落とすか、比べるか", "落とす", ("制約", "✅❌の二値で判定し、❌の案を落とす。技術制約と、相手の方針・法規制・契約のようなビジネス制約がある"), "比べる（評価）"),
    ("案の間で差が出るか", "出ない", ("表から外す", ""), "出る"),
    ("相手の言葉に直せるか", "直せない", ("技術の差", "自分たちで決めて報告する"), "直せる（QCD や攻め・守りの軸に載る）"),
    ("意思決定の決め手になるか", "ならない", ("論点にしない", "差はあるが、相手の前提や他の行で結論が決まっていて、今回の文脈では重視されない"), "なる"),
]
WHO = [
    ("自分たちで決められる", "報告"),
    ("別の場ですでに決まっている", "確認"),
    ("相手の価値判断が要る", "論点"),
]
FORMS = [("基準への同意", "落とす条件、振り分ける条件"), ("重みの選択", "優先する軸"), ("弱みの許容", "推奨案の弱み")]


def axis_route():
    qx, qw, qh = M + 40, 380, 64
    lx = qx + qw + 150
    # 右端に、制約から論点へ下りる線を通す幅を空ける
    lw = W - M - lx - 50
    o = []
    y = M
    box(o, qx, y, qw, 54, "#ffffff", "#c0c7ce")
    text(o, qx + qw / 2, y + 34, "観点（比較表の1行）", 18, 700, anchor="middle")
    y += 54
    for q, no, (leaf, desc), yes in QUESTIONS:
        arrow(o, qx + qw / 2, y + 2, qx + qw / 2, y + 40)
        y += 42
        box(o, qx, y, qw, qh)
        text(o, qx + qw / 2, y + 40, q, 18, 700, anchor="middle")
        dl = wrap(desc, 15, lw - 28) if desc else []
        lh = 46 + 22 * len(dl)
        ly = y + qh / 2 - lh / 2
        arrow(o, qx + qw + 2, y + qh / 2, lx - 4, y + qh / 2, no, qx + qw + 20, y + qh / 2 - 10)
        box(o, lx, ly, lw, lh, PALE, GRAY)
        if leaf == "制約":
            con_y, con_bottom = y + qh / 2, ly + lh
        text(o, lx + 14, ly + 30, leaf, 17, 700)
        for k, line in enumerate(dl):
            text(o, lx + 14, ly + 54 + 22 * k, line, 15, fill=SUB)
        y += qh
        # 次の問いへ進む側のラベルは、下向きの矢印の右に添える
        text(o, qx + qw / 2 + 14, y + 26, yes, 15, 700, DARK)
    arrow(o, qx + qw / 2, y + 2, qx + qw / 2, y + 40)
    y += 42
    box(o, qx, y, qw, qh)
    text(o, qx + qw / 2, y + 40, "だれが決められるか", 18, 700, anchor="middle")
    y += qh
    # 3つの行き先を「相手へのコミュニケーション」の枠に入れる。
    # 報告と確認は細くし、論点の3つの形が目立つようにする
    fy = y + 40
    pad, gap, sw = 16, 16, 170
    ty = fy + pad
    bh = 64 + 90 + 14
    pw = W - 2 * M - 2 * pad - 2 * (sw + gap)
    box(o, M, fy, W - 2 * M, pad + bh + 44, "#ffffff", "#9aa3ab", dash=True, rx=12)
    text(o, M + pad, fy + pad + bh + 30, "相手へのコミュニケーション（5形式）", 16, 700, DARK)
    for i, (cond, dest) in enumerate(WHO):
        last = i == len(WHO) - 1
        cx = M + pad + i * (sw + gap)
        cw = pw if last else sw
        o.append(f'  <path d="M{qx + qw / 2:.1f},{y + 2:.1f} V{y + 20:.1f} H{cx + cw / 2:.1f} V{ty - 4:.1f}" stroke="{DARK}" stroke-width="2.5" fill="none" marker-end="url(#a)"/>')
        box(o, cx, ty, cw, bh if last else 96, DARK if last else PALE, DARK if last else GRAY)
        fill = "#ffffff" if last else INK
        text(o, cx + cw / 2, ty + 32, dest, 18, 700, fill, "middle")
        for j, line in enumerate(wrap(cond, 13, cw - 20)):
            text(o, cx + cw / 2, ty + 54 + 18 * j, line, 13, fill="#dfe8ef" if last else SUB, anchor="middle")
        if last:
            fw = (cw - 24 - (len(FORMS) - 1) * 8) / len(FORMS)
            for k, (what, form) in enumerate(FORMS):
                fx = cx + 12 + k * (fw + 8)
                box(o, fx, ty + 68, fw, 88, "#ffffff", "#ffffff", rx=8)
                text(o, fx + fw / 2, ty + 68 + 32, what, 16, 700, DARK, "middle")
                for j, line in enumerate(wrap(form, 13, fw - 10)):
                    text(o, fx + fw / 2, ty + 68 + 56 + 18 * j, line, 13, fill=INK, anchor="middle")
    # 制約の線を自分たちだけで引けないときは、基準への同意の論点になる
    rx = W - M - 30
    o.append(f'  <path d="M{lx + lw + 2:.1f},{con_y:.1f} H{rx:.1f} V{ty - 4:.1f}" stroke="{DARK}" stroke-width="2.5" stroke-dasharray="7 5" fill="none" marker-end="url(#a)"/>')
    text(o, rx - 8, con_bottom + 22, "線を相手の価値判断で引くなら、基準への同意の論点へ", 14, 700, DARK, "end")
    H = int(fy + pad + bh + 44 + M)
    return "\n".join(head(W, H) + o + ["</svg>"]) + "\n"


# 進め方の依存関係 ---------------------------------------------------------------


if __name__ == "__main__":
    here = Path(__file__).parents[1] / "images"
    (here / "appendix_axis_route.svg").write_text(axis_route(), encoding="utf-8")
