// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
import { redirect } from "@sveltejs/kit";
import type { LayoutLoadEvent } from "./$types";
import { dashboardUrl } from "$lib/urls/dashboard";
import { currentUser } from "$lib/stores/user";

interface Data {
    redirectTo: string | undefined;
}

export async function load({ url }: LayoutLoadEvent): Promise<Data> {
    // TODO might want to default to dashboardUrl here with redirectTo
    const redirectTo = url.searchParams.get("next") ?? undefined;
    const user = await currentUser.load();
    if (user.kind === "authenticated") {
        redirect(302, redirectTo ?? dashboardUrl);
    }
    return { redirectTo };
}

export const prerender = false;
