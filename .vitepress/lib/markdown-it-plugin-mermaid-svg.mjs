import { hashOf, readSvg } from "./mermaid-cache.mjs";

const warned = new Set();

/**
 * kroki の SVG を Vue のテンプレートに埋め込める形にする。
 *
 * - <style> はテンプレートコンパイラが副作用のあるタグとして捨てる
 *   （compiler-dom の ignoreSideEffectTags）。<component is="style"> にすると
 *   実行時に本物の <style> 要素として描かれ、SVG の中に置いたままにできる。
 *   v-pre は <component> も素の要素にしてしまうので使えず、代わりに
 *   ラベルの本文に現れうる {{ だけを実体参照で逃がす
 * - 図の本体は静的な文字列（createStaticVNode）に畳まれる必要がある。
 *   VitePress はその文字列を lean チャンクから削るので、畳まれないと
 *   SVG 1枚ぶんの描画コードがページの JS に丸ごと乗る（実測で 33KB → 536KB）。
 *   Vue は既知の属性しか畳まないので、svg 要素の role と、foreignObject の中の
 *   div が持つ xmlns を落とす（インライン SVG ではどちらも無くても解釈は変わらない）
 * @param {string} svg kroki が生成した SVG
 * @returns {string} Vue のテンプレートに埋め込める形
 */
function toTemplateHtml(svg) {
  return svg
    .replace(/<svg\b[^>]*>/u, (tag) => tag.replace(/\srole="[^"]*"/u, ""))
    .replaceAll(' xmlns="http://www.w3.org/1999/xhtml"', "")
    .replace(/<style\b[^>]*>/gu, '<component is="style">')
    .replace(/<\/style>/gu, "</component>")
    .replaceAll("{{", "{&#123;");
}

/**
 * ```mermaid フェンスのうち、`npm run mermaid` が SVG を生成済みのものを
 * インライン SVG に置き換える。無い図は元の fence ルール
 * （vitepress-plugin-mermaid のクライアント描画）に渡す
 * @param {import("markdown-it")} md markdown-it
 * @returns {void}
 */
export default function markdownItMermaidSvg(md) {
  const fallback = md.renderer.rules.fence;
  md.renderer.rules.fence = (tokens, idx, options, env, self) => {
    const token = tokens[idx];
    if (token.info.trim() !== "mermaid") {
      return fallback(tokens, idx, options, env, self);
    }
    const hash = hashOf(token.content);
    const svg = readSvg(hash);
    if (svg === null) {
      // 未生成でもブラウザで描かれて気づけないので、ここで知らせる
      if (!warned.has(hash)) {
        warned.add(hash);
        console.warn(
          `mermaid: ${env.relativePath ?? ""} に SVG キャッシュ未生成の図があります（${hash.slice(0, 12)}）。` +
            "`npm run mermaid` を実行してコミットしてください（それまではブラウザ描画で表示されます）",
        );
      }
      return fallback(tokens, idx, options, env, self);
    }
    return `<div class="mermaid-svg" data-mermaid="${hash}">${toTemplateHtml(svg)}</div>\n`;
  };
}
