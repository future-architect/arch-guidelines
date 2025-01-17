import path from "node:path";
import { fileURLToPath } from "node:url";
import js from "@eslint/js";
import { FlatCompat } from "@eslint/eslintrc";
import pluginVue from "eslint-plugin-vue";
import eslintConfigPrettier from "eslint-config-prettier";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
  allConfig: js.configs.all,
});

export default [
  {
    ignores: ["node_modules/", "docs/", ".vitepress/cache/"],
  },
  ...compat.extends("standard"),
  ...pluginVue.configs["flat/recommended"],
  {
    rules: {
      "no-var": "error",
      "prefer-const": "error",
    },
  },
  eslintConfigPrettier,
];
