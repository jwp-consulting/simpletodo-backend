// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import type { ProjectDetail } from "$lib/types/workspace";

import type { LayoutLoadEvent } from "./$types";

import { getProject } from "$lib/stores/dashboard/project";
import { error } from "@sveltejs/kit";
import { currentWorkspace } from "$lib/stores/dashboard/workspace";

interface Data {
    project: ProjectDetail;
}

export async function load({
    params: { projectUuid },
}: LayoutLoadEvent): Promise<Data> {
    const project: ProjectDetail | undefined = await getProject(projectUuid);
    if (project === undefined) {
        error(404, `No project could be found for UUID '${projectUuid}'`);
    }
    await currentWorkspace.loadUuid(project.workspace.uuid);
    return { project };
}

export const prerender = false;
