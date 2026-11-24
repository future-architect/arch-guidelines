"""ケーススタディの目次ページの図。3つのケースの題材を横に並べて比べる。

python3 figures/gen_case_index.py で images/case_index.svg を作る。配色は gen_reaction_stages.py に揃える。
"""
from pathlib import Path

from gen_review_figs import page, lines_at, BLUE, PALE, INK, HEAD, MARGIN, W

ROWS = ["テーマ", "相手", "決めたいこと", "比べる案", "推奨", "判断をお願いすること"]
CASES = [
    ("マルチテナントのデータ分離方式", [
        "技術方式の選定",
        "人事・勤怠 SaaS の事業者。約3,000社に提供",
        "利用企業ごとのデータを、次期基盤でどう分けるか",
        "5つの方式を2案に絞る。全社で DB を共有する方式2 と、大手企業だけ専用 DB に分ける方式5",
        "方式5（大手企業の獲得を優先する案）",
        "契約の前に初期構築費と運用委託費の増加分を負って、大手企業の獲得を目指すか",
    ]),
    ("基幹システム刷新の移行方式", [
        "進め方の合意",
        "食品スーパーチェーン。約220店",
        "基幹システムを、どの順に新システムへ切り替えるか",
        "全店一斉、10店で検証してから一斉、エリアごとに3回、の3案",
        "案B（実店舗での検証を優先する案）",
        "一斉切り替えの日の影響を受け入れて案B を取るか、約2.5億円を追加して影響を約70店に抑える案C を取るか",
    ]),
    ("社内問い合わせへの生成AIの導入範囲", [
        "実施範囲の合意",
        "設備工事会社（電気・空調）。従業員約3,500人",
        "社内の問い合わせ対応に、生成AIをどこまで導入するか",
        "松竹梅の3案。梅は FAQ に答える、竹は規程と手順書も調べて出典を添えて答える、松は申請の起票まで",
        "竹",
        "梅より増える費用、文書の棚卸し、回答の誤りのおそれと引き換えに、規程の質問まで自己解決を広げるか",
    ]),
]


def fig():
    o = []
    gap = 10
    lw = 200
    cw = (W - 2 * MARGIN - lw - gap * 3) / 3
    xs = [MARGIN + lw + gap + (cw + gap) * i for i in range(3)]
    y = MARGIN
    hh = 92
    for i, (x, (name, _)) in enumerate(zip(xs, CASES), 1):
        o.append(f'  <rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="{hh}" rx="8" fill="{BLUE}"/>')
        o += lines_at(x + cw / 2, y + 26, f"ケーススタディ{i}", 15, cw - 30, fill="#ffffff", anchor="middle")[0]
        ls, n = lines_at(0, 0, name, 20, cw - 30, fill="#ffffff", weight=700, anchor="middle")
        ls, _ = lines_at(x + cw / 2, y + 58 - (n - 1) * 12 + 7, name, 20, cw - 30, fill="#ffffff", weight=700, anchor="middle")
        o += ls
    y += hh + gap
    size, lh, pad = 17, 27.2, 14
    for r, label in enumerate(ROWS):
        n = max(len(lines_at(0, 0, c[1][r], size, cw - 2 * pad)[0]) for c in CASES)
        rh = n * lh + 2 * pad
        o.append(f'  <rect x="{MARGIN}" y="{y}" width="{lw}" height="{rh}" fill="{HEAD}"/>')
        ls, k = lines_at(0, 0, label, 18, lw - 24, weight=700)
        ls, _ = lines_at(MARGIN + 14, y + rh / 2 - (k - 1) * 14.4 + 6, label, 18, lw - 24, weight=700)
        o += ls
        for x, (_, vals) in zip(xs, CASES):
            o.append(f'  <rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="{rh}" fill="{PALE}"/>')
            ls, _ = lines_at(x + pad, y + pad + 18, vals[r], 20 if r == 0 else size, cw - 2 * pad, fill=BLUE if r == 0 else INK, weight=700 if r in (0, len(ROWS) - 1) else 400)
            o += ls
        y += rh + gap
    return page(y - gap + MARGIN, o)


if __name__ == "__main__":
    out = Path(__file__).parents[1] / "images" / "case_index.svg"
    out.write_text(fig(), encoding="utf-8")
    print(out)
