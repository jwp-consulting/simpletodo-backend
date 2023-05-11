import Fuse from "fuse.js";
import lodash from "lodash";
import { get, derived, writable } from "svelte/store";
import type { Readable } from "svelte/store";
import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";

import { currentWorkspaceBoardUuid } from "$lib/stores/dashboard/workspaceBoard";
import { selectWorkspaceUser } from "$lib/stores/dashboard/workspaceUser";

import { selectedLabels } from "$lib/stores/dashboard/label";
import { fuseSearchThreshold } from "$lib/config";
import { getTask } from "$lib/repository/workspace";
import { browser } from "$app/environment";
import type { WSSubscriptionStore } from "$lib/stores/wsSubscription";
import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";

export const taskSearchInput = writable<string>("");
export const currentTaskUuid = writable<string | null>(null);

let currentTaskSubscription: WSSubscriptionStore | null = null;
let currentTaskSubscriptionUnsubscribe: (() => void) | null = null;

// Clear on workspace board change
currentWorkspaceBoardUuid.subscribe((_uuid) => {
    selectedLabels.set({ kind: "allLabels" });
    selectWorkspaceUser({ kind: "allWorkspaceUsers" });
    taskSearchInput.set("");
});

type CurrentSearchedTasks = Readable<Task[] | null>;

export function createCurrentSearchedTasks(
    currentWorkspaceBoardSections: Readable<WorkspaceBoardSection[]>,
    taskSearchInput: Readable<string>
): CurrentSearchedTasks {
    return derived<
        [typeof currentWorkspaceBoardSections, typeof taskSearchInput],
        Task[] | null
    >(
        [currentWorkspaceBoardSections, taskSearchInput],
        ([$currentWorkspaceBoardSections, $taskSearchInput], set) => {
            if ($taskSearchInput == "") {
                set(null);
            } else {
                set(
                    searchTasks(
                        $currentWorkspaceBoardSections,
                        $taskSearchInput
                    )
                );
            }
        },
        null
    );
}

export function searchTasks(
    sections: WorkspaceBoardSection[],
    searchText: string
): Task[] {
    const tasks: Task[] = lodash.flatten(
        sections.map((section) => (section.tasks ? section.tasks : []))
    );

    const searchEngine: Fuse<Task> = new Fuse(tasks, {
        keys: ["title"],
        threshold: fuseSearchThreshold,
    });

    return searchEngine
        .search(searchText)
        .map((res: Fuse.FuseResult<Task>) => res.item);
}

export const currentTask = derived<[typeof currentTaskUuid], Task | null>(
    [currentTaskUuid],
    ([$currentTaskUuid], set) => {
        if (!browser) {
            set(null);
            return;
        }
        if (!$currentTaskUuid) {
            set(null);
            return;
        }
        set(null);
        getTask($currentTaskUuid)
            .then((task) => set(task))
            .catch((error: Error) => {
                console.error(
                    "An error happened when refetching $currentTask",
                    { error }
                );
            });
        if (currentTaskSubscriptionUnsubscribe) {
            currentTaskSubscriptionUnsubscribe();
        }
        currentTaskSubscription = getSubscriptionForCollection(
            "task",
            $currentTaskUuid
        );
        if (!currentTaskSubscription) {
            throw new Error("Expected currentWorkspaceBoardSubscription");
        }
        currentTaskSubscriptionUnsubscribe = currentTaskSubscription.subscribe(
            async (_value) => {
                console.log("Refetching task", $currentTaskUuid);
                set(await getTask($currentTaskUuid));
            }
        );
    },
    null
);

// XXX Remove the following
import { goto } from "$app/navigation";
import { getDashboardTaskUrl, getDashboardWorkspaceBoardUrl } from "$lib/urls";

export const drawerModalOpen = writable(false);
export const newTaskSectionUuid = writable<string | null>(null);

export function openNewTask(sectionUuid: string): void {
    drawerModalOpen.set(true);
    newTaskSectionUuid.set(sectionUuid);
    currentTaskUuid.set(null);
}
export async function openTaskDetails(
    workspaceBoardUuid: string,
    taskUuid: string,
    subView = "details"
) {
    drawerModalOpen.set(true);
    currentTaskUuid.set(taskUuid);
    await goto(getDashboardTaskUrl(workspaceBoardUuid, taskUuid, subView));
}
export async function closeTaskDetails() {
    drawerModalOpen.set(false);
    currentTaskUuid.set(null);
    const boardUuid = get(currentWorkspaceBoardUuid);
    if (!boardUuid) {
        throw new Error("Expected boardUuid");
    }
    await goto(getDashboardWorkspaceBoardUrl(boardUuid));
}
