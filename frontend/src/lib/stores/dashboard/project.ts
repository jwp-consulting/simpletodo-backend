// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { openApiClient } from "$lib/repository/util";
import type { ProjectDetail } from "$lib/types/workspace";

export async function getProject(
    project_uuid: string,
): Promise<ProjectDetail | undefined> {
    const { error, data } = await openApiClient.GET(
        "/workspace/project/{project_uuid}",
        { params: { path: { project_uuid } } },
    );
    if (error?.code === 500) {
        throw new Error("Unrecoverable server error");
    }
    return data;
}
