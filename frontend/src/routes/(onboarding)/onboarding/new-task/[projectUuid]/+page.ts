// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { error } from "@sveltejs/kit";

import type { ProjectDetail, WorkspaceDetail } from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";
import { currentProject } from "$lib/stores/dashboard/project";
import { currentWorkspace } from "$lib/stores/dashboard/workspace";

export async function load({
    params: { projectUuid },
}: PageLoadEvent): Promise<{
    project: ProjectDetail;
    workspace: WorkspaceDetail;
    section?: ProjectDetail["sections"][number];
}> {
    const project = await currentProject.loadUuid(projectUuid);
    if (!project) {
        error(404, `No project could be found for UUID ${projectUuid}.`);
    }
    const { uuid: workspaceUuid } = project.workspace;
    const workspace = await currentWorkspace.loadUuid(workspaceUuid);
    if (!workspace) {
        // If this happens something is very wrong
        error(
            500,
            `No workspace with UUID ${workspaceUuid} could be found for project UUID ${projectUuid}.`,
        );
    }
    const section = project.sections.at(0);
    return { project, workspace, section };
}
