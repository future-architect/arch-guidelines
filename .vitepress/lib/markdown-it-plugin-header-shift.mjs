// @ts-check
/**
 * @typedef {import('markdown-it/lib/rules_core/state_core.mjs').default} StateCore
 * @typedef {import('markdown-it').default} MarkdownIt
 */
/**
 * headerタグを1つづつずらします。
 * Pandocでも利用できるMarkdownファイルにしたいので、`# header`を一つしかつくれないvitepress制約がうまく共存できないため、
 * vitepressではhタグの番号をずらし、無理やり共存できるようにします。
 * @param {MarkdownIt} md
 */
export default function headerSections(md) {
  /**
   *
   * @param {InstanceType<md['core']['State']>} state
   * @returns
   */
  function shiftHeaders(state) {
    if (
      !state.tokens.some(
        (token) =>
          token.type === "html_inline" &&
          token.content.startsWith("<page-title"),
      )
    ) {
      // <page-title>がない場合は何もしない
      return;
    }

    state.tokens.forEach((t, i) => {
      if (t.type.includes("heading")) {
        t.tag = t.tag.replace(/^h(\d)$/, (_h, n) => `h${n - 0 + 1}`);
      }
    });
  }

  md.core.ruler.push("header_shift", shiftHeaders);
}
