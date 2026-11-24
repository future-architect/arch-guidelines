"""手続きごとの手順フロー図（手順 → アウトプット、各手順の躓き）を SVG で書き出す。

python3 figures/gen_step_flow.py で images/procedure{N}_flow.svg を作る。
全図の幅を 1520 に揃え、手順の数が違っても文字の大きさが図ごとに変わらないようにしている。
"""
from html import escape
from pathlib import Path

W = 1520
MARGIN = 15
GAP = 30
OUT_W = 188

STEPS = {
    1: ("決めたいことの一覧\n決める順序", [
        ("1-1", "検討課題を分解してタスク化する", ""),
        ("1-2", "確認事項と相談事項を区別する", "本来相談すべきことを確認として問い、相手に答えを求めすぎる"),
        ("1-3", "相手側のキーマンを確かめる", "だれ向けの資料かを決めないまま作る。担当外の相手に判断を求める"),
        ("1-4", "影響の大きさや依存関係から優先度付けする", "話しやすい議題から始め、前提になる議題が未決だと後で気づく"),
    ]),
    2: ("落としどころの仮説", [
        ("2-1", "背景資料から、相手の判断軸に当たりをつける", "一般論での当たりとなり、説得力に欠く"),
        ("2-2", "粗案を3〜4つ並べる", ""),
        ("2-3", "自分の言葉で、落としどころの仮説を作る", "ユースケースや要件が決まらないことを理由に、仮説を作らずに待つ"),
        ("2-4", "推し案が浮かぶ理由を言葉にする", "推し案の理由が「なんとなく」のまま比較に入り、「主観が入りすぎ」と言われて崩れる"),
    ]),
    3: ("案の一覧", [
        ("3-1", "案を出す", "「この案は検討した？」と一覧に無い案を聞かれ、検討不足と見られる"),
        ("3-2", "亜種を代表パターンにまとめる", "亜種を並べたまま比較表に載せ、列が増えて違いが見えなくなる"),
    ]),
    4: ("比較表", [
        ("4-1", "制約で足切りし、候補を絞る", "全候補を精緻に比べようとして破綻する"),
        ("4-2", "観点を挙げ、技術的に評価する", ""),
        ("4-3", "前提を確かめ、プロジェクト文脈を加えて再評価する", "一般論の✅⚠️❌のまま進む"),
        ("4-4", "観点を、差・制約・差なしに仕分ける", "差の出ない観点まで残し、どこが論点かが埋もれる"),
        ("4-5", "推奨案について自分たちの仮説を検証する", "推奨が無いため自分たちの意思が見えず、相手任せに見える"),
    ]),
    5: ("評価軸", [
        ("5-1", "評価観点を、相手の関心事に紐づける", "技術的な評価観点のまま提示し、相手が判断できない"),
        ("5-2", "一般的に用いられる MECE な軸を利用し、網羅性を確認する", "なぜこの軸かと問われて答えられない"),
        ("5-3", "各評価軸を、プロジェクト文脈を加味して自然な言葉にする", "数百ミリ秒、RPO 15分を\nそのまま出し、相手が自分たちの使われ方に置き換えられない"),
        ("5-4", "だれに説明するかに合わせて、ビジネス文脈への翻訳レベルを変える", "技術が分かる相手と翻訳しないまま\n合意し、業務側の条件が後から出て手戻る"),
    ]),
    6: ("コンセプト別の\n選択肢", [
        ("6-1", "差が出ない評価軸を、論点から省けないか見極める", "翻訳できない技術の差を論点に残し、相手の価値判断が要る差を落とす"),
        ("6-2", "決め手になる行だけ、文脈を注入して評価の精度を上げる", ""),
        ("6-3", "案にコンセプト名をつけ、デメリットを整理する", "案1、案2 のまま並べ、「どれがよいですか」と聞く"),
        ("6-4", "推奨の仮説を添えた問いにする", "「どうですか」とだけ問い、自分たちが何を良いと考えているかを言わない"),
    ]),
    7: ("ストーリー\n伝え方の計画", [
        ("7-1", "推奨案と論点、背景、案の集合、受け入れる弱みの順にストーリーを組み立てる", "表をどう作ったかから説明し、相手が「今何の時間？」と迷子になる。推奨案だけ示し、弱みを伏せる"),
        ("7-2", "相手の反応を予想し、疑問が出そうな箇所には補足を入れる", "想定していない質問で止まり、持ち帰りになる"),
        ("7-3", "相手の負荷と時間の制約から、伝え方を計画する", "一度に話す情報量が多すぎて相手がついて行けなくなる"),
    ]),
    8: ("相手の価値基準\n受け入れる弱み", [
        ("8-1", "背景や前提がすり合っているか確認する", "前提が未決のまま話を進め、決めたことが後で覆る"),
        ("8-2", "相手の反応から、真意を推し量る", "反応をその場の賛否として受け取り、どの判断基準が効いたかを確かめない"),
        ("8-3", "緩和策を添えて、浮上した案の\n弱みやリスクが許容できるか確認する", "許容できないリスクを説得可能と勘違いし、時間を浪費する"),
    ]),
    9: ("合意事項", [
        ("9-1", "決定を議事録に残す。重視した価値基準、受容した痛み、緩和策の3点をセットで", "議事録を残さず、決めたはずのことが次の回で覆る"),
        ("9-2", "影響の大きい決定は、会議体での最終承認まで通す", "現場で合意したまま進め、後から利害関係者に「知らなかった」と言われる"),
    ]),
}

