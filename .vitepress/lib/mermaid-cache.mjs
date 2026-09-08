/**
 * mermaid 図の SVG キャッシュ（#406）の共通定義。
 *
 * 生成側（mermaid_svg.mjs）と展開側（markdown-it-plugin-mermaid-svg.mjs）で
 * キーの取り方がズレるとキャッシュが空振りして全図がクライアント描画に落ちるため、
 * ハッシュと置き場所はここに集約する。
 */
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const CACHE_DIR = fileURLToPath(new URL("../mermaid/", import.meta.url));

/**
 * 生成側は正規表現、展開側は markdown-it のトークンから図のソースを取るので、
 * 改行の種類と前後の空行をそろえてから比べる
 * @param {string} source 図のソース
 * @returns {string} 正規化したソース
 */
export function normalizeSource(source) {
  return source.replace(/\r\n?/gu, "\n").trim();
}

/**
 * @param {string} source 図のソース
 * @returns {string} SVG キャッシュのキー。図を編集したときだけ再生成される
 */
export function hashOf(source) {
  return createHash("sha256")
    .update(normalizeSource(source), "utf8")
    .digest("hex");
}

/**
 * @param {string} hash キャッシュのキー
 * @returns {string} SVG ファイルのパス
 */
export function svgPath(hash) {
  return path.join(CACHE_DIR, `${hash}.svg`);
}

/**
 * @param {string} hash キャッシュのキー
 * @returns {string | null} 生成済みの SVG。無ければ null
 */
export function readSvg(hash) {
  const file = svgPath(hash);
  return existsSync(file) ? readFileSync(file, "utf8").trim() : null;
}
