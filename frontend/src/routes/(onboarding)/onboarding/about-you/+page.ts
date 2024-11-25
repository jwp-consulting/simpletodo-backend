// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
import type { PageLoadEvent } from "./$types";

export async function load({ parent }: PageLoadEvent) {
    const { user } = await parent();
    return { user };
}
