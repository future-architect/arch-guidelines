// @ts-check
import fs from "node:fs";
import path from "node:path";
import { imageSize } from "image-size";

/**
 * @typedef {import('markdown-it').default} MarkdownIt
 */

/**
 * 画像に実寸の width / height と、2枚目以降の loading="lazy" を付ける (#474)。
 *
 * 原稿は `![alt](images/xxx.png)` の記法なので、markdown-it の出力は
 * `<img src alt>` だけになる。幅が確定するまで高さ 0 で置かれ、読み込まれた
 * 瞬間に本文が下へ動く（CLS）。技術ブログは寸法を原稿に焼き込む運用だが
 * （#2605）、こちらは原稿を素の Markdown に保ちたいのでビルド時に付ける。
 *
 * lazy は 2 枚目以降だけに付ける（技術ブログ #2645）。先頭の画像は LCP の
 * 候補になりやすく、lazy が付いていると表示が遅れる。
 * markdown.image.lazyLoading は全画像に付けるので使わない。
 */

/** 寸法を読まない src（外部・データ URI・アンカー） */
const EXTERNAL = /^(?:[a-z][a-z0-9+.-]*:|\/\/|#)/iu;

/** @type {Map<string, {width: number, height: number} | null>} */
const cache = new Map();

/**
 * SVG の寸法を <svg> の属性から読む。
 *
 * image-size は SVG を先頭の <svg で見分けるので、draw.io が書き出す
 * XML 宣言と DOCTYPE で始まるファイル（6 枚）を読めない。
 * width / height が無いものは viewBox の 3・4 番目を使う。
 *
 * 全体を文字列にしてから探す。draw.io は <svg> の開きタグに style を
 * 丸ごと書くので、タグ 1 つが 17KB になることがある（先頭だけ切って
 * 探すと閉じ > に届かない）。
 *
 * @param {Buffer} buf
 * @returns {{width: number, height: number} | null}
 */
function svgSize(buf) {
  const tag = buf.toString("utf8").match(/<svg\b[^>]*>/iu)?.[0];
  if (!tag) return null;
  const attr = (name) =>
    Number.parseFloat(
      tag.match(new RegExp(`\\b${name}="([^"]+)"`, "iu"))?.[1] ?? "",
    );
  const width = attr("width");
  const height = attr("height");
  if (width > 0 && height > 0) return { width, height };
  const box = tag
    .match(/\bviewBox="([^"]+)"/iu)?.[1]
    ?.trim()
    .split(/[\s,]+/u);
  if (box?.length === 4) {
    const [w, h] = [Number.parseFloat(box[2]), Number.parseFloat(box[3])];
    if (w > 0 && h > 0) return { width: w, height: h };
  }
  return null;
}

/**
 * 画像ファイルの実寸を読む。読めなければ null。
 *
 * @param {string} file 絶対パス
 * @returns {{width: number, height: number} | null}
 */
function sizeOf(file) {
  if (cache.has(file)) return cache.get(file) ?? null;
  /** @type {{width: number, height: number} | null} */
  let size = null;
  try {
    const buf = fs.readFileSync(file);
    try {
      const { width, height } = imageSize(buf);
      if (width && height) size = { width, height };
    } catch {
      size = null;
    }
    if (!size && file.toLowerCase().endsWith(".svg")) size = svgSize(buf);
  } catch {
    size = null;
  }
  if (size)
    size = { width: Math.round(size.width), height: Math.round(size.height) };
  cache.set(file, size);
  return size;
}

/**
 * @param {MarkdownIt} md
 * @param {{ srcDir: string }} options srcDir はルート相対の src を解決する起点
 */
export default function imageSizePlugin(md, options) {
  const image = md.renderer.rules.image;
  if (!image) return;
  md.renderer.rules.image = (...args) => {
    const [tokens, idx, , env] = args;
    const token = tokens[idx];
    const src = token.attrGet("src") ?? "";

    // ページごとに何枚目かを数える。env は 1 ページの描画で 1 つ
    const seen = (env.__imageCount ?? 0) + 1;
    env.__imageCount = seen;

    if (!EXTERNAL.test(src) && !token.attrGet("width")) {
      const base = env.path ? path.dirname(env.path) : options.srcDir;
      // 日本語のファイル名は src がパーセント符号化されている
      let rel = src;
      try {
        rel = decodeURIComponent(src);
      } catch {
        rel = src;
      }
      const file = rel.startsWith("/")
        ? path.join(options.srcDir, rel)
        : path.resolve(base, rel);
      const size = sizeOf(file);
      if (size) {
        token.attrSet("width", String(size.width));
        token.attrSet("height", String(size.height));
      }
    }
    // 先頭の画像には付けない
    if (seen > 1 && !token.attrGet("loading")) token.attrSet("loading", "lazy");

    return image(...args);
  };
}
