"""翻訳の軸（観点 → 制約・評価 → 既成の軸 → QCD の中身）を横向きのツリーで、重みの軸を別枠で SVG に書き出す。

python3 figures/gen_axis_tree.py で images/axis_tree.svg を作る。
スライドの Appendix「翻訳の軸」と同じ木を、本書の手順図と同じ色とフォントで描く。
"""
from html import escape
from pathlib import Path

from gen_step_flow import wrap

BW = 140
STUB = 14
VGAP = 10
MARGIN = 16
TITLE = 15
SUB = 12

# 背景色の意味はスライドの凡例と同じ。big=大分類に使えそうな軸、small=小分類・中分類に使えそうな軸、struct=分け方の構造
STYLE = {
    "big": ("#e4eef5", "#a6c6da", "#1b2026"),
    "small": ("#fbfaf7", "#d7dce1", "#1b2026"),
    "struct": ("#ffffff", "#c0c7ce", "#4a5568"),
}


def n(title, sub="", kind="struct", children=()):
    return {"title": title, "sub": sub, "kind": kind, "children": list(children)}


TREE = n("観点", "比較表の1行", children=[
    n("制約", children=[
        n("技術制約", "相手の既存環境に載らない、自分たちの技術方針に反する。例: 閉域網でつながるのは AWS だけ"),
        n("ビジネス制約", "相手の方針、法規制、契約。例: IT 方針で GCP は使えない"),
    ]),
    n("評価", children=[
        n("ボトムアップ", "束ねる。手元の評価項目を似たもの同士でまとめる", children=[
            n("関心事", "題材ごとに作る小分類。相手が読める最初の粒度。MECE ではない", "small"),
        ]),
        n("トップダウン", "借りる。題材と無関係に先にある既成の軸を当てる", children=[
            n("QCD", "品質、コスト、納期", "struct", [
                n("Q 品質", "", "big", [
                    n("機能要件", "機能適合性", "small"),
                    n("非機能要件", "", "small", [
                        n("性能効率性", "", "small"),
                        n("信頼性", "可用性、障害許容性、回復性", "small"),
                        n("セキュリティ", "", "small", [
                            n("外部脅威", "サイバー攻撃、不正侵入", "small"),
                            n("内部脅威", "誤操作、内部不正、コンプライアンス", "small"),
                        ]),
                        n("保守性", "改修や運用のしやすさ", "small"),
                        n("その他", "互換性、使用性、移植性", "small"),
                    ]),
                ]),
                n("C コスト", "初期費用、運用費用、体制", "big"),
                n("D 納期", "導入期間、日程の確実性", "big"),
            ]),
        ]),
    ]),
])

# 重みの軸は木の階層を作らず、分けた行ごとに添える。QCD と兄弟に置くと、どちらか一方を選ぶように読めるため木から外す
WEIGHTS = [
    ("攻め・守り", "事業を伸ばすか、リスクを抑えるか"),
    ("短期・中期・長期", "いつ効いてくるか"),
    ("フェーズ", "設計・構築・保守運用。\nどの工程で効くか"),
    ("戦略・戦術", "事業の方向を決めるものか、実行の巧拙か"),
    ("内部・外部", "社内に効くか、社外に効くか"),
]


def measure(node):
    node["tl"] = wrap(node["title"], TITLE, BW - 20)
    node["sl"] = wrap(node["sub"], SUB, BW - 20) if node["sub"] else []
    node["h"] = 20 + 20 * len(node["tl"]) + (4 + 16 * len(node["sl"]) if node["sl"] else 0)
    for c in node["children"]:
        measure(c)


def layout(node, depth):
    """部分木を原点 0 に置き、深さごとの上端・下端（輪郭）を返す。

    兄弟の部分木は、同じ深さの列だけが重ならないように詰める。
    浅い葉（技術制約など）が、深い部分木の脇の空いた行に入れるようにするため。
    """
    if not node["children"]:
        node["y"] = 0.0
        return {depth: (0.0, node["h"])}
    contour, placed = {}, []
    for c in node["children"]:
        cc = layout(c, depth + 1)
        off = 0.0
        if contour:
            off = max((contour[d][1] + VGAP - cc[d][0] for d in cc if d in contour), default=0.0)
        shift(c, off)
        for d, (t, b) in cc.items():
            t, b = t + off, b + off
            contour[d] = (min(contour[d][0], t), max(contour[d][1], b)) if d in contour else (t, b)
        placed.append(c)
    first, last = placed[0], placed[-1]
    mid = (first["y"] + first["h"] / 2 + last["y"] + last["h"] / 2) / 2
    node["y"] = mid - node["h"] / 2
    contour[depth] = (node["y"], node["y"] + node["h"])
    return contour


def shift(node, dy):
    node["y"] += dy
    for c in node["children"]:
        shift(c, dy)


