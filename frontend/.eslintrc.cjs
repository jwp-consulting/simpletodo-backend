// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2021-2024 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
module.exports = {
    root: true,
    extends: [
        "eslint:recommended",
        "plugin:@typescript-eslint/strict-type-checked",
        "plugin:@typescript-eslint/stylistic-type-checked",
        "prettier",
        "plugin:import/recommended",
        "plugin:import/typescript",
        "plugin:svelte/recommended",
        "plugin:@typescript-eslint/recommended",
    ],
    plugins: [
        "@typescript-eslint",
        // "unused-imports",
        "import",
        "eslint-plugin-tsdoc",
    ],
    parser: "@typescript-eslint/parser",
    parserOptions: {
        project: ["./tsconfig.json"],
        sourceType: "module",
        ecmaVersion: 2020,
        extraFileExtensions: [".svelte"],
    },
    overrides: [
        {
            files: ["*.svelte"],
            parser: "svelte-eslint-parser",
            parserOptions: {
                parser: "@typescript-eslint/parser",
            },
            rules: {
                // This is unfortunately required because of export let
                // style svelte component prop declarations
                "@typescript-eslint/init-declarations": "off",
            },
        },
    ],
    ignorePatterns: [
        ".git",
        ".mypy_cache",
        "node_modules",
        ".storebook",
        ".svelte-kit",
        "*.stories.ts",
    ],
    settings: {
        "import/ignore": [
            // TODO revisit this at some point in the future
            // Justus 2023-09-06
            "dom-focus-lock/dist/index.esm.js",
            "@steeze-ui/heroicons.index.js",
            // fixes
            // `parseForESLint` from parser
            // `monorepo/frontend/node_modules/svelte-eslint-parser/lib/index.js`
            // is invalid and will just be ignored
            "marked-gfm-heading-id/src/index.js",
        ],
        "import/resolver": {
            typescript: {
                project: "./tsconfig.json",
                $lib: "src",
            },
        },
    },
    env: {
        browser: true,
        es2017: true,
        node: true,
    },
    rules: {
        "prefer-const": "error",
        // "unused-imports/no-unused-imports": "error",
        "import/no-unresolved": "off",
        "import/first": "error",
        "import/newline-after-import": "error",
        "import/no-cycle": "error",
        "import/no-relative-packages": "error",
        // Reenable once https://github.com/import-js/eslint-plugin-import/issues/1479 is fixed.
        "import/no-duplicates": "off",
        // Since we use typescript, we have declarations for __BUILD_DATE__
        // and others, so we don't need to check for plain JS undefined
        // variables.
        "no-undef": "off",
        // https://stackoverflow.com/a//64150393
        "no-unused-vars": "off",
        // TODO Remove me
        "@typescript-eslint/prefer-optional-chain": "off",
        // TODO Remove me
        "@typescript-eslint/no-confusing-void-expression": "off",
        // TODO Remove me
        "@typescript-eslint/no-redundant-type-constituents": "off",
        // TODO find a way to apply me to svelte as well
        // While ignoring export lets.
        // This is useful because reactive code might refer to
        // HTMLElements that are undefined? Is this true? Can
        // reactive code blocks be run before a svelte component is
        // mounted?
        // Justus 2023-08-17
        "@typescript-eslint/init-declarations": ["error", "always"],
        "@typescript-eslint/indent": "off",
        "@typescript-eslint/switch-exhaustiveness-check": "error",
        "@typescript-eslint/no-unused-vars": [
            "error",
            {
                argsIgnorePattern: "_.*",
                varsIgnorePattern: "_.*",
            },
        ],
        "@typescript-eslint/no-misused-promises": [
            "error",
            {
                checksVoidReturn: {
                    arguments: false,
                    returns: false,
                    variables: false,
                },
            },
        ],
    },
};
