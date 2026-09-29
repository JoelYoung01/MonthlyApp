/* eslint-env node */
require("@rushstack/eslint-patch/modern-module-resolution");

module.exports = {
  root: true,
  extends: [
    "plugin:vue/vue3-recommended",
    "eslint:recommended",
    "@vue/eslint-config-typescript",
    "@vue/eslint-config-prettier/skip-formatting"
  ],
  parserOptions: {
    ecmaVersion: "latest"
  },
  rules: {
    "prettier/prettier": "warn"
  },
  overrides: [
    {
      files: ["src/components/ui/**/*.{vue,ts}"],
      rules: {
        "vue/multi-word-component-names": "off",
        "vue/require-default-prop": "off"
      }
    }
  ]
};
