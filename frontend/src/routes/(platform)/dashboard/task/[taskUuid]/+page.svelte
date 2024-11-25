<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { _, number } from "svelte-i18n";

    import Breadcrumbs from "$lib/figma/screens/task/Breadcrumbs.svelte";
    import Fields from "$lib/figma/screens/task/Fields.svelte";
    import Layout from "$lib/figma/screens/task/Layout.svelte";
    import ReadSubTasks from "$lib/figma/screens/task/ReadSubTasks.svelte";
    import TaskDescription from "$lib/figma/screens/task/TaskDescription.svelte";
    import TaskDueDate from "$lib/figma/screens/task/TaskDueDate.svelte";
    import TaskLabel from "$lib/figma/screens/task/TaskLabel.svelte";
    import TaskTitle from "$lib/figma/screens/task/TaskTitle.svelte";
    import TaskUser from "$lib/figma/screens/task/TaskUser.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    import { openContextMenu } from "$lib/stores/globalUi";
    import {
        getDashboardSectionUrl,
        getDashboardProjectUrl,
        getTaskEditUrl,
        getTaskUrl,
    } from "$lib/urls";
    import { coerceIsoDate } from "$lib/utils/date";

    import type { PageData } from "./$types";

    import { goto } from "$app/navigation";
    import type { CurrentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import { getContext } from "svelte";
    import type { TaskDetail } from "$lib/types/workspace";
    import type { WsResource } from "$lib/types/stores";

    const currentTeamMemberCan = getContext<CurrentTeamMemberCan>(
        "currentTeamMemberCan",
    );

    export let data: PageData;

    const currentTask = getContext<WsResource<TaskDetail>>("currentTask");

    $: task = $currentTask.or(data.task);

    let contextMenuRef: HTMLElement;

    async function onInteract() {
        if (!$currentTeamMemberCan("update", "task")) {
            return;
        }
        await goto(getTaskEditUrl(task));
    }
</script>

<Layout>
    <TopBar slot="top-bar" section={task.section}>
        <Breadcrumbs
            slot="breadcrumbs"
            crumbs={[
                {
                    label: task.section.project.title,
                    href: getDashboardProjectUrl(task.section.project),
                },
                {
                    label: task.section.title,
                    href: getDashboardSectionUrl(task.section),
                },
                {
                    label: $number(task.number),
                    href: getTaskUrl(task),
                },
            ]}
        />
        <svelte:fragment slot="buttons">
            {#if $currentTeamMemberCan("update", "task")}
                <Button
                    grow={false}
                    color="blue"
                    size="medium"
                    style={{ kind: "primary" }}
                    label={$_("task-screen.edit")}
                    action={{ kind: "a", href: getTaskEditUrl(task) }}
                />
            {/if}
            <div bind:this={contextMenuRef}>
                <SquovalIcon
                    ariaLabel={$_("task-screen.open-context-menu")}
                    icon="dotsVertical"
                    state="active"
                    action={{
                        kind: "button",
                        action: openContextMenu.bind(
                            null,
                            {
                                kind: "task",
                                task,
                                location: "task",
                            },
                            contextMenuRef,
                        ),
                    }}
                />
            </div>
        </svelte:fragment>
    </TopBar>
    <svelte:fragment slot="content">
        <Fields>
            <TaskTitle slot="title" title={task.title} readonly {onInteract} />
            <TaskUser
                slot="assignee"
                teamMember={task.assignee}
                {onInteract}
                readonly
            />
            <TaskLabel
                slot="labels"
                labels={task.labels}
                {onInteract}
                readonly
            />
            <TaskDueDate
                slot="due-date"
                dueDate={task.due_date && coerceIsoDate(task.due_date)}
                readonly
                {onInteract}
            />
            <TaskDescription
                slot="description"
                readonly
                description={task.description}
                {onInteract}
            />
        </Fields>
        <ReadSubTasks subTasks={task.sub_tasks} {onInteract} />
    </svelte:fragment>
</Layout>
