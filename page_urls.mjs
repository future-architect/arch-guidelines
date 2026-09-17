/**
 * 共有ボタンを持つページの公開 URL を集める。
 *
 * はてブ（#425）と X（#490）の2つの件数キャッシュが同じ URL をキーにする。
 * 組み立ての規則が割れると、片方のキャッシュだけ数字が引けなくなるのでここに置く。
 */
import { readFile, readdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const SOURCES = [path.join(ROOT, "index.md"), path.join(ROOT, "documents")];

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
export async function listPageUrls() {
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

export { ROOT };
