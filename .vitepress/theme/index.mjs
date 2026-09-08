import { defineAsyncComponent } from "vue";
import DefaultTheme from "vitepress/theme";
import "./style.css";
import "./mermaid.css";
import PageInfo from "./components/PageInfo.vue";
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

    ctx.app.component("PageInfo", PageInfo);
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
