// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import type { KnipConfig } from "knip";

const config: KnipConfig = {
    ignore: [
        "**/*.d.ts",
        // Temporary fix until stories have been migrated
        "src/lib-stories/storybook.ts",
        "src/routes/stories/**/*.{stories.ts,ts,svelte}",
    ],
    entry: [
        "postcss.config.cjs",
        "bin/check-i18n",
        "src/bin/check-i18n.ts",
        "src/hooks.server.ts",
    ],
    /* Extensions looked up by running the following in fish:
     * for file in (find src -type f)
     * path extension "$file"
     * end | sort | uniq
     */
    project: ["static/**/*.png", "src/**/*.{css,html,scss,svg,png,ts,svelte}"],
    rules: {
        binaries: "error",
        dependencies: "error",
        devDependencies: "error",
        exports: "error",
        files: "error",
        nsExports: "error",
        types: "error",
        unlisted: "error",
        // False positive for *.html?raw
        unresolved: "off",
    },
    paths: {
        // This ain't pretty, but Svelte basically does the same
        "$app/*": ["node_modules/@sveltejs/kit/src/runtime/app/*"],
        "$env/*": [".svelte-kit/ambient.d.ts"],
    },
    ignoreBinaries: ["open", "bin/test", "bin/update-schema"],
    ignoreDependencies: [
        "esm-loader-import-alias",
        "openapi-typescript",
        "esm-loader-import-relative-extension",
        "esm-loader-typescript",
        "node-esm-loader",
        // Synthetic import created as part of vite build
        "third-party-licenses",
        "favicon-html",
    ],
    compilers: {
        // https://github.com/webpro/knip/blob/7011a5107b6693f70a966a12bc3c31b6bc3353a8/docs/compilers.md
        svelte: (text: string) =>
            [...text.matchAll(/import[^;]+/g)].join("\n"),
        scss: (text: string) =>
            [...text.matchAll(/(?<=@)import[^;]+/g)].join("\n"),
    },
};

export default config;
