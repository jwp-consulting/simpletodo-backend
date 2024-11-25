<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { onMount } from "svelte";
    import { _, number } from "svelte-i18n";

    import Loading from "$lib/components/Loading.svelte";
    import Breadcrumbs from "$lib/figma/screens/task/Breadcrumbs.svelte";
    import Form from "$lib/figma/screens/task/Form.svelte";
    import Layout from "$lib/figma/screens/task/Layout.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { goto } from "$lib/navigation";
    import { updateTask } from "$lib/repository/workspace/task";
    import { createSubTaskAssignment } from "$lib/stores/dashboard/subTaskAssignment";
    import { createLabelAssignment } from "$lib/stores/dashboard/labelAssignment";
    import { createTeamMemberAssignment } from "$lib/stores/dashboard/teamMemberAssignment";
    import type {
        LabelAssignment,
        SubTaskAssignment,
        TeamMemberAssignment,
    } from "$lib/types/stores";
    import type { TaskDetail } from "$lib/types/workspace";
    import {
        getDashboardSectionUrl,
        getDashboardProjectUrl,
        getTaskUrl,
    } from "$lib/urls";
    import { coerceIsoDate } from "$lib/utils/date";

    import type { PageData } from "./$types";
    import { beforeNavigate } from "$app/navigation";
    import type { BeforeNavigate } from "@sveltejs/kit";
    import type { FormViewState } from "$lib/types/ui";
    import type { InputFieldValidation } from "$lib/funabashi/types";

    export let data: PageData;
    const { task } = data;

    // Initial data
    let title: string | null = null;
    let titleValidation: InputFieldValidation | undefined = undefined;
    let description: string | null = null;
    let descriptionValidation: string | undefined = undefined;
    let dueDate: string | null = null;
    let dueDateValidation: InputFieldValidation | undefined = undefined;

    let teamMemberAssignment: TeamMemberAssignment | undefined = undefined;
    let teamMemberAssignmentValidation: string | undefined = undefined;
    let labelAssignment: LabelAssignment | undefined = undefined;
    let labelAssignmentValidation: string | undefined = undefined;
    let subTaskAssignment: SubTaskAssignment | undefined = undefined;
    let subTaskAssignmentValidation: string | undefined = undefined;

    onMount(() => {
        const t = task;
        title = t.title;
        description = t.description;
        dueDate = t.due_date && coerceIsoDate(t.due_date);
        teamMemberAssignment = createTeamMemberAssignment(t);
        labelAssignment = createLabelAssignment(t);
        subTaskAssignment = createSubTaskAssignment(t);
    });

    $: subTasks = subTaskAssignment?.subTasks;

    // XXX I am sure we can have really fancy validation
    $: canUpdate =
        state.kind !== "done" &&
        state.kind !== "submitting" &&
        title !== null &&
        $subTasks !== undefined;

    type State = FormViewState | { kind: "done" };
    let state: State = { kind: "start" };

    async function action(task: TaskDetail, continueEditing: boolean) {
        if (title === null) {
            throw new Error("Expected title");
        }
        if (!$labelAssignment) {
            throw new Error("Expected $labelAssignment");
        }
        state = { kind: "submitting" };
        const { data: result, error } = await updateTask(
            { uuid: task.uuid },
            {
                title,
                description,
                due_date: dueDate,
                assignee: $teamMemberAssignment ?? null,
                labels: $labelAssignment,
                sub_tasks: $subTasks ?? [],
            },
        );
        if (result) {
            state = { kind: "done" };
            if (continueEditing) {
                await goto(getTaskUrl(task));
            } else {
                await goto(getDashboardSectionUrl(task.section));
            }
            return;
        }
        if (error.code === 500 || error.code === 404) {
            state = {
                kind: "error",
                message: $_("task-screen.update.errors.general"),
            };
            return;
        } else if (error.code === 403) {
            // TODO handle authentication error
            state = {
                kind: "error",
                message: $_("task-screen.update.errors.general"),
            };
            return;
        }
        const { details } = error;
        titleValidation = details.title
            ? { ok: false, error: details.title }
            : { ok: true, result: $_("task-screen.form.title.valid") };
        descriptionValidation =
            details.description ?? $_("task-screen.form.description.valid");
        dueDateValidation = details.due_date
            ? { ok: false, error: details.due_date }
            : { ok: true, result: $_("task-screen.form.due-date.valid") };

        teamMemberAssignmentValidation = details.assignee
            ? $_("task-screen.form.assignee.invalid", {
                  values: { error: JSON.stringify(details.assignee) },
              })
            : $_("task-screen.form.assignee.valid");
        labelAssignmentValidation = details.labels
            ? $_("task-screen.form.labels.invalid", {
                  values: { error: JSON.stringify(details.labels) },
              })
            : $_("task-screen.form.labels.valid");
        // TODO annotate each sub task correctly
        subTaskAssignmentValidation = details.sub_tasks
            ? $_("task-screen.sub-tasks.invalid", {
                  values: { error: JSON.stringify(details.sub_tasks) },
              })
            : $_("task-screen.sub-tasks.valid");
        state = {
            kind: "error",
            message: $_("task-screen.update.errors.field"),
        };
    }

    beforeNavigate((navigation: BeforeNavigate) => {
        if (state.kind === "done") {
            return;
        }
        const navigateAway = window.confirm(
            $_("task-screen.confirm-navigate-away.update"),
        );
        if (!navigateAway) {
            navigation.cancel();
        }
    });
</script>

<svelte:head>
    <title
        >{$_("task.update-task-title", {
            values: { title: task.title },
        })}</title
    >
</svelte:head>

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
                // We could add a better task name here, or even
                // extract the whole thing as a layout for any task/[taskUuid] route
                {
                    label: $number(task.number),
                    href: getTaskUrl(task),
                },
            ]}
        />
        <svelte:fragment slot="buttons">
            <Button
                grow={false}
                action={{
                    kind: "submit",
                    form: "task-form",
                    disabled: !canUpdate,
                }}
                color="blue"
                size="medium"
                style={{ kind: "primary" }}
                label={$_("task-screen.update.update")}
            />
            <Button
                grow={false}
                action={{
                    kind: "button",
                    action: () => action(task, true),
                    disabled: !canUpdate,
                }}
                color="blue"
                size="medium"
                style={{ kind: "primary" }}
                label={$_("task-screen.update.update-continue-editing")}
            />
        </svelte:fragment>
    </TopBar>
    <svelte:fragment slot="content">
        {#if state.kind === "error"}
            <p class="text-error">{state.message}</p>
        {/if}
        {#if teamMemberAssignment && labelAssignment && subTaskAssignment}
            <Form
                action={action.bind(null, task, false)}
                {teamMemberAssignment}
                {teamMemberAssignmentValidation}
                {labelAssignment}
                {labelAssignmentValidation}
                {subTaskAssignment}
                {subTaskAssignmentValidation}
                bind:title
                {titleValidation}
                bind:dueDate
                {dueDateValidation}
                bind:description
                {descriptionValidation}
            />
        {:else}
            <Loading />
        {/if}
    </svelte:fragment>
</Layout>
