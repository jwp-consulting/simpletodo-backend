// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { redirect } from "@sveltejs/kit";

import { currentWorkspaces } from "$lib/stores/dashboard/workspace";
import { getLogInWithNextUrl } from "$lib/urls/user";

import type { LayoutLoadEvent } from "./$types";
import type { CurrentUser } from "$lib/types/user";

export async function load({ parent, url }: LayoutLoadEvent): Promise<{
    user: CurrentUser & { kind: "authenticated" };
}> {
    await currentWorkspaces.load();
    const { user } = await parent();
    if (user.kind === "unauthenticated") {
        const next = getLogInWithNextUrl(url.pathname);
        console.log("Not logged in, redirecting to", next);
        redirect(302, next);
    }
    return { user };
}

export const ssr = true;
export const prerender = false;
