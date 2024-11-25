<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<script lang="ts">
    import DashboardPlaceholder from "$lib/components/onboarding/DashboardPlaceholder.svelte";
    import type { State } from "$lib/components/onboarding/DashboardPlaceholder.svelte";
    import type {
        ProjectDetail,
        ProjectDetailSection,
        ProjectDetailWorkspace,
        TaskDetail,
    } from "$lib/types/workspace";

    const workspace = {
        uuid: "workspace-uuid",
        title: "Workspace",
    } as ProjectDetailWorkspace;
    const project = {
        uuid: "project-uuid",
        title: "Project",
    } as ProjectDetail;
    const section = {
        uuid: "section-uuid",
        title: "Section",
        _order: 0,
        tasks: [],
    } as ProjectDetailSection;
    const task = { uuid: "task-uuid", title: "Task" } as TaskDetail;
    const label = { uuid: "label-uuid", name: "Label", color: 0 };
    const assignee = {
        uuid: "assignee-uuid" as const,
        user: { email: "", preferred_name: null, profile_picture: null },
        role: "CONTRIBUTOR" as const,
        job_title: null,
    };

    type Kind = State["kind"];
    let stateKind: Kind = "new-workspace";

    const user = {
        email: "asd",
        kind: "authenticated" as const,
        preferred_name: "asd",
        profile_picture: null,
    };

    // https://stackoverflow.com/questions/56981452/typescript-union-type-to-single-mapped-type/56981568#56981568
    type StateSelector<
        K extends State["kind"],
        U extends { kind: State["kind"] },
    > = U extends { kind: K } ? U : never;
    const states: { [K in State["kind"]]: StateSelector<K, State> } = {
        "new-workspace": {
            kind: "new-workspace",
            title: "New workspace",
        },
        "new-project": {
            kind: "new-project",
            workspace,
            title: "New project",
        },
        "new-task": {
            kind: "new-task",
            workspace,
            project,
            sectionTitle: "Section",
            title: "New task",
        },
        "new-label": {
            kind: "new-label",
            workspace,
            project,
            section,
            task,
            title: "New label",
        },
        "assign-task": {
            kind: "assign-task",
            workspace,
            project,
            section,
            task,
            label,
            assignee,
        },
    } as const;

    let state: State = {
        kind: "new-workspace",
        title: "Hello world",
    };

    function updateState() {
        /*
        XXX why eslint?
/Users/justusperlwitz/projects/projectify/monorepo/frontend/src/routes/stories/components/Onboarding/DashboardPlaceholder/+page.svelte
  98:15  error  Unsafe assignment of an `any` value            @typescript-eslint/no-unsafe-assignment
  99:9   error  Unsafe assignment of an `any` value            @typescript-eslint/no-unsafe-assignment
  99:24  error  Computed name [kind] resolves to an any value  @typescript-eslint/no-unsafe-member-access
        */
        // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
        const kind: Kind = stateKind;
        // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
        state = states[kind];
    }
</script>

<div class="flex flex-row">
    <h1>Dashboard Placeholder Demo</h1>

    <div class="flex flex-col">
        <label>
            State Kind:
            <select bind:value={stateKind} on:change={updateState}>
                <option value="new-workspace">New Workspace</option>
                <option value="new-project">New Project</option>
                <option value="new-task">New Task</option>
                <option value="new-label">New Label</option>
                <option value="assign-task">Assign Task</option>
            </select>
        </label>
    </div>

    <DashboardPlaceholder {user} {state} />
</div>
