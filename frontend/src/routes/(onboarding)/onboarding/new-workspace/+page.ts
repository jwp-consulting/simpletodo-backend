// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
import type { CurrentUser } from "$lib/types/user";
import type { UserWorkspace } from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";
import { currentWorkspaces } from "$lib/stores/dashboard/workspace";

export async function load({ parent }: PageLoadEvent): Promise<{
    user: CurrentUser & { kind: "authenticated" };
    workspace?: UserWorkspace;
}> {
    const { user } = await parent();
    const workspaces = await currentWorkspaces.load();
    const workspace = workspaces.at(0);
    return { user, workspace };
}
