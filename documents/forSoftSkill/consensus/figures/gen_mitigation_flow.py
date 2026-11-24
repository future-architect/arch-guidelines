"""Appendix「緩和策は、4つの型から考える」の決定フロー図。

python3 figures/gen_mitigation_flow.py で images/mitigation_flow.svg を作る。
回避・低減・転嫁・受容の順に問い、できなければ次の型へ進む。型の説明と例も図に持たせ、本文に箇条書きを置かない。
配色は gen_reaction_stages.py に揃える。
"""
from pathlib import Path

from gen_reaction_stages import BLUE, PALE, HEAD, INK, text
from gen_step_flow import wrap

W = 1560
QX, QW = 30, 520            # 問いの列
PX, PW = 640, 430           # 緩和策パターンの列
EX, EW = 1086, 444          # 例の列
TOP = 100                   # 列見出しの下端
ROW0, RH, STEP = 128, 126, 168
GRAY = "#6a7179"

START = "相手が許容できない弱みがある"
QUESTIONS = [
    "弱みが生じる条件そのものを外せるか",
    "起こりやすさか、起きたときの影響を小さくできるか",
    "影響を引き受けられる別の主体がいるか",
]
PATTERNS = [
    ("回避", "弱みが生じる条件そのものを外す", "見込みが立つまで専用の環境を作らない"),
    ("低減", "起こりやすさか、起きたときの影響を小さくする", "リハーサルを増やす、戻す手順を決めておく"),
    ("転嫁", "影響を別の主体に移す", "運用を自分たちが引き受ける、保守契約で賄う"),
    ("受容", "手を打たずに受け入れ、起きたときの対応だけを決めておく", "受け入れる理由を書き添える"),
]


def block(x, y, s, size, width, fill, weight=400, anchor="start", lh=None):
    lh = lh or size * 1.5
    return [text(x, y + lh * k, l, size, weight, fill, anchor) for k, l in enumerate(wrap(s, size, width))]


def line(points, label=None, lx=0, ly=0):
    d = " ".join(f"{'M' if i == 0 else 'L'}{x:.0f},{y:.0f}" for i, (x, y) in enumerate(points))
    out = [f'  <path d="{d}" fill="none" stroke="{GRAY}" stroke-width="2.5" marker-end="url(#a)"/>']
    if label:
        out.append(text(lx, ly, label, 18, 700, GRAY))
    return out


def row(y, q=None, pattern=None):
    o = []
    if q:
        o.append(f'  <rect x="{QX}" y="{y}" width="{QW}" height="{RH}" rx="12" fill="{PALE}" stroke="{HEAD}" stroke-width="2"/>')
        n = len(wrap(q, 22, QW - 60))
        o += block(QX + QW / 2, y + RH / 2 + 8 - (n - 1) * 16, q, 22, QW - 60, INK, 700, "middle", lh=32)
    # 型と例は表として読ませるため角を立て、角丸の問い（フロー）と見分けられるようにする
    name, desc, ex = pattern
    o.append(f'  <rect x="{PX}" y="{y}" width="{PW}" height="{RH}" fill="{BLUE}"/>')
    o.append(text(PX + 26, y + 40, name, 26, 700))
    o += block(PX + 26, y + 74, desc, 18, PW - 52, "#ffffff", lh=27)
    o.append(f'  <rect x="{EX}" y="{y}" width="{EW}" height="{RH}" fill="#ffffff" stroke="{HEAD}" stroke-width="2"/>')
    n = len(wrap(ex, 19, EW - 52))
    o += block(EX + 26, y + RH / 2 + 7 - (n - 1) * 14, ex, 19, EW - 52, INK, lh=29)
    return o


def fig():
    qc = QX + QW / 2
    o = [f'<defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="{GRAY}"/></marker></defs>']
    o.append(f'  <rect x="{qc - 210}" y="24" width="420" height="56" rx="28" fill="#ffffff" stroke="{BLUE}" stroke-width="2"/>')
    o.append(text(qc, 60, START, 20, 700, BLUE, "middle"))
    for x, w, label in ((PX, PW, "緩和策パターン"), (EX, EW, "例")):
        o.append(f'  <rect x="{x}" y="36" width="{w}" height="{TOP - 36 - 14}" fill="{HEAD}"/>')
        o.append(text(x + w / 2, 36 + (TOP - 50) / 2 + 7, label, 20, 700, INK, "middle"))
    o += line([(qc, 82), (qc, ROW0 - 6)])
    for i, q in enumerate(QUESTIONS):
        y = ROW0 + STEP * i
        o += row(y, q, PATTERNS[i])
        o += line([(QX + QW + 4, y + RH / 2), (PX - 8, y + RH / 2)], "はい", QX + QW + 22, y + RH / 2 - 12)
        if i < len(QUESTIONS) - 1:
            o += line([(qc, y + RH + 2), (qc, y + STEP - 6)], "いいえ", qc + 12, y + RH + 30)
    y_last = ROW0 + STEP * len(QUESTIONS)
    o += row(y_last, pattern=PATTERNS[-1])
    y3 = ROW0 + STEP * (len(QUESTIONS) - 1)
    o += line([(qc, y3 + RH + 2), (qc, y_last + RH / 2), (PX - 8, y_last + RH / 2)], "いいえ", qc + 12, y3 + RH + 30)
    h = y_last + RH + 30
    head = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" font-family="Noto Sans CJK JP, sans-serif">',
            f'  <rect width="{W}" height="{h}" fill="#ffffff"/>']
    return "\n".join(head + o + ["</svg>", ""])


if __name__ == "__main__":
    out = (Path(__file__).parents[1] / "images" / "mitigation_flow.svg")
    out.write_text(fig(), encoding="utf-8")
    print(out)
