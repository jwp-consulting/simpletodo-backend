// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
// TODO it seems like we could bundle all these [taskUuid] dependent onboarding
// pages like so:
// onboarding/task/[taskUuid]/new-label/
import { error } from "@sveltejs/kit";

import type {
    ProjectDetailWorkspace,
    ProjectDetail,
    ProjectDetailSection,
    TaskDetail,
} from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";
import { openApiClient } from "$lib/repository/util";
import { currentProject } from "$lib/stores/dashboard/project";

interface returnType {
    task: TaskDetail;
    section: ProjectDetailSection;
    project: ProjectDetail;
    workspace: ProjectDetailWorkspace;
}

export async function load({
    params: { taskUuid },
}: PageLoadEvent): Promise<returnType> {
    const { error: e, data: task } = await openApiClient.GET(
        "/workspace/task/{task_uuid}",
        { params: { path: { task_uuid: taskUuid } } },
    );
    if (e) {
        error(404, `No task could found for UUID ${taskUuid}.`);
    }
    const {
        section: {
            uuid: sectionUuid,
            project: { uuid: projectUuid },
        },
    } = task;
    const project = await currentProject.loadUuid(projectUuid);
    if (!project) {
        throw new Error("Expected project");
    }
    const section = project.sections.find((s) => s.uuid == sectionUuid);
    if (!section) {
        throw new Error("Expected section");
    }
    const { workspace } = project;
    return { task, section, project, workspace };
}
