// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
import type { LayoutLoadEvent } from "./$types";

export async function load({ parent }: LayoutLoadEvent) {
    const { user } = await parent();
    return { user };
}

export const prerender = false;
