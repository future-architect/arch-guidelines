"""ベテランの進め方（想定進行ごとに、どの手続きをどう省くか）を SVG で書き出す。

python3 figures/gen_veteran_flow.py で images/veteran_flows.svg を作る。
配色と折り返しは手続きの流れ図（gen_step_flow.py）に揃える。
"""
from html import escape
from pathlib import Path

from gen_step_flow import MARGIN, wrap

# 手続きの流れ図（1520）より狭いのは、ドキュメントの本文幅に縮めても文字が読める大きさに保つため
W = 1200
GAP = 22
# 列が増えても縮尺が変わらないよう、カードの幅は5列で割った幅に固定する
SLOTS = 5

STAGES = [
    ("準備", [
        ("1", "決めなければならないことを洗い出す", "前提を列挙し、WBS と課題一覧を精緻に作る"),
        ("2", "落としどころを考える", "課題一覧に粗く言葉で書く"),
        ("3", "取りうる案を考える", "頭の中でやる。手は動かさない"),
    ]),
    ("初回打合せ\n（計画の頭出し）", [
        ("8", "相手の反応を引き出す", "計画を説明し、質問で相手を探る"),
    ]),
    ("テーマ別\n1回目", [
        ("5〜6", "評価軸に組み替え、コンセプト別の選択肢を作る", "探りを受けて、その場で\nトップダウンに決める"),
        ("7", "説明用のストーリーと伝え方を組み立てる", "論点と比較案を1枚の紙にまとめる"),
        ("4", "各案を観点ごとに評価する", "後付けの根拠づけ。AI や若手に任せる"),
    ]),
    ("テーマ別\n2回目", [
        ("8", "弱みを許容できるか確かめる", "外れた仮説と前提の変更をフォローする"),
        ("9", "クロージング", "2回で合意し、上位の会議体に先回りする"),
    ]),
]

SINGLE = [
    ("テーマ別\n1回目", [
        ("7", "説明用のストーリーと伝え方を組み立てる", "この相手はどこなら頷くかを先に決める"),
        ("6、5", "選択肢と評価軸に遡る", "主張を支える\nコンセプト別の選択肢と\n評価軸が揃っているか\n確かめる"),
        ("4", "各案を観点ごとに評価する", "主張を支えるファクトが揃っているか確かめる"),
    ]),
    STAGES[3],
]


def card(x, y, cw, num, name, gist):
    nl = wrap(name, 18, cw - 28)
    gl = wrap(gist, 17, cw - 28)
    gy = y + 52 + 25 * len(nl) + 12
    h = gy - y + 25 * len(gl) + 10
    bw = 44 if len(num) <= 2 else 58
    o = [f'  <rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{h}" rx="10" fill="#e4eef5" stroke="#a6c6da" stroke-width="2"/>',
         f'  <rect x="{x + 14:.1f}" y="{y + 14:.1f}" width="{bw}" height="26" rx="13" fill="#2b5f83"/>',
         f'  <text x="{x + 14 + bw / 2:.1f}" y="{y + 33:.1f}" font-size="16" font-weight="700" fill="#ffffff" text-anchor="middle">{escape(num)}</text>']
    for k, line in enumerate(nl):
        o.append(f'  <text x="{x + 14:.1f}" y="{y + 68 + 25 * k:.1f}" font-size="18" font-weight="700" fill="#1b2026">{escape(line)}</text>')
    o.append(f'  <line x1="{x + 14:.1f}" y1="{gy - 2:.1f}" x2="{x + cw - 14:.1f}" y2="{gy - 2:.1f}" stroke="#a6c6da" stroke-width="1"/>')
    for k, line in enumerate(gl):
        o.append(f'  <text x="{x + 14:.1f}" y="{gy + 22 + 25 * k:.1f}" font-size="17" fill="#1b2026">{escape(line)}</text>')
    return o, h


COMBINED_W = 1800
COL_GAP = 48
COL_HEADS = [("WBS 計画から関わる", STAGES), ("途中から単発で参画する", SINGLE)]


def stage_block(stages, left, top, cw):
    n = len(stages)
    head_lines = max(len(stage.split("\n")) for stage, _ in stages)
    head_h = 20 + 24 * head_lines
    body, col_bottom = [], []
    for i, (stage, steps) in enumerate(stages):
        x = left + i * (cw + GAP)
        body.append(f'  <rect x="{x:.1f}" y="{top}" width="{cw:.1f}" height="{head_h}" rx="10" fill="#2b5f83"/>')
        sl = stage.split("\n")
        y0 = top + (head_h - 24 * len(sl)) / 2 + 18
        for k, line in enumerate(sl):
            body.append(f'  <text x="{x + cw / 2:.1f}" y="{y0 + 24 * k:.1f}" font-size="18" font-weight="700" fill="#ffffff" text-anchor="middle">{escape(line)}</text>')
        if i < n - 1:
            ay = top + head_h / 2
            body.append(f'  <line x1="{x + cw + 2:.1f}" y1="{ay}" x2="{x + cw + GAP - 3:.1f}" y2="{ay}" stroke="#2b5f83" stroke-width="2.5" marker-end="url(#a)"/>')
        y = top + head_h + 22
        for j, (num, name, gist) in enumerate(steps):
            if j:
                body.append(f'  <line x1="{x + cw / 2:.1f}" y1="{y - 22:.1f}" x2="{x + cw / 2:.1f}" y2="{y - 3:.1f}" stroke="#2b5f83" stroke-width="2" marker-end="url(#a)"/>')
            o, h = card(x, y, cw, num, name, gist)
            body += o
            y += h + 26
        col_bottom.append(y - 26)
    return body, max(col_bottom)


def combined():
    W = COMBINED_W
    total = sum(len(st) for _, st in COL_HEADS)
    cw = (W - 2 * MARGIN - COL_GAP - GAP * (total - len(COL_HEADS))) / total
    head_h, top = 46, 16 + 46 + 18
    body, bottom, x = [], 0, MARGIN
    for k, (label, stages) in enumerate(COL_HEADS):
        width = len(stages) * cw + (len(stages) - 1) * GAP
        body.append(f'  <rect x="{x:.1f}" y="16" width="{width:.1f}" height="{head_h}" fill="#e4eef5"/>')
        body.append(f'  <text x="{x + width / 2:.1f}" y="{16 + 31}" font-size="20" font-weight="700" fill="#1b2026" text-anchor="middle">{escape(label)}</text>')
        o, b = stage_block(stages, x, top, cw)
        body += o
        bottom = max(bottom, b)
        if k == 0:
            lx = x + width + COL_GAP / 2
            body.append(f'  <line x1="{lx:.1f}" y1="16" x2="{lx:.1f}" y2="BOTTOM" stroke="#2b5f83" stroke-width="2.5"/>')
        x += width + COL_GAP
    H = int(bottom + 16)
    body = [b.replace('BOTTOM', str(H - 8)) for b in body]
    head = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Noto Sans CJK JP, sans-serif">',
            '  <defs>',
            '    <marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">',
            '      <path d="M0,0 L10,5 L0,10 z" fill="#2b5f83"/>',
            '    </marker>',
            '  </defs>',
            f'  <rect width="{W}" height="{H}" fill="#ffffff"/>']
    return "\n".join(head + body + ['</svg>']) + "\n"


if __name__ == "__main__":
    here = Path(__file__).parents[1] / "images"
    (here / "veteran_flows.svg").write_text(combined(), encoding="utf-8")
