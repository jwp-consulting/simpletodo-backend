// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2021-2024 JWP Consulting GK
import adapterStatic from "@sveltejs/adapter-static";
import adapterNode from "@sveltejs/adapter-node";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

const adapter =
    process.env.PROJECTIFY_FRONTEND_ADAPTER === "static"
        ? adapterStatic({
              fallback: "fallback.html",
              strict: true,
          })
        : process.env.PROJECTIFY_FRONTEND_ADAPTER === "node"
          ? adapterNode({
                envPrefix: "SVELTE_KIT_",
            })
          : undefined;

/** @type {import('@sveltejs/kit').Config} */
const config = {
    // Consult https://github.com/sveltejs/svelte-preprocess
    // for more information about preprocessors
    preprocess: [vitePreprocess()],
    kit: {
        alias: {
            "$messages": "src/messages",
            "$routes": "src/routes",
            "$lib-stories": "src/lib-stories",
        },
        adapter,
        csp: {
            directives: {
                // Mirrors root directory Caddyfile backend_headers,
                // with exception of making style-src more lenient
                // See https://github.com/sveltejs/kit/issues/11747 and
                // https://kit.svelte.dev/docs/configuration
                "default-src": ["self"],
                "style-src": ["self", "unsafe-inline"],
                "script-src": ["self"],
                "font-src": ["self"],
                "img-src": ["self", "blob:", "res.cloudinary.com"],
                "form-action": ["self"],
                // XXX we add this to ensure our cross-domain Netlify/Heroku
                // deployment keeps working
                "connect-src": [
                    "self",
                    "wss://api.projectifyapp.com",
                    "https://api.projectifyapp.com",
                ],
                "frame-ancestors": ["none"],
                "object-src": ["self"],
                "base-uri": ["self"],
            },
            // TODO add reports
        },
        typescript: {
            config(config) {
                return {
                    ...config,
                    include: [
                        ...config.include,
                        "../tailwind.config.ts",
                        "../knip.ts",
                    ],
                };
            },
        },
    },
};

// eslint-disable-next-line
export default config;
