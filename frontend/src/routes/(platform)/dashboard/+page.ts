// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { redirect } from "@sveltejs/kit";

import { currentWorkspaces } from "$lib/stores/dashboard/workspace";
import { getDashboardWorkspaceUrl } from "$lib/urls";
import { startUrl } from "$lib/urls/onboarding";

import { selectedWorkspaceUuid } from "$lib/stores/dashboard/ui";

export async function load(): Promise<void> {
    const maybeWorkspaceUuid: string | null = await new Promise(
        selectedWorkspaceUuid.subscribe,
    );
    if (maybeWorkspaceUuid) {
        redirect(302, getDashboardWorkspaceUrl({ uuid: maybeWorkspaceUuid }));
    }
    const workspaces = await currentWorkspaces.load();
    const workspace = workspaces[0];
    if (workspace === undefined) {
        redirect(302, startUrl);
    } else {
        redirect(302, getDashboardWorkspaceUrl(workspace));
    }
}
