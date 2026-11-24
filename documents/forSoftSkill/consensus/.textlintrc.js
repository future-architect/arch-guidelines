// 合意形成編の文章検査。リポジトリ共通の設定に、本書で決めた書き方と用語の辞書を重ねる。
// 共通の .textlintrc に足すと、ほかのガイドラインにも本書の用語ルールがかかるため分けている。
const { readFileSync } = require("node:fs");
const { join } = require("node:path");

const root = join(__dirname, "../../..");
const base = JSON.parse(readFileSync(join(root, ".textlintrc"), "utf8"));

module.exports = {
  ...base,
  filters: {
    ...base.filters,
    allowlist: {
      allow: [
        ...base.filters.allowlist.allow,
        "/[◎○△×]{2,}/",
        // 相手に意見を求める問いの引用。書き手自身の「〜と思う」は弱い表現として拾いたいので、問いの形だけを許す
        "/どう思[いうわ]/",
        "/と思うか/",
        "/と思う[？?]/",
        "/[よどな]い?と思う/",
        "/かもしれない/",
        "/^:::.*$/m",
        // 長音の辞書は「ドライバ」に揃えるが、本書は図も本文も長音ありで統一している
        "ドライバー",
      ],
    },
  },
  rules: {
    ...base.rules,
    "preset-ja-technical-writing": {
      ...base.rules["preset-ja-technical-writing"],
      // 箇条書きの項目の末尾に「。」を付けない
      "ja-no-mixed-period": false,
      // 相手への問いを「ですます」で引用する。本文は「である」
      "no-mix-dearu-desumasu": false,
      // トレードオフを「Aだが、B」で書くため、1文に複数出る
      "no-doubled-conjunctive-particle-ga": false,
      // 表と箇条書きが多く、誤検知が本物を埋める
      "no-doubled-joshi": false,
      "max-ten": false,
      "arabic-kanji-numbers": false,
      "sentence-length": false,
      "max-comma": false,
      "max-kanji-continuous-len": false,
    },
    prh: {
      rulePaths: [join(root, "prh-choon.yml"), join(__dirname, "prh.yml")],
    },
  },
};
