// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { error } from "@sveltejs/kit";

import type { WorkspaceDetail, ProjectDetail } from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";
import { currentProject } from "$lib/stores/dashboard/project";
import { currentWorkspace } from "$lib/stores/dashboard/workspace";

export async function load({
    params: { workspaceUuid },
}: PageLoadEvent): Promise<{
    workspace: WorkspaceDetail;
    project?: ProjectDetail;
}> {
    const workspace = await currentWorkspace.loadUuid(workspaceUuid);
    if (!workspace) {
        error(404, `No workspace could be found for UUID '${workspaceUuid}'`);
    }
    const projectUuid = workspace.projects.at(0)?.uuid;
    const project = projectUuid
        ? await currentProject.loadUuid(projectUuid)
        : undefined;
    return { workspace, project };
}
