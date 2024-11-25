<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import type { ProjectDetailTask } from "$lib/types/workspace";
    import { getNewTaskUrl } from "$lib/urls";
    import SectionTitle from "$lib/figma/cards/section-bar/SectionTitle.svelte";
    import TaskCard from "$lib/figma/cards/TaskCard.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";
    import type {
        ProjectDetail,
        ProjectDetailSection,
    } from "$lib/types/workspace";
    import { currentSections } from "$lib/stores/dashboard/section";
    import { handleKey } from "$lib/utils/keyboard";
    import { onMount, getContext, setContext } from "svelte";
    import type { PageData } from "./$types";
    import type { CurrentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import type { WsResource } from "$lib/types/stores";
    import { readonly, writable } from "svelte/store";

    const currentProject =
        getContext<WsResource<ProjectDetail>>("currentProject");
    const currentTeamMemberCan = getContext<CurrentTeamMemberCan>(
        "currentTeamMemberCan",
    );
    const sectionClosed = getContext<Set<string>>("sectionClosed");

    export let data: PageData;

    let { project } = data;
    $: project = $currentProject.or(data.project);

    $: hasSections = project.sections.length > 0;

    let sections: readonly ProjectDetailSection[];
    $: sections = $currentSections ?? [];

    async function onAddNewSection() {
        await openConstructiveOverlay({
            kind: "createSection",
            project,
        });
    }

    onMount(() => {
        return handleKey("j", () => selectInProject(project, "next-task"));
    });

    onMount(() => {
        return handleKey("k", () => selectInProject(project, "prev-task"));
    });

    onMount(() => {
        return handleKey("h", () => selectInProject(project, "prev-section"));
    });

    onMount(() => {
        return handleKey("l", () => selectInProject(project, "next-section"));
    });

    type SectionTaskSelection =
        | {
              kind: "task-selected";
              project: ProjectDetail;
              sectionUuid: string;
              taskUuid: string;
          }
        | {
              kind: "section-selected";
              project: ProjectDetail;
              sectionUuid: string;
              taskUuid: undefined;
          }
        | {
              kind: "project-selected";
              project: ProjectDetail;
              sectionUuid: undefined;
              taskUuid: undefined;
          }
        | undefined;

    const _currentSectionTask = writable<SectionTaskSelection>(
        undefined,
        (set, update) => {
            const unsubscriber = currentProject.subscribe(
                ($currentProject) => {
                    const project = $currentProject.value;
                    const projectUuid = project?.uuid;
                    if (!projectUuid) {
                        set(undefined);
                    } else {
                        update(($currentSectionTask) => {
                            // if no current selection, overwrite
                            if (
                                $currentSectionTask?.project.uuid ===
                                projectUuid
                            ) {
                                return;
                            } else {
                                return {
                                    kind: "project-selected",
                                    project,
                                    sectionUuid: undefined,
                                    taskUuid: undefined,
                                };
                            }
                        });
                    }
                },
            );
            return unsubscriber;
        },
    );

    const currentSectionTask = readonly(_currentSectionTask);
    setContext("currentSectionTask", currentSectionTask);

    // XXX this is very complicated code, but it works
    // Possible scenarios
    // current   input        action
    // project   next section select 1st section (if exist), 1st task (if exist)
    // project   next task    select 1st section (if exist), 1st task (if exist)
    // project   prev section select 1st section (if exist), 1st task (if exist)
    // project   prev task    select 1st section (if exist), 1st task (if exist)
    // section   next section select next section (if exist), 1st task (if exist)
    // section   next task    select 1st task (if exist)
    // section   prev section select prev section (if exist), 1st task (if exist)
    // section   prev task    select prev section (if exist), 1st task (if exist)
    // task      next section select next section, 1st task (if exist)
    // task      next task    select next task across sections (if exist)
    // task      prev section select prev section, last task (if exist)
    // task      prev task    select prev task across sections (if exist)
    // undefined next section select 1st section (if exist), 1st task (if exist)
    // undefined next task    select 1st section (if exist), 1st task (if exist)
    // undefined prev section select 1st section (if exist), 1st task (if exist)
    // undefined prev task    select 1st section (if exist), 1st task (if exist)
    type SelectionKind =
        | "prev-section"
        | "prev-task"
        | "next-section"
        | "next-task";
    export function selectInProject(
        project: ProjectDetail | undefined,
        action: SelectionKind,
    ) {
        if (project === undefined) {
            _currentSectionTask.set(undefined);
            return;
        }
        _currentSectionTask.update(
            (
                $currentSectionTask: SectionTaskSelection,
            ): SectionTaskSelection => {
                if (
                    $currentSectionTask === undefined ||
                    $currentSectionTask.kind === "project-selected"
                ) {
                    const firstSection = project.sections.at(0);
                    const firstTask = firstSection?.tasks.at(0);
                    if (
                        firstSection !== undefined &&
                        firstTask !== undefined
                    ) {
                        return {
                            kind: "task-selected",
                            taskUuid: firstTask.uuid,
                            sectionUuid: firstSection.uuid,
                            project,
                        };
                    }
                    throw new Error("fall-through");
                }

                const sectionIx = project.sections.findIndex(
                    (s: ProjectDetailSection) =>
                        s.uuid === $currentSectionTask.sectionUuid,
                );
                const section = project.sections[sectionIx];
                if (!section) {
                    throw new Error("Expected section");
                }
                const nextSectionIx = sectionIx + 1;
                const nextSection = project.sections[nextSectionIx];
                const nextSectionTask = nextSection?.tasks[0];
                const prevSectionIx = sectionIx - 1;
                const prevSection = project.sections[prevSectionIx];
                const prevSectionTask = prevSection?.tasks[0];

                const taskIx = section.tasks.findIndex(
                    (t: ProjectDetailTask) =>
                        t.uuid === $currentSectionTask.taskUuid,
                );
                const task = section.tasks[taskIx];
                const prevTask = section.tasks[taskIx - 1];
                const nextTask = section.tasks[taskIx + 1];
                const lastTask = prevSection?.tasks.at(-1);
                const firstTask = nextSection?.tasks[0];
                if ($currentSectionTask.kind === "section-selected") {
                    switch (action) {
                        case "next-section": {
                            if (nextSection && nextSectionTask) {
                                return {
                                    ...$currentSectionTask,
                                    kind: "task-selected",
                                    sectionUuid: nextSection.uuid,
                                    taskUuid: nextSectionTask.uuid,
                                };
                            } else if (nextSection) {
                                return {
                                    ...$currentSectionTask,
                                    sectionUuid: nextSection.uuid,
                                };
                            } else {
                                return $currentSectionTask;
                            }
                        }
                        case "next-task": {
                            const taskUuid = section.tasks[0]?.uuid;
                            if (taskUuid) {
                                return {
                                    ...$currentSectionTask,
                                    kind: "task-selected",
                                    taskUuid,
                                };
                            } else {
                                return $currentSectionTask;
                            }
                        }
                        case "prev-task":
                        case "prev-section": {
                            if (prevSection && prevSectionTask) {
                                return {
                                    ...$currentSectionTask,
                                    kind: "task-selected",
                                    sectionUuid: prevSection.uuid,
                                    taskUuid: prevSectionTask.uuid,
                                };
                            } else if (prevSection) {
                                return {
                                    ...$currentSectionTask,
                                    sectionUuid: prevSection.uuid,
                                };
                            } else {
                                return $currentSectionTask;
                            }
                        }
                    }
                } else {
                    if (!task) {
                        throw new Error("Expected task");
                    }
                    switch (action) {
                        case "next-section": {
                            if (nextSection && nextSectionTask) {
                                return {
                                    ...$currentSectionTask,
                                    kind: "task-selected",
                                    sectionUuid: nextSection.uuid,
                                    taskUuid: nextSectionTask.uuid,
                                };
                            } else if (nextSection) {
                                return {
                                    ...$currentSectionTask,
                                    sectionUuid: nextSection.uuid,
                                };
                            } else {
                                return $currentSectionTask;
                            }
                        }
                        case "prev-section": {
                            if (prevSection && prevSectionTask) {
                                return {
                                    ...$currentSectionTask,
                                    kind: "task-selected",
                                    sectionUuid: prevSection.uuid,
                                    taskUuid: prevSectionTask.uuid,
                                };
                            } else if (prevSection) {
                                return {
                                    ...$currentSectionTask,
                                    sectionUuid: prevSection.uuid,
                                };
                            } else {
                                return $currentSectionTask;
                            }
                        }
                        case "prev-task": {
                            if (prevTask) {
                                return {
                                    ...$currentSectionTask,
                                    taskUuid: prevTask.uuid,
                                };
                            } else if (prevSection && lastTask) {
                                return {
                                    ...$currentSectionTask,
                                    sectionUuid: prevSection.uuid,
                                    taskUuid: lastTask.uuid,
                                };
                            } else if (prevSection) {
                                return {
                                    ...$currentSectionTask,
                                    kind: "section-selected",
                                    sectionUuid: prevSection.uuid,
                                    taskUuid: undefined,
                                };
                            } else {
                                return $currentSectionTask;
                            }
                        }
                        case "next-task": {
                            if (nextTask) {
                                return {
                                    ...$currentSectionTask,
                                    taskUuid: nextTask.uuid,
                                };
                            } else if (nextSection && firstTask) {
                                return {
                                    ...$currentSectionTask,
                                    sectionUuid: nextSection.uuid,
                                    taskUuid: firstTask.uuid,
                                };
                            } else if (nextSection) {
                                return {
                                    ...$currentSectionTask,
                                    kind: "section-selected",
                                    sectionUuid: nextSection.uuid,
                                    taskUuid: undefined,
                                };
                            } else {
                                return $currentSectionTask;
                            }
                        }
                    }
                }
            },
        );
    }
</script>

<svelte:head>
    <title
        >{$_("dashboard.title", {
            values: { title: project.title },
        })}</title
    >
</svelte:head>

<!-- Sections -->
{#each sections as section (section.uuid)}
    {@const open = !$sectionClosed.has(section.uuid)}
    {@const isCurrentSection =
        $currentSectionTask?.sectionUuid === section.uuid}
    <section class="flex flex-col" class:ring={isCurrentSection}>
        <SectionTitle {project} {section} {open} />
        {#if open}
            <table
                class="flex flex-col gap-2 rounded-b-2xl bg-foreground p-4 lg:grid lg:grid-cols-[8fr_3fr_max-content] lg:gap-4"
            >
                <tbody class="contents">
                    {#each section.tasks as task (task.uuid)}
                        <TaskCard {project} {task} {section} />
                    {:else}
                        <p>
                            {$_("dashboard.section.empty.message")}
                            <Anchor
                                label={$_("dashboard.section.empty.prompt")}
                                size="normal"
                                href={getNewTaskUrl(section)}
                            />
                        </p>
                    {/each}
                </tbody>
            </table>
        {/if}
    </section>
{:else}
    <section class="py-2 px-4 gap-8 bg-foreground rounded-lg flex flex-col">
        <p>
            {$_("dashboard.no-sections.message")}
        </p>
        <Button
            style={{ kind: "primary" }}
            color="blue"
            size="medium"
            grow={false}
            label={$_("dashboard.no-sections.prompt")}
            action={{ kind: "button", action: onAddNewSection }}
        />
    </section>
{/each}

{#if hasSections && $currentTeamMemberCan("create", "section")}
    <div class="sticky bottom-0 self-end p-2">
        <Button
            style={{ kind: "primary" }}
            label={$_("dashboard.actions.add-section")}
            size="medium"
            action={{ kind: "button", action: onAddNewSection }}
            color="blue"
        />
    </div>
{/if}
