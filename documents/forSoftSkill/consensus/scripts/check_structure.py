#!/usr/bin/env python3
"""合意形成編の構造チェック。textlint で見られないものだけを見る。

見るもの: 手続き番号の実在、節あたりの太字の数、章番号のローマ数字、[要検討] の棚卸し。
サブステップ（N-k）の正は、流れ図の生成元 figures/gen_step_flow.py の STEPS とする。
本文は（N-k）を箇条書きの項目にしていて見出しを持たないため。

    python3 scripts/check_structure.py          # 全ページ
    python3 scripts/check_structure.py a.md ...  # 指定したページ
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "figures"))
from gen_step_flow import STEPS  # noqa: E402

HEAD = re.compile(r'^(#{2,4}) (.*)$')
STEP_REF = re.compile(r'手続き([0-9]+)(?:-([0-9]+))?')
LABEL_REF = re.compile(r'（([0-9]+)-([0-9]+)）')
BOLD = re.compile(r'\*\*([^*]+)\*\*')
# 箇条書きの行頭にある太字は項目ラベル。「:」が付かない形もある
LABEL = re.compile(r'^\s*(?:[-*]|[0-9]+\.) \*\*[^*]+\*\*')
ROMAN = re.compile(r'[ⅠⅡⅢⅣⅤⅥ]|\((?:I{1,3}|IV|V)\)')

PROCS = set(STEPS)
SUBS = {tuple(map(int, num.split('-'))) for _, steps in STEPS.values() for num, _, _ in steps}


def sections(lines):
    """見出しごとに (見出し, 開始行, 行のリスト) を返す。"""
    cur, buf, start = '(冒頭)', [], 1
    for i, ln in enumerate(lines, 1):
        m = HEAD.match(ln)
        if m:
            yield cur, start, buf
            cur, buf, start = m.group(2), [], i
        else:
            buf.append(ln)
    yield cur, start, buf


def check(path):
    lines = Path(path).read_text(encoding='utf-8').split('\n')
    problems, refs = [], set()

    for i, ln in enumerate(lines, 1):
        for m in STEP_REF.finditer(ln):
            n = int(m.group(1))
            if m.group(2) is None:
                if n not in PROCS:
                    problems.append((i, f'手続き{n} は定義されていない'))
            else:
                k = int(m.group(2))
                refs.add((n, k))
                if (n, k) not in SUBS:
                    problems.append((i, f'手続き{n}-{k} は定義されていない'))
        for m in LABEL_REF.finditer(ln):
            if (int(m.group(1)), int(m.group(2))) not in SUBS:
                problems.append((i, f'（{m.group(1)}-{m.group(2)}）は定義されていない'))
        if ROMAN.search(ln):
            problems.append((i, 'ローマ数字が使われている。章や層の番号は (1) (2) (3)'))

    # 節あたりの太字は1つまで。項目ラベル・引用・表のセル・手続きの参照は数えない
    for title, start, body in sections(lines):
        n = 0
        for ln in body:
            t = ln.lstrip()
            if LABEL.match(ln) or t.startswith('>') or t.startswith('|'):
                continue
            n += sum(1 for b in BOLD.findall(ln) if not b.startswith('手続き'))
        if n > 1:
            problems.append((start, f'「{title}」の太字が {n} 個。1節に1つまで'))

    todo = [(i, ln) for i, ln in enumerate(lines, 1) if '[要検討]' in ln]
    return problems, todo, refs


def main(paths):
    bad, refs = 0, set()
    for p in paths:
        problems, todo, r = check(p)
        refs |= r
        name = Path(p).name
        for line, msg in sorted(problems):
            print(f'{name}:{line}: {msg}')
        bad += len(problems)
        if todo:
            print(f'--- {name} の [要検討] {len(todo)} 件')
            for line, ln in todo:
                print(f'  {line}: {ln.strip().lstrip("> ")[:70]}')
    # 「手続きN-k」の形でどのページからも参照されていないサブステップ。指摘ではなく棚卸しの材料
    orphan = sorted(SUBS - refs)
    if orphan:
        print('--- 参照されていないサブステップ: ' + ', '.join(f'{a}-{b}' for a, b in orphan))
    print(f'\n{bad} problems')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:] or sorted(str(p) for p in HERE.glob('*.md') if p.name != 'CLAUDE.md')))
