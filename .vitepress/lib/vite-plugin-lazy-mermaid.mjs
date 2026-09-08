/**
 * vitepress-plugin-mermaid はアプリの入口に Mermaid.vue を静的 import で差し込む
 * （MermaidPlugin の transform）。Mermaid.vue は mermaid 本体を静的に import するので、
 * 図の無いページでも mermaid.js（約 600KB）が app チャンクに入り、図の種類ごとの
 * チャンクも modulepreload される。
 *
 * ここでは差し込まれた import と登録を取り除き、登録は theme/index.mjs が
 * defineAsyncComponent で行う。app の dynamicImports は VitePress が全ページで
 * preload するので、遅延 import は theme 側に置く必要がある。
 * キャッシュの無い図（クライアント描画へのフォールバック）があるページだけが
 * mermaid.js を取りに行く。
 * @returns {import("vite").Plugin} プラグイン
 */
export default function lazyMermaid() {
  const injectedImport =
    "import Mermaid from 'vitepress-plugin-mermaid/Mermaid.vue';";
  const injectedRegister = 'app.component("Mermaid", Mermaid);';
  return {
    name: "vite-plugin-lazy-mermaid",
    enforce: "post",
    transform(code, id) {
      if (!id.includes("vitepress/dist/client/app/index.js")) return undefined;
      if (!code.includes(injectedImport)) return undefined;
      return {
        code: code.replace(injectedImport, "").replace(injectedRegister, ""),
        map: null,
      };
    },
  };
}
