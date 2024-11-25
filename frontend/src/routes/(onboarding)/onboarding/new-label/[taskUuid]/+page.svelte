<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import DashboardPlaceholder from "$lib/components/onboarding/DashboardPlaceholder.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { InputFieldValidation } from "$lib/funabashi/types";
    import { goto } from "$lib/navigation";
    import { updateTask } from "$lib/repository/workspace/task";
    import { createLabel } from "$lib/repository/workspace/label";
    import type { FormViewState } from "$lib/types/ui";
    import { getAssignTaskUrl, getNewTaskUrl } from "$lib/urls/onboarding";
    import { cloneMutable } from "$lib/utils/type";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { user, workspace, project, section, task } = data;

    const taskTitle = task.title;
    let labelTitle: string | undefined = undefined;
    let labelTitleValidation: InputFieldValidation | undefined = undefined;

    let state: FormViewState = { kind: "start" };

    $: disabled = !labelTitle || state.kind === "submitting";

    async function submit() {
        if (!labelTitle) {
            throw new Error("Expected labelTitle");
        }

        state = { kind: "submitting" };
        const { error, data } = await createLabel(workspace, {
            name: labelTitle,
            color: 0,
        });
        labelTitleValidation = undefined;
        if (error?.code === 400) {
            if (error.details.name) {
                labelTitleValidation = {
                    ok: false,
                    error: error.details.name,
                };
            }
            state = {
                kind: "error",
                message: $_("onboarding.new-label.error"),
            };
            return;
        } else if (error) {
            throw new Error("No data returned");
        }

        const label = data;
        await updateTask(task, {
            ...cloneMutable(task),
            labels: [label],
            assignee: task.assignee,
        });
        // TODO handle if label with this name already exists
        await goto(getAssignTaskUrl(task.uuid));
    }
</script>

<svelte:head>
    <title
        >{$_("onboarding.new-label.title", {
            values: { taskTitle },
        })}</title
    >
</svelte:head>

<Onboarding
    stepCount={5}
    step={4}
    backAction={{ kind: "a", href: getNewTaskUrl(project.uuid) }}
    nextAction={{ kind: "submit", disabled, submit }}
>
    <svelte:fragment slot="title"
        >{$_("onboarding.new-label.heading", {
            values: { taskTitle },
        })}</svelte:fragment
    >
    <svelte:fragment slot="prompt"
        ><p>{$_("onboarding.new-label.prompt")}</p></svelte:fragment
    >

    <svelte:fragment slot="inputs">
        <InputField
            style={{ inputType: "text" }}
            name="label-title"
            label={$_("onboarding.new-label.input.label")}
            placeholder={$_("onboarding.new-label.input.placeholder")}
            bind:value={labelTitle}
            validation={labelTitleValidation}
        />
        {#if state.kind === "error"}
            <p>
                {state.message}
            </p>
        {/if}
    </svelte:fragment>

    <DashboardPlaceholder
        slot="content"
        {user}
        state={{
            kind: "new-label",
            workspace,
            project,
            section,
            task,
            title: labelTitle ?? $_("onboarding.new-label.default-name"),
        }}
    />
</Onboarding>
