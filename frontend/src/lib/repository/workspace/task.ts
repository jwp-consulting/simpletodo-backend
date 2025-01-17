// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { invalidateGettableUrl, openApiClient } from "$lib/repository/util";
import type { components } from "$lib/types/schema";
import type {
    Task,
    TaskDetailSection,
    ProjectDetailSection,
    ProjectDetailTask,
} from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

// Task CRUD
// Create

export async function createTask(body: components["schemas"]["TaskCreate"]) {
    return await openApiClient.POST("/workspace/task/", { body });
}

// Update
// TODO change me to accept CreateOrUpdateTaskData directly
// Then we don't have to pass task, labels, ws user separately
// This is possible now because the API accepts a whole task object,
// incl. labels and so on
export async function updateTask(
    { uuid: task_uuid }: Pick<Task, "uuid">,
    body: components["schemas"]["TaskUpdate"],
) {
    const params = { path: { task_uuid } };
    const response = await openApiClient.PUT("/workspace/task/{task_uuid}", {
        params,
        body,
    });
    await invalidateGettableUrl("/workspace/task/{task_uuid}", params);
    return response;
}

type TaskPosition =
    | { kind: "top"; position: 0; isOnly: boolean }
    | { kind: "within"; position: number; isOnly: false }
    | { kind: "bottom"; position: number; isOnly: false }
    | { kind: "outside"; isOnly: undefined };

function getTaskPosition(
    section: ProjectDetailSection,
    task: Pick<Task, "uuid">,
): TaskPosition {
    const { tasks } = section;
    const taskIndex = tasks.findIndex((t) => t.uuid == task.uuid);
    const lastIndex = tasks.length - 1;
    switch (taskIndex) {
        case -1:
            return { kind: "outside", isOnly: undefined };
        case 0:
            return { kind: "top", position: 0, isOnly: tasks.length === 1 };
        case lastIndex:
            return { kind: "bottom", position: lastIndex, isOnly: false };
        default:
            return { kind: "within", position: taskIndex, isOnly: false };
    }
}

async function moveTaskAfterTask(
    task: Pick<Task, "uuid">,
    { uuid }: Pick<Task, "uuid">,
) {
    return await openApiClient.POST(
        "/workspace/task/{task_uuid}/move-after-task",
        {
            params: { path: { task_uuid: task.uuid } },
            body: { task_uuid: uuid },
        },
    );
}

async function moveToBottom(
    section: ProjectDetailSection,
    task: Pick<Task, "uuid">,
) {
    const { tasks } = section;
    const lastTask = tasks[tasks.length - 1];
    if (lastTask === undefined) {
        throw new Error("Expected lastTask");
    }
    return await moveTaskAfterTask(task, lastTask);
}

async function moveUp(
    section: ProjectDetailSection,
    task: Pick<ProjectDetailTask, "uuid">,
) {
    const { tasks } = section;
    const position = getTaskPosition(section, task);
    if (!(position.kind === "within" || position.kind === "bottom")) {
        throw new Error("Expected task to be within or at bottom");
    }
    const prevTask = unwrap(
        tasks.at(position.position - 1),
        "Expected prevTask",
    );
    return await moveTaskAfterTask(task, prevTask);
}

async function moveDown(
    section: ProjectDetailSection,
    task: Pick<ProjectDetailTask, "uuid">,
) {
    const position = getTaskPosition(section, task);
    if (!(position.kind === "top" || position.kind === "within")) {
        throw new Error("Expected task to be at top or within");
    }
    const tasks = unwrap(section.tasks, "Expected tasks");
    const nextTask = unwrap(
        tasks.at(position.position + 1),
        "Expected nextTask",
    );
    return await moveTaskAfterTask(task, nextTask);
}

async function moveTaskToSection(
    { uuid }: Pick<TaskDetailSection, "uuid">,
    task: Pick<Task, "uuid">,
) {
    return await openApiClient.POST(
        "/workspace/task/{task_uuid}/move-to-section",
        {
            params: { path: { task_uuid: task.uuid } },
            body: { section_uuid: uuid },
        },
    );
}

type MoveTaskWhere =
    | { kind: "top"; section: ProjectDetailSection }
    | { kind: "up"; section: ProjectDetailSection }
    | { kind: "down"; section: ProjectDetailSection }
    | { kind: "bottom"; section: ProjectDetailSection }
    | { kind: "section"; section: ProjectDetailSection };

export function canMoveTask(
    task: Pick<Task, "uuid">,
    { kind, section }: MoveTaskWhere,
) {
    if (kind === "section") {
        return true;
    }
    const pos = getTaskPosition(section, task);
    if (pos.isOnly) {
        return false;
    }
    switch (kind) {
        case "top":
        case "up":
            return pos.kind !== "top";
        case "down":
        case "bottom":
            return pos.kind !== "bottom";
    }
}

export async function moveTask(
    task: Pick<Task, "uuid">,
    { kind, section }: MoveTaskWhere,
) {
    switch (kind) {
        case "top":
            return await moveTaskToSection(section, task);
        case "up":
            return await moveUp(section, task);
        case "down":
            return await moveDown(section, task);
        case "bottom":
            return await moveToBottom(section, task);
        case "section":
            return await moveTaskToSection(section, task);
    }
}
