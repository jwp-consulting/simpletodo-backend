// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2021-2024 JWP Consulting GK
/// <reference types="@sveltejs/kit" />
declare const __GIT_COMMIT_DATE__: string;
declare const __GIT_BRANCH_NAME__: string;
declare const __GIT_COMMIT_HASH__: string;
declare const __BUILD_DATE__: string;

declare const __MODE__: string;

declare const __API_ENDPOINT__: string;
declare const __API_ENDPOINT_REWRITE_TO__: string;
declare const __WS_ENDPOINT__: string;

// Automatically generated third-party-licenses module as part of vite
// build process
declare module "third-party-licenses" {
    export = string;
}

// Used for @sveltejs/enhanced-img, images have to be loaded by appending
// ?enhanced
declare module "*.png?enhanced" {
    const value: string;
    export = value;
}

// https://www.npmjs.com/package/@poppanator/sveltekit-svg#typescript
// Copied from the packages dist/svg.d.ts file
declare module "*.svg?url" {
    const content: string;
    export default content;
}

declare module "favicon-html" {
    const content: string;
    export default content;
}
