// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { openApiClient } from "$lib/repository/util";
import { createHttpStore } from "$lib/stores/httpSubscription";
import { createWsStore } from "$lib/stores/wsSubscription";
import type { UserWorkspace, WorkspaceDetail } from "$lib/types/workspace";

async function getWorkspace(
    workspace_uuid: string,
): Promise<WorkspaceDetail | undefined> {
    const { error, data } = await openApiClient.GET(
        "/workspace/workspace/{workspace_uuid}",
        {
            params: { path: { workspace_uuid } },
        },
    );
    if (error?.code === 404) {
        return undefined;
    }
    if (error) {
        throw new Error(
            `Error when retrieving workspace ${workspace_uuid} ${JSON.stringify(
                error,
            )}`,
        );
    }
    return data;
}

async function getWorkspaces(): Promise<UserWorkspace[]> {
    const { error, data } = await openApiClient.GET(
        "/workspace/workspace/user-workspaces/",
    );
    if (error?.code === 500) {
        console.error("Could not retrieve workspaces, retrying");
        throw new Error();
    }
    if (data) {
        return data;
    }
    throw new Error(`Could not retrieve workspaces ${JSON.stringify(error)}`);
}

export const currentWorkspace = createWsStore("workspace", getWorkspace);

export const currentWorkspaces = createHttpStore(getWorkspaces);
