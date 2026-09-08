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
import { readFile, readdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const SOURCES = [path.join(ROOT, "index.md"), path.join(ROOT, "documents")];
const CACHE_FILE = path.join(ROOT, ".vitepress", "hatebu_count_cache.json");
const ENDPOINT = "https://bookmark.hatenaapis.com/count/entries";
// まとめ取得は1リクエスト50 URL まで
const CHUNK = 50;

/**
 * @param {string} target ファイルかディレクトリ
 * @returns {Promise<string[]>} 配下の Markdown ファイル
 */
async function listMarkdown(target) {
  if (target.endsWith(".md")) return [target];
  const entries = await readdir(target, {
    withFileTypes: true,
    recursive: true,
  });
  return entries
    .filter((e) => e.isFile() && e.name.endsWith(".md"))
    .map((e) => path.join(e.parentPath, e.name));
}

/**
 * 数字を出すのは共有ボタンを持つページだけなので、そのページの URL に絞る。
 * 公開 URL の組み立ては package.json の homepage を正とする。
 *
 * @returns {Promise<string[]>} 公開 URL
 */
async function listPageUrls() {
  const pkg = JSON.parse(
    await readFile(path.join(ROOT, "package.json"), "utf8"),
  );
  const files = (await Promise.all(SOURCES.map(listMarkdown))).flat();
  const urls = [];
  for (const file of files) {
    const content = await readFile(file, "utf8");
    if (!content.includes("<page-title")) continue;
    const rel = path.relative(ROOT, file).split(path.sep).join("/");
    // ディレクトリの index はスラッシュ止まり、それ以外は .html（VitePress の既定）
    const route = rel.endsWith("index.md")
      ? rel.slice(0, -"index.md".length)
      : rel.replace(/\.md$/u, ".html");
    urls.push(new URL(route, pkg.homepage).toString());
  }
  return urls.sort();
}

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
