// @ts-check
/**
 * @typedef {import('markdown-it').default} MarkdownIt
 */

/**
 * コードフェンスのファイル名を出す (#473)。
 *
 * VitePress は情報行の `[title]` を **::: code-group の中でしか使わない**
 * （extractTitle を呼ぶのは createCodeGroup だけ）。単独のフェンスでは
 * extractLang が空白以降を捨てるので、`sh .gitattributes` も
 * `json [example.json]` もファイル名が表示されないまま落ちる。
 *
 * 技術ブログの記法（言語の後ろに空白でファイル名）と、VitePress 素の
 * `[title]` の両方を読む。code-group の中はタブが名乗るので触らない。
 */

/** 情報行のうち、ファイル名ではなく VitePress の指定を表す形 */
const META = /^[{:=]|^twoslash\b|^vue\b/u;

/**
 * 情報行からファイル名を取り出す。
 *
 * @param {string} info フェンスの情報行
 * @returns {string} ファイル名。無ければ空文字
 */
function extractTitle(info) {
  const bracketed = info.match(/\[(.*)\]/u);
  if (bracketed) return bracketed[1].trim();
  // preWrapperPlugin が付ける ` active`（code-group の1枚目）を落としてから見る
  const rest = info
    .replace(/\[.*\]/u, "")
    .replace(/\s+active$/u, "")
    .trim();
  const spaced = rest.match(/^\S+\s+(.+)$/u);
  if (!spaced) return "";
  const title = spaced[1].trim();
  return META.test(title) ? "" : title;
}

/**
 * このフェンスが ::: code-group の中にあるか。
 *
 * @param {import('markdown-it/index.mjs').Token[]} tokens
 * @param {number} idx
 * @returns {boolean}
 */
function inCodeGroup(tokens, idx) {
  for (let i = idx - 1; i >= 0; i--) {
    if (tokens[i].type === "container_code-group_close") return false;
    if (tokens[i].type === "container_code-group_open") return true;
  }
  return false;
}

/**
 * @param {MarkdownIt} md
 */
export default function fenceTitle(md) {
  const fence = md.renderer.rules.fence;
  if (!fence) return;
  md.renderer.rules.fence = (...args) => {
    const [tokens, idx] = args;
    const title = extractTitle(tokens[idx].info);
    const html = fence(...args);
    if (!title || inCodeGroup(tokens, idx)) return html;
    const label = `<span class="fence-title">${md.utils.escapeHtml(title)}</span>`;
    // preWrapperPlugin が返す <div class="language-…"> の直後に差し込む
    return html.replace(/^(<div class="language-[^"]*">)/u, `$1${label}`);
  };
}
