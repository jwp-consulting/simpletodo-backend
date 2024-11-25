<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023, 2024 JWP Consulting GK -->
<script lang="ts" context="module">
    // TODO factor into an types/onboarding.ts type so that we can test this
    // in storybook
    export type State =
        | {
              kind: "new-workspace";
              workspace?: UserWorkspace;
              title: string;
          }
        | {
              kind: "new-project";
              workspace: ProjectDetailWorkspace;
              project?: ProjectDetail;
              title: string;
          }
        | {
              kind: "new-task";
              workspace: ProjectDetailWorkspace;
              project: ProjectDetail;
              sectionTitle: string;
              title: string;
          }
        | {
              kind: "new-label";
              workspace: ProjectDetailWorkspace;
              project: ProjectDetail;
              section: ProjectDetailSection;
              task: TaskDetail;
              title: string;
          }
        | {
              kind: "assign-task";
              workspace: ProjectDetailWorkspace;
              project: ProjectDetail;
              section: ProjectDetailSection;
              task: TaskDetail;
              label: Label;
              assignee: TaskDetailAssignee;
          };
</script>

<script lang="ts">
    import { onMount } from "svelte";
    import { _ } from "svelte-i18n";

    import {
        projectExpandOpen,
        labelExpandOpen,
        toggleProjectExpandOpen,
        toggleLabelDropdownClosedNavOpen,
        toggleUserExpandOpen,
        userExpandOpen,
    } from "$lib/stores/dashboard/ui";
    import type {
        Label,
        ProjectDetail,
        WorkspaceDetail,
        WorkspaceQuota,
        ProjectDetailSection,
        ProjectDetailTask,
        TaskDetail,
        TaskDetailAssignee,
        ProjectDetailWorkspace,
        UserWorkspace,
    } from "$lib/types/workspace";
    import Dashboard from "$routes/(platform)/dashboard/project/[projectUuid]/+page.svelte";
    import WorkspaceSelector from "$lib/figma/navigation/side-nav/WorkspaceSelector.svelte";
    import Projects from "$lib/figma/navigation/side-nav/Projects.svelte";
    import type { CurrentUser } from "$lib/types/user";

    // We are cheating a bit here
    const quota: WorkspaceQuota = {
        workspace_status: "trial",
    } as WorkspaceQuota;
    const workspaceFallback: WorkspaceDetail = {
        uuid: "does-not-exist",
        title: "",
        description: null,
        picture: null,
        projects: [],
        labels: [],
        team_members: [],
        team_member_invites: [],
        quota,
    };
    const projectFallback: ProjectDetail = {
        uuid: "does-not-exist",
        title: $_("onboarding.new-project.default-name"),
        description: "",
        sections: [],
        archived: null,
        workspace: workspaceFallback,
    };
    const sectionFallback: ProjectDetailSection = {
        title: "",
        uuid: "",
        _order: 0,
        tasks: [],
    };
    const taskFallback: ProjectDetailTask = {
        title: "",
        description: null,
        assignee: null,
        uuid: "",
        due_date: null,
        sub_task_progress: null,
        number: 1,
        labels: [],
    };
    const labelFallback: Label = {
        name: "",
        color: 0,
        uuid: "does-not-exist",
    };

    onMount(() => {
        // Ensure we have all side panels open
        if (!$projectExpandOpen) {
            toggleProjectExpandOpen();
        }
        if (!$labelExpandOpen) {
            toggleLabelDropdownClosedNavOpen();
        }
        if (!$userExpandOpen) {
            toggleUserExpandOpen();
        }
    });

    export let user: CurrentUser & { kind: "authenticated" };
    export let state: State;

    $: workspace = {
        ...workspaceFallback,
        ...state.workspace,
        ...(state.kind === "new-workspace"
            ? {
                  title: state.title,
                  projects: [projectFallback],
              }
            : undefined),
        ...(state.kind !== "new-workspace"
            ? { projects: [project] }
            : undefined),
    } satisfies WorkspaceDetail;

    $: project = {
        ...((state.kind === "new-workspace" ? undefined : state.project) ??
            projectFallback),
        ...(state.kind === "new-project"
            ? { title: state.title, sections: [] }
            : undefined),
        ...(state.kind === "new-task"
            ? {
                  sections: [
                      {
                          ...sectionFallback,
                          title: state.sectionTitle,
                          tasks: [
                              {
                                  ...taskFallback,
                                  sub_task_progress: null,
                                  title: state.title,
                              },
                          ],
                      },
                  ],
              }
            : undefined),
        ...(state.kind === "new-label"
            ? {
                  sections: [
                      {
                          ...state.section,
                          tasks: [
                              {
                                  ...state.task,
                                  sub_task_progress: null,
                                  labels: [
                                      { ...labelFallback, name: state.title },
                                  ],
                              },
                          ],
                      },
                  ],
              }
            : undefined),
        ...(state.kind === "assign-task"
            ? {
                  sections: [
                      {
                          ...sectionFallback,
                          tasks: [
                              {
                                  ...state.task,
                                  sub_task_progress: null,
                                  labels: [state.label],
                                  assignee: state.assignee,
                              },
                          ],
                      },
                  ],
              }
            : undefined),
    } satisfies ProjectDetail;

    const width = 500;
</script>

<div class="w-fit origin-center scale-[0.6]" style:width={width * 0.6} inert>
    <div class="flex flex-col bg-foreground ring-4 ring-border" style:width>
        <div class="flex flex-row">
            <div class="flex max-w-xs shrink flex-col py-4">
                <WorkspaceSelector open={true} {workspace} />
                <Projects {workspace} />
            </div>
            <div class="min-w-0 grow">
                <Dashboard data={{ user, project }} />
            </div>
        </div>
    </div>
</div>
