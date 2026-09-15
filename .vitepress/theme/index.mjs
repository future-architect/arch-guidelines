import { defineAsyncComponent } from "vue";
// Web フォント（Inter）を読まない入口 (#465)。変わるのは欧文と数字の字形だけで、
// 和文は元から system-ui に落ちていた
import DefaultTheme from "vitepress/theme-without-fonts";
import "./style.css";
import "./mermaid.css";
import PageTitle from "./components/PageTitle.vue";
import FutureStar from "./components/FutureStar.vue";

/**
 * @typedef {import('vitepress').EnhanceAppContext} EnhanceAppContext
 */
export default {
  ...DefaultTheme,
  /**
   * @param {EnhanceAppContext} ctx context
   * @returns {void}
   */
  enhanceApp: (ctx) => {
    DefaultTheme.enhanceApp(ctx);

    ctx.app.component("PageTitle", PageTitle);
    ctx.app.component("FutureStar", FutureStar);
    // SVG キャッシュの無い図だけがクライアント描画に落ちる。mermaid.js はそのときだけ読む
    ctx.app.component(
      "Mermaid",
      defineAsyncComponent(
        () => import("vitepress-plugin-mermaid/Mermaid.vue"),
      ),
    );
  },
};
