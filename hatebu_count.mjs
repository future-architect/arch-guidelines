/**
 * はてなブックマークの件数キャッシュ生成（#425）。
 *
 * 共有ボタン（`<page-title/>`）を持つページの URL を集め、件数を
 * .vitepress/hatebu_count_cache.json に書き出す。ページ側はこの JSON を
 * import してビルド時に数字を焼き込む。
 *
 * 件数 API は CORS ヘッダを持たないのでブラウザからは叩けず、ビルド時に
 * 取るしかない。ビルド自体を外部に依存させないため、取得はここで済ませて
 * 結果をコミットする（日次ワークフロー hatebu-count.yml が回す）。
 *
 * 実行: npm run hatebu
 */
import { writeFile } from "node:fs/promises";
import path from "node:path";
import { ROOT, listPageUrls } from "./page_urls.mjs";

const CACHE_FILE = path.join(ROOT, ".vitepress", "hatebu_count_cache.json");
const ENDPOINT = "https://bookmark.hatenaapis.com/count/entries";
// まとめ取得は1リクエスト50 URL まで
const CHUNK = 50;

/**
 * @param {string[]} urls 公開 URL
 * @returns {Promise<Record<string, number>>} URL → 件数（0 は含めない）
 */
async function fetchCounts(urls) {
  const counts = {};
  for (let i = 0; i < urls.length; i += CHUNK) {
    const query = new URLSearchParams();
    for (const url of urls.slice(i, i + CHUNK)) query.append("url", url);
    const res = await fetch(`${ENDPOINT}?${query}`);
    if (!res.ok) {
      throw new Error(`はてブ件数の取得に失敗しました: ${res.status}`);
    }
    // 0 のページは数字を出さないので持たない。キャッシュの差分が実際の増減だけになる
    for (const [url, count] of Object.entries(await res.json())) {
      if (count > 0) counts[url] = count;
    }
  }
  // 並びはコードポイント順で固定する。localeCompare は環境で結果が変わるため
  return Object.fromEntries(
    Object.entries(counts).sort(([a], [b]) => (a < b ? -1 : 1)),
  );
}

const urls = await listPageUrls();
const counts = await fetchCounts(urls);
await writeFile(CACHE_FILE, `${JSON.stringify(counts, null, 2)}\n`, "utf8");
console.log(
  `はてブ件数: ${urls.length} ページ中 ${Object.keys(counts).length} ページに1件以上`,
);
