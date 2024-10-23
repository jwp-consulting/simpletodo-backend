// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { openApiClient } from "$lib/repository/util";
import { selectedLabels } from "$lib/stores/dashboard/labelFilter";
import { currentProject } from "$lib/stores/dashboard/project";
import { filterByTeamMember } from "$lib/stores/dashboard/teamMemberFilter";
import { searchAmong } from "$lib/stores/util";
import { createWsStore } from "$lib/stores/wsSubscription";
import type { SearchInput } from "$lib/types/base";
import type {
    // XXX only use TaskWithWorkspace
    TaskWithSection,
    TaskDetail,
    ProjectDetailSection,
} from "$lib/types/workspace";

// Clear on project change
// TODO clarify if this subscription still makes sense
// It's good to unsubscribe whenever we can
// Justus 2023-08-30
currentProject.subscribe((_$currentProject) => {
    selectedLabels.set({ kind: "allLabels" });
    filterByTeamMember({ kind: "allTeamMembers" });
});

export function searchTasks(
    sections: readonly ProjectDetailSection[],
    searchText: SearchInput,
): readonly TaskWithSection[] {
    type Task = ProjectDetailSection["tasks"][number];
    const sectionTasks = sections.map((section) =>
        section.tasks.map((task: Task) => {
            return { ...task, section };
        }),
    );
    const tasks = sectionTasks.flat();
    return searchAmong<TaskWithSection>(
        ["section.title", "title", "number"],
        tasks,
        searchText,
    );
}

export const currentTask = createWsStore<TaskDetail>(
    "task",
    async (task_uuid: string) => {
        const { data, error } = await openApiClient.GET(
            "/workspace/task/{task_uuid}",
            { params: { path: { task_uuid } } },
        );
        if (error?.code === 500) {
            throw new Error("Server error 500");
        }
        if (data) {
            return data;
        }
        return undefined;
    },
);