def bounds(node):
    ys = [(node["y"], node["y"] + node["h"])]
    for c in node["children"]:
        ys += bounds(c)
    return ys


def draw(node, depth, o):
    x = MARGIN + depth * (BW + 2 * STUB)
    fill, stroke, color = STYLE[node["kind"]]
    o.append(f'  <rect x="{x}" y="{node["y"]:.1f}" width="{BW}" height="{node["h"]}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
    y = node["y"] + 10 + 15
    for line in node["tl"]:
        o.append(f'  <text x="{x + 10}" y="{y:.1f}" font-size="{TITLE}" font-weight="700" fill="{color}">{escape(line)}</text>')
        y += 20
    y += 2
    for line in node["sl"]:
        o.append(f'  <text x="{x + 10}" y="{y:.1f}" font-size="{SUB}" fill="#6a7179">{escape(line)}</text>')
        y += 16
    if node["children"]:
        cy = node["y"] + node["h"] / 2
        bx = x + BW + STUB
        tops = [c["y"] + c["h"] / 2 for c in node["children"]]
        o.append(f'  <path d="M{x + BW},{cy:.1f} H{bx}" stroke="#a6c6da" stroke-width="2" fill="none"/>')
        o.append(f'  <path d="M{bx},{min(tops + [cy]):.1f} V{max(tops + [cy]):.1f}" stroke="#a6c6da" stroke-width="2" fill="none"/>')
        for t in tops:
            o.append(f'  <path d="M{bx},{t:.1f} H{bx + STUB}" stroke="#a6c6da" stroke-width="2" fill="none"/>')
        for c in node["children"]:
            draw(c, depth + 1, o)


def depth_of(node):
    return 1 + max((depth_of(c) for c in node["children"]), default=0)


def svg():
    measure(TREE)
    layout(TREE, 0)
    ys = bounds(TREE)
    top = min(t for t, _ in ys)
    shift(TREE, MARGIN - top)
    tree_h = max(b for _, b in bounds(TREE))
    W = 2 * MARGIN + depth_of(TREE) * (BW + 2 * STUB) - 2 * STUB
    legend_y = tree_h + 24
    px = MARGIN + 2 * (BW + 2 * STUB)
    pw = W - px - MARGIN
    cw = (pw - 24 - 4 * 12) / 5
    chips = [(t, wrap(d, SUB, cw - 20)) for t, d in WEIGHTS]
    chip_h = 20 + 20 + 4 + 16 * max(len(l) for _, l in chips)
    ph = 12 + 24 + 8 + chip_h + 12
    H = int(max(legend_y + 3 * 26, legend_y + ph) + MARGIN)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Noto Sans CJK JP, sans-serif">',
         f'  <rect width="{W}" height="{H}" fill="#ffffff"/>']
    draw(TREE, 0, o)
    o.append(f'  <rect x="{px}" y="{legend_y}" width="{pw}" height="{ph}" rx="10" fill="#ffffff" stroke="#a6c6da" stroke-width="1.5" stroke-dasharray="6 4"/>')
    o.append(f'  <text x="{px + 12}" y="{legend_y + 30}" font-size="{TITLE}" font-weight="700" fill="#1b2026">重みの軸<tspan font-size="13" font-weight="400" fill="#4a5568">　分けた行ごとに添え、相手がどう重みを置くかの向きを見る。相手のモードが明確なら、大分類にも使える</tspan></text>')
    fill, stroke, color = STYLE["big"]
    for i, (t, lines) in enumerate(chips):
        cx = px + 12 + i * (cw + 12)
        cy = legend_y + 12 + 24 + 8
        o.append(f'  <rect x="{cx:.1f}" y="{cy}" width="{cw:.1f}" height="{chip_h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        o.append(f'  <text x="{cx + 10:.1f}" y="{cy + 25}" font-size="{TITLE}" font-weight="700" fill="{color}">{escape(t)}</text>')
        for k, line in enumerate(lines):
            o.append(f'  <text x="{cx + 10:.1f}" y="{cy + 47 + 16 * k}" font-size="{SUB}" fill="#6a7179">{escape(line)}</text>')
    for i, (kind, label) in enumerate([("big", "大分類に使えそうな軸"), ("small", "小分類・中分類に使えそうな軸"), ("struct", "分け方の構造")]):
        fill, stroke, _ = STYLE[kind]
        y = legend_y + 26 * i
        o.append(f'  <rect x="{MARGIN}" y="{y}" width="24" height="18" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        o.append(f'  <text x="{MARGIN + 34}" y="{y + 14}" font-size="14" fill="#4a5568">{label}</text>')
    o.append('</svg>')
    return "\n".join(o) + "\n"


if __name__ == "__main__":
    here = Path(__file__).parents[1] / "images"
    (here / "axis_tree.svg").write_text(svg(), encoding="utf-8")
