// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import "$lib/stores/globalUi";

import "$lib/i18n";

import { overrideClient } from "$lib/repository/util";
import type { LayoutLoadEvent } from "./$types";
import { currentUser } from "$lib/stores/user";

export async function load({ fetch }: LayoutLoadEvent) {
    overrideClient(fetch);
    const user = await currentUser.load();
    return { user };
}

export const prerender = true;
export const ssr = true;
