// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { error } from "@sveltejs/kit";

import { clearSelectedWorkspaceUuidIfMatch } from "$lib/stores/dashboard/ui";
import type { WorkspaceDetail } from "$lib/types/workspace";

import type { LayoutLoadEvent } from "./$types";
import { currentWorkspace } from "$lib/stores/dashboard/workspace";

interface Data {
    workspace: WorkspaceDetail;
}

export async function load({
    params: { workspaceUuid },
}: LayoutLoadEvent): Promise<Data> {
    const workspace = await currentWorkspace.loadUuid(workspaceUuid);
    if (!workspace) {
        clearSelectedWorkspaceUuidIfMatch(workspaceUuid);
        error(404, `No workspace found for UUID '${workspaceUuid}'`);
    }
    return { workspace };
}

export const prerender = false;
