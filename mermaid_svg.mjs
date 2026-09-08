/**
 * mermaid 図の SVG キャッシュ生成（#406）。ローカル専用で、CI では実行しない。
 *
 * index.md と documents 配下の ```mermaid フェンスを集め、ソースの SHA-256 をキーに
 * .vitepress/mermaid/<hash>.svg として保存する。生成済みはスキップし、
 * 参照されなくなった SVG は削除する。
 *
 * レンダラはセルフホストの kroki（mermaid_svg.compose.yml）。未起動なら
 * docker compose で自動起動する。生成後も起動したままにする（停止は
 * `docker compose -f mermaid_svg.compose.yml down`）。
 *
 * 実行: npm run mermaid
 */
import { execFileSync } from "node:child_process";
import { mkdir, readFile, readdir, unlink, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  CACHE_DIR,
  hashOf,
  normalizeSource,
  svgPath,
} from "./.vitepress/lib/mermaid-cache.mjs";

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const SOURCES = [path.join(ROOT, "index.md"), path.join(ROOT, "documents")];
const COMPOSE_FILE = path.join(ROOT, "mermaid_svg.compose.yml");
const KROKI_URL = process.env.KROKI_URL || "http://127.0.0.1:8007";
const CONCURRENCY = 4;

// 展開側（markdown-it）は info が mermaid のフェンスだけを見る。ここも同じ条件にそろえる
const FENCE_PATTERN = /^(`{3,})mermaid[ \t]*\n([\s\S]*?)\n\1[ \t]*$/gmu;

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
 * @returns {Promise<Map<string, {source: string, files: string[]}>>} hash → 図
 */
async function collectDiagrams() {
  const diagrams = new Map();
  const files = (await Promise.all(SOURCES.map(listMarkdown))).flat();
  for (const file of files) {
    const content = await readFile(file, "utf8");
    for (const m of content.matchAll(FENCE_PATTERN)) {
      const source = normalizeSource(m[2]);
      const hash = hashOf(source);
      const entry = diagrams.get(hash) || { source, files: [] };
      entry.files.push(path.relative(ROOT, file));
      diagrams.set(hash, entry);
    }
  }
  return diagrams;
}

/**
 * @returns {Promise<boolean>} kroki が応答するか
 */
async function krokiIsUp() {
  try {
    const res = await fetch(`${KROKI_URL}/health`, {
      signal: AbortSignal.timeout(3000),
    });
    return res.ok;
  } catch {
    return false;
  }
}

/**
 * @returns {Promise<void>}
 */
async function ensureKroki() {
  if (await krokiIsUp()) return;
  console.log(
    `kroki (${KROKI_URL}) が未起動のため docker compose で起動します`,
  );
  execFileSync("docker", ["compose", "-f", COMPOSE_FILE, "up", "-d"], {
    stdio: "inherit",
  });
  for (let i = 0; i < 60; i++) {
    await new Promise((resolve) => setTimeout(resolve, 2000));
    if (await krokiIsUp()) return;
  }
  throw new Error(
    `kroki が ${KROKI_URL} で起動しない。docker compose -f ${COMPOSE_FILE} logs を確認`,
  );
}

/**
 * kroki は毎回 id="container" で返す。<style> やマーカー参照が id でスコープされるので、
 * 同一ページに複数の図を並べると互いのスタイルを汚染する。図ごとに一意にする
 * @param {string} svg kroki の出力
 * @param {string} hash 図のキー
 * @returns {string} id を付け替えた SVG
 */
function uniquifyIds(svg, hash) {
  const m = svg.match(/<svg\b[^>]*?\sid="([^"]+)"/u);
  if (!m) return svg;
  const oldId = m[1];
  const newId = `mermaid-${hash.slice(0, 12)}`;
  if (oldId === newId) return svg;
  // ラベル本文に同じ文字列が現れても壊さないよう、id の参照形に限定して置換する
  return svg
    .replaceAll(`id="${oldId}`, `id="${newId}`)
    .replaceAll(`#${oldId}`, `#${newId}`);
}

/**
 * @param {string} hash 図のキー
 * @param {{source: string, files: string[]}} entry 図
 * @returns {Promise<string>} SVG
 */
async function render(hash, entry) {
  let lastError;
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const res = await fetch(`${KROKI_URL}/mermaid/svg`, {
        method: "POST",
        headers: { "Content-Type": "text/plain" },
        body: entry.source,
        signal: AbortSignal.timeout(60000),
      });
      const body = await res.text();
      if (!res.ok) {
        // 図のソース起因（構文エラー等）はリトライしても無駄
        throw Object.assign(
          new Error(`HTTP ${res.status}: ${body.slice(0, 300)}`),
          { fatal: res.status < 500 },
        );
      }
      return uniquifyIds(body.trim(), hash);
    } catch (e) {
      lastError = e;
      if (e.fatal) break;
      await new Promise((resolve) => setTimeout(resolve, 1000 * (attempt + 1)));
    }
  }
  throw new Error(
    `${entry.files.join(", ")} の図 (${hash.slice(0, 12)}) の生成に失敗: ${lastError.message}`,
  );
}

/**
 * @template T
 * @param {T[]} items 入力
 * @param {number} limit 同時実行数
 * @param {(item: T) => Promise<void>} fn 処理
 * @returns {Promise<{error?: Error}[]>} 結果
 */
async function mapLimit(items, limit, fn) {
  const results = [];
  let index = 0;
  await Promise.all(
    Array.from({ length: Math.min(limit, items.length) }, async () => {
      while (index < items.length) {
        const i = index++;
        results[i] = await fn(items[i]).then(
          () => ({}),
          (error) => ({ error }),
        );
      }
    }),
  );
  return results;
}

const diagrams = await collectDiagrams();
await mkdir(CACHE_DIR, { recursive: true });
const cached = new Set(
  (await readdir(CACHE_DIR))
    .filter((f) => f.endsWith(".svg"))
    .map((f) => path.basename(f, ".svg")),
);

const missing = [...diagrams.keys()].filter((hash) => !cached.has(hash));
const orphans = [...cached].filter((hash) => !diagrams.has(hash));
console.log(
  `図 ${diagrams.size} 件 / 生成済み ${diagrams.size - missing.length} 件 / 未生成 ${missing.length} 件 / 不要 ${orphans.length} 件`,
);

if (missing.length > 0) {
  await ensureKroki();
}

const results = await mapLimit(missing, CONCURRENCY, async (hash) => {
  const svg = await render(hash, diagrams.get(hash));
  await writeFile(svgPath(hash), svg + "\n");
  console.log(`生成: ${hash.slice(0, 12)} (${diagrams.get(hash).files[0]})`);
});
const failed = results.filter((r) => r.error);
for (const r of failed) console.error(r.error.message);

for (const hash of orphans) {
  await unlink(svgPath(hash));
  console.log(`削除: ${hash.slice(0, 12)}（参照するページが無い）`);
}

if (failed.length > 0) {
  console.error(
    `${failed.length} 件の生成に失敗（失敗した図はブラウザ描画のフォールバックで表示される）`,
  );
  process.exitCode = 1;
}