NO_HEAD = set("、。，．）」』？！ー・ぁぃぅぇぉっゃゅょ〜")
NO_TAIL = set("（「『")


def char_w(c, size):
    return size * (0.56 if ord(c) < 0x2000 else 1.0)


def kind(c):
    if c in "、。，．": return "punct"
    if "\u3041" <= c <= "\u309f": return "hira"
    if "\u30a0" <= c <= "\u30ff": return "kata"
    if c.isascii() and c.isalnum(): return "ascii"
    if "\u4e00" <= c <= "\u9fff" or c in "々〜": return "kanji"
    return "other"


def break_cost(a, b):
    # 文節の切れ目らしい位置（句読点の後、ひらがなから漢字・カタカナへ移る所）で折る
    if b in NO_HEAD or a in NO_TAIL:
        return None
    ka, kb = kind(a), kind(b)
    if ka == "punct":
        return 0
    if a == " ":
        return 4
    if a in "」）』" or b in "「（『":
        return 1
    if ka == kb and ka in ("ascii", "kata"):
        return None
    if ka == "hira" and kb != "hira":
        return 2
    if ka == "kanji" and kb == "hira":
        return 10
    if ka != kb:
        return 6
    return {"hira": 12, "kanji": 14}.get(ka, 8)


def wrap(text, size, width):
    # 自動の折り返しで語が割れる箇所は、文言側に改行を書いて指定する
    if "\n" in text:
        return [l for part in text.split("\n") for l in wrap(part, size, width)]
    n = len(text)
    widths = [char_w(c, size) for c in text]
    best = [None] * (n + 1)
    best[0] = (0.0, -1)
    for i in range(1, n + 1):
        bc = 0 if i == n else break_cost(text[i - 1], text[i])
        if bc is None:
            continue
        for j in range(i - 1, -1, -1):
            if best[j] is None:
                continue
            line = text[j:i].strip()
            w = sum(widths[j:i])
            if w > width:
                break
            slack = (width - w) / size
            cost = best[j][0] + 100 + bc * 3 + (0 if i == n else slack * slack * 0.3)
            if len(line) <= 2:
                cost += 60
            if best[i] is None or cost < best[i][0]:
                best[i] = (cost, j)
    lines, i = [], n
    while i > 0:
        j = best[i][1]
        lines.append(text[j:i].strip())
        i = j
    return lines[::-1]


