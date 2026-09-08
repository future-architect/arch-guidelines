import DefaultTheme from "vitepress/theme";
import "./style.css";
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
  },
};
