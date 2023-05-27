// XXX "stores.ts" should be renamed "modules.ts" maybe?
import type { Readable, Writable } from "svelte/store";

import type {
    LabelSelection,
    LabelSelectionInput,
    TasksPerUser,
    WorkspaceUserSelection,
    WorkspaceUserSelectionInput,
} from "$lib/types/ui";
import type {
    CreateTask,
    CreateWorkspaceBoardSection,
    Label,
    NewTask,
    Task,
    Workspace,
    WorkspaceBoard,
    WorkspaceBoardSection,
    WorkspaceUser,
} from "$lib/types/workspace";

// It would make sense to rename all Module to Store

// XXX I took the liberty of adding workspace board creation into here
// Not sure if that is good Justus 2023-05-01
export interface WorkspaceBoardSearchModule {
    // TODO for a consistent API we would have workspace boards as
    // searchResults here
    currentWorkspaceBoardUuid: Readable<string | null>;
    currentWorkspaceBoard: Readable<WorkspaceBoard | null>;
    currentWorkspace: Readable<Workspace | null>;
}

export interface WorkspaceUserSearchModule {
    select: (selection: WorkspaceUserSelectionInput) => void;
    deselect: (selection: WorkspaceUserSelectionInput) => void;
    selected: Readable<WorkspaceUserSelection>;
    tasksPerUser: Readable<TasksPerUser>;
    search: Writable<string>;
    searchResults: Readable<WorkspaceUser[]>;
}

export interface LabelSearchModule {
    select: (selection: LabelSelectionInput) => void;
    deselect: (selection: LabelSelectionInput) => void;
    selected: Readable<LabelSelection>;
    // TODO make readonly
    search: Writable<string>;
    searchResults: Readable<Label[]>;
    createLabel: (color: number, name: string) => Promise<void>;
}

export interface WorkspaceBoardSectionModule {
    switchWithPrevSection?: () => Promise<void>;
    switchWithNextSection?: () => Promise<void>;
}

export interface NewWorkspaceBoardSectionModule {
    createWorkspaceBoardSection: (
        workspaceBoard: WorkspaceBoard,
        workspaceBoardSection: CreateWorkspaceBoardSection
    ) => void;
}

// XXX
// This is a mess!
// this contains whatever is shared between creating / updating tasks
export interface CreateOrUpdateTaskModule {
    canCreateOrUpdate: Readable<boolean>;
    createOrUpdateTask: () => void;
    workspaceUserSearchModule: WorkspaceUserSearchModule;
    labelSearchModule: LabelSearchModule;
}

export type TaskModule = {
    task: Task;
    updateTask: Writable<Partial<Task>>;
    showUpdateWorkspaceUser: (anchor: HTMLElement) => void;
    showUpdateLabel: (anchor: HTMLElement) => void;
} & CreateOrUpdateTaskModule;

export type CreateTaskModule = {
    newTask: NewTask;
    createTask: Writable<Partial<CreateTask>>;
} & CreateOrUpdateTaskModule;

// Functions needed to move task around inside section or between sections
export interface MoveTaskModule {
    moveToBottom?: () => Promise<void>;
    moveToTop?: () => Promise<void>;
    moveToWorkspaceBoardSection: (
        workspaceBoardSection: WorkspaceBoardSection
    ) => Promise<void>;
}

export const subscriptionTypes = [
    "workspace",
    "workspace-board",
    "task",
] as const;
export type SubscriptionType = (typeof subscriptionTypes)[number];
