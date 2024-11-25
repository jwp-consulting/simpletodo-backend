// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import type { TaskDetail } from "$lib/types/workspace";
import { error } from "@sveltejs/kit";

import type { LayoutLoadEvent } from "./$types";
import { openApiClient } from "$lib/repository/util";

interface Data {
    task: TaskDetail;
}

export async function load({
    params: { taskUuid },
}: LayoutLoadEvent): Promise<Data> {
    const { data: task } = await openApiClient.GET(
        "/workspace/task/{task_uuid}",
        { params: { path: { task_uuid: taskUuid } } },
    );
    if (!task) {
        error(404, `No task could be found for UUID '${taskUuid}'`);
    }
    currentWorkspace
        .loadUuid(task.section.project.workspace.uuid)
        .catch((error: unknown) =>
            console.error(
                "Error when fetching currentWorkspace for task ${taskUuid}",
                error,
            ),
        );
    return { task };
}
export const prerender = false;
