<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 Saki Adachi -->
<!-- SPDX-FileCopyrightText: 2023, 2024 JWP Consulting GK -->
<script lang="ts">
    import {
        ArrowsExpand,
        ChevronDown,
        ChevronUp,
        Duplicate,
        SortAscending,
        SortDescending,
        SwitchVertical,
        Trash,
    } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import { goto } from "$lib/navigation";
    import { openDestructiveOverlay } from "$lib/stores/globalUi";
    import { canMoveTask, moveTask } from "$lib/repository/workspace/task";
    import type { ContextMenuType } from "$lib/types/ui";
    import {
        getTaskUrl,
        getDashboardSectionUrl,
        getDashboardProjectUrl,
    } from "$lib/urls";
    import { copyToClipboard } from "$lib/utils/clipboard";
    import { openApiClient } from "$lib/repository/util";
    import type { CurrentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import { getContext } from "svelte";

    const currentTeamMemberCan = getContext<CurrentTeamMemberCan>(
        "currentTeamMemberCan",
    );

    export let kind: ContextMenuType & { kind: "task" };

    async function promptDeleteTask() {
        await openDestructiveOverlay({
            kind: "deleteTask" as const,
            task: kind.task,
        });
        const { error } = await openApiClient.DELETE(
            "/workspace/task/{task_uuid}",
            {
                params: { path: { task_uuid: kind.task.uuid } },
            },
        );
        if (error !== undefined) {
            throw new Error("Could not delete task");
        }
        if (kind.location === "task") {
            await goto(getDashboardProjectUrl(kind.task.section.project));
        } else if (kind.location === "dashboard") {
            await goto(getDashboardSectionUrl(kind.section));
        } else {
            await goto(getDashboardProjectUrl(kind.project));
        }
    }

    let moveToSectionOpened = false;

    function toggleMoveToSection() {
        moveToSectionOpened = !moveToSectionOpened;
    }

    $: canMove = $currentTeamMemberCan("update", "task");
</script>

<Layout>
    {#if kind.location === "dashboard" && canMove}
        <ContextMenuButton
            kind={{
                kind: "a",
                href: getTaskUrl(kind.task),
            }}
            label={$_("overlay.context-menu.task.open-task")}
            icon={ArrowsExpand}
        />
        <ContextMenuButton
            kind={{
                kind: "button",
                action: toggleMoveToSection,
            }}
            label={$_("overlay.context-menu.task.move-to-section")}
            closeOnInteract={false}
            icon={SwitchVertical}
            iconRight={moveToSectionOpened ? ChevronUp : ChevronDown}
        />
        {#if moveToSectionOpened}
            <div class="flex max-h-60 max-w-xs flex-col overflow-y-auto">
                {#each kind.project.sections as section}
                    <ContextMenuButton
                        label={section.title}
                        kind={{
                            kind: "button",
                            action: moveTask.bind(null, kind.task, {
                                kind: "section",
                                section,
                            }),
                        }}
                    />
                {/each}
            </div>
        {/if}
        {#if canMoveTask( kind.task, { kind: "top", section: kind.section }, ) && canMove}
            <ContextMenuButton
                kind={{
                    kind: "button",
                    action: moveTask.bind(null, kind.task, {
                        kind: "top",
                        section: kind.section,
                    }),
                }}
                label={$_("overlay.context-menu.task.move-to-top")}
                icon={SortAscending}
            />
        {/if}
        {#if canMoveTask( kind.task, { kind: "bottom", section: kind.section }, ) && canMove}
            <ContextMenuButton
                kind={{
                    kind: "button",
                    action: moveTask.bind(null, kind.task, {
                        kind: "bottom",
                        section: kind.section,
                    }),
                }}
                label={$_("overlay.context-menu.task.move-to-bottom")}
                icon={SortDescending}
            />
        {/if}
    {/if}
    <ContextMenuButton
        kind={{
            kind: "button",
            action: copyToClipboard.bind(
                null,
                new URL(getTaskUrl(kind.task), document.baseURI).href,
            ),
        }}
        label={$_("overlay.context-menu.task.copy-link")}
        icon={Duplicate}
    />
    {#if $currentTeamMemberCan("delete", "task")}
        <ContextMenuButton
            kind={{
                kind: "button",
                action: promptDeleteTask,
            }}
            label={$_("overlay.context-menu.task.delete-task")}
            color="destructive"
            icon={Trash}
        />
    {/if}
</Layout>