def svg(n_steps, output, steps):
    n = len(steps)
    # 手順が少ない図も、箱の幅は4手順の図に揃える。全幅に引き伸ばすと手続きごとに縮尺が変わって見えるため
    slots = max(n, 4)
    cw = (W - 2 * MARGIN - OUT_W - GAP * slots) / slots
    names = [wrap(name, 16, cw - 24) for _, name, _ in steps]
    trips = [wrap(trip, 14.5, cw - 32) for _, _, trip in steps]
    step_h = 72 + 24 * max(len(l) for l in names)
    trip_y = 16 + step_h + 34
    trip_h = 48 + 23 * max(len(l) for l in trips)
    H = int(trip_y + trip_h + 14)
    mid = 16 + step_h / 2

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Noto Sans CJK JP, sans-serif">',
         '  <defs>',
         '    <marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">',
         '      <path d="M0,0 L10,5 L0,10 z" fill="#2b5f83"/>',
         '    </marker>',
         '  </defs>',
         f'  <rect width="{W}" height="{H}" fill="#ffffff"/>']
    for i, ((num, _, _), nl, tl) in enumerate(zip(steps, names, trips)):
        x = MARGIN + i * (cw + GAP)
        cx = x + cw / 2
        o.append(f'  <rect x="{x:.1f}" y="16" width="{cw:.1f}" height="{step_h}" rx="10" fill="#e4eef5" stroke="#a6c6da" stroke-width="2"/>')
        bw = 48 if len(num) <= 3 else 58
        o.append(f'  <rect x="{cx - bw / 2:.1f}" y="28" width="{bw}" height="26" rx="13" fill="#2b5f83"/>')
        o.append(f'  <text x="{cx:.1f}" y="47" font-size="16" font-weight="700" fill="#ffffff" text-anchor="middle">{num}</text>')
        # 手順名は枠の下側の余白に中央寄せする
        y0 = 54 + (step_h - 38 - 24 * len(nl)) / 2 + 20
        for k, line in enumerate(nl):
            o.append(f'  <text x="{cx:.1f}" y="{y0 + 24 * k:.1f}" font-size="16" font-weight="700" fill="#1b2026" text-anchor="middle">{escape(line)}</text>')
        o.append(f'  <line x1="{x + cw + 2:.1f}" y1="{mid:.1f}" x2="{x + cw + GAP - 3:.1f}" y2="{mid:.1f}" stroke="#2b5f83" stroke-width="2.5" marker-end="url(#a)"/>')
        # 躓きが空の手順は、本書のスコープ外として箱ごと描かない
        if not tl:
            continue
        o.append(f'  <line x1="{cx:.1f}" y1="{16 + step_h}" x2="{cx:.1f}" y2="{trip_y}" stroke="#b5562a" stroke-width="1.5" stroke-dasharray="4 4"/>')
        o.append(f'  <rect x="{x:.1f}" y="{trip_y}" width="{cw:.1f}" height="{trip_h}" rx="8" fill="#fbf3ee" stroke="#e2c3b2" stroke-width="1.5"/>')
        o.append(f'  <text x="{x + 16:.1f}" y="{trip_y + 26}" font-size="14" font-weight="700" fill="#b5562a">躓き</text>')
        for k, line in enumerate(tl):
            o.append(f'  <text x="{x + 16:.1f}" y="{trip_y + 56 + 23 * k}" font-size="14.5" fill="#1b2026">{escape(line)}</text>')
    ox = MARGIN + n * (cw + GAP)
    o.append(f'  <rect x="{ox}" y="16" width="{OUT_W}" height="{step_h}" rx="10" fill="#2b5f83" stroke="#2b5f83" stroke-width="2"/>')
    o.append(f'  <text x="{ox + OUT_W / 2}" y="47" font-size="14" font-weight="700" fill="#ffffff" fill-opacity="0.8" text-anchor="middle">アウトプット</text>')
    ol = wrap(output, 16, OUT_W - 24)
    y0 = 54 + (step_h - 38 - 24 * len(ol)) / 2 + 20
    for k, line in enumerate(ol):
        o.append(f'  <text x="{ox + OUT_W / 2}" y="{y0 + 24 * k:.1f}" font-size="16" font-weight="700" fill="#ffffff" text-anchor="middle">{escape(line)}</text>')
    o.append('</svg>')
    return "\n".join(o) + "\n"


if __name__ == "__main__":
    here = Path(__file__).parents[1] / "images"
    for n, (output, steps) in STEPS.items():
        (here / f"procedure{n}_flow.svg").write_text(svg(n, output, steps), encoding="utf-8")
