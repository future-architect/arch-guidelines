/**
 * X の言及の点のキャッシュ生成（#490）。
 *
 * X の件数 API は 2015 年に消えていて検索 API も有料なので、公式の数字は取れない。
 * 技術ブログ側が手元に保存した X の検索結果から言及ポストを集計しているので、
 * そこが書き出したページごとの点を取り込む（future-architect.github.io#2031）。
 * 点の重み（ポスト1・リポスト1・ブックマーク1/2・いいね1/4）はあちらが持つ。
 *
 * 共有ボタンを持つページの URL だけを残す。ページを改名するとあちらの表が古くなるが、
 * ここで交差させておけば消えた URL の数字がキャッシュに居残らない。
 *
 * 実行: npm run xcount
 */
import { writeFile } from "node:fs/promises";
import path from "node:path";
import { ROOT, listPageUrls } from "./page_urls.mjs";

const CACHE_FILE = path.join(ROOT, ".vitepress", "x_count_cache.json");
const SOURCE =
  "https://raw.githubusercontent.com/future-architect/future-architect.github.io/main/x_guideline_counts.json";

/**
 * @returns {Promise<Record<string, number>>} URL → 点
 */
async function fetchCounts() {
  const res = await fetch(SOURCE);
  if (!res.ok) {
    throw new Error(`X の点の取得に失敗しました: ${res.status}`);
  }
  return res.json();
}

const urls = await listPageUrls();
const source = await fetchCounts();
const counts = {};
// 0 のページは数字を出さないので持たない。キャッシュの差分が実際の増減だけになる
for (const url of urls) {
  if (source[url] > 0) counts[url] = source[url];
}
await writeFile(CACHE_FILE, `${JSON.stringify(counts, null, 2)}\n`, "utf8");

const stale = Object.keys(source).filter((url) => !urls.includes(url));
console.log(
  `X の点: ${urls.length} ページ中 ${Object.keys(counts).length} ページに1以上`,
);
// 向こうの表が古い（ページを改名した・共有ボタンを外した）ときに気づけるように出す
if (stale.length > 0) {
  console.log(
    `このサイトに無い URL が ${stale.length} 件:\n  ${stale.join("\n  ")}`,
  );
}
