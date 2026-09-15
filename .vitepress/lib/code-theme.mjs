import { bundledThemes } from "shiki";

/**
 * コードブロックの配色 (#466)。
 *
 * shiki 既定の github-light / github-dark をそのまま置くと、地の上で WCAG AA
 * （4.5）を割るトークンが出る。既製のテーマを載せ替えるのではなく、
 * **色相だけ借りて明度を振る**（技術ブログ #3266 と同じ方針）。
 *
 * 余裕は 4.6 で取る。AA の 4.5 ちょうどでは取らない。
 * 相手にする地は、明るい側が注記の中のコードブロックを含めた 5 つのうち
 * いちばん厳しいもの（danger の #ffeded）、暗い側は #161618 の 1 つ。
 *
 * 置き換えるのは色だけで、スコープ（どの字がどの役か）は触らない。
 */

/** 明るい側。github-light の 10 色のうち 4 色が danger の地で 3.09〜4.26 と AA を割る。 */
const LIGHT_OVERRIDES = {
  // comment（4.26 → 4.64）
  "#6a737d": "#656d77",
  // entity.name.tag / markup.inserted（4.10 → 4.65）
  "#22863a": "#207c36",
  // keyword / storage（4.05 → 4.63）
  "#d73a49": "#ce2a3a",
  // variable / markup.changed（3.09 → 4.61）
  "#e36209": "#b44e07",
};

/**
 * 暗い側。AA を割るのは comment（3.75）だけ。色相 212°・彩度 8% を保ったまま
 * 明度を上げて 4.62 にする。
 *
 * markup.ignored / markup.untracked / carriage-return（#2f363d / #24292e）も
 * 地との差が 1.2〜1.5 しか無いが、これは「無視された行」をわざと地に沈めるための
 * 色で、読ませる対象ではない。原稿に diff のコードフェンスは 1 つも無い。
 */
const DARK_OVERRIDES = {
  "#6a737d": "#78828c",
};

/**
 * テーマの色を置き換えた複製を返す。tokenColors の foreground と、
 * editor 側の colors の両方を舐める（同じ色が両方に出る）。
 *
 * @param {object} theme shiki の bundled theme
 * @param {Record<string, string>} overrides 置き換え表（小文字の16進数）
 * @returns {object} 置き換え済みのテーマ
 */
function override(theme, overrides) {
  const swap = (v) =>
    typeof v === "string" ? (overrides[v.toLowerCase()] ?? v) : v;
  return {
    ...theme,
    colors: Object.fromEntries(
      Object.entries(theme.colors ?? {}).map(([k, v]) => [k, swap(v)]),
    ),
    tokenColors: (theme.tokenColors ?? []).map((t) => ({
      ...t,
      settings: t.settings
        ? { ...t.settings, foreground: swap(t.settings.foreground) }
        : t.settings,
    })),
  };
}

export const codeThemeLight = override(
  (await bundledThemes["github-light"]()).default,
  LIGHT_OVERRIDES,
);

export const codeThemeDark = override(
  (await bundledThemes["github-dark"]()).default,
  DARK_OVERRIDES,
);
