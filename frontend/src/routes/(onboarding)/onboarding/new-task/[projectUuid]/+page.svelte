<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import DashboardPlaceholder from "$lib/components/onboarding/DashboardPlaceholder.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { goto } from "$lib/navigation";
    import { createTask } from "$lib/repository/workspace/task";
    import { getNewLabelUrl } from "$lib/urls/onboarding";

    import type { PageData } from "./$types";
    import { openApiClient } from "$lib/repository/util";

    export let data: PageData;

    const { user, workspace, project, section } = data;

    let taskTitle: string | undefined = undefined;

    $: sectionTitle =
        section?.title ?? $_("onboarding.new-task.section-title");

    $: disabled = taskTitle === undefined;
    async function submit() {
        // TODO add state tracking with submit button blocking
        if (!taskTitle) {
            throw new Error("Expected taskTitle");
        }
        const { error, data: section } = await openApiClient.POST(
            "/workspace/section/",
            {
                body: {
                    project_uuid: project.uuid,
                    title: sectionTitle,
                    description: null,
                },
            },
        );
        if (error) {
            throw Error("Could not create section");
        }
        // Find ourselves
        const assignee =
            workspace.team_members.find((w) => w.user.email === user.email) ??
            null;
        const { error: e, data: task } = await createTask({
            title: taskTitle,
            description: null,
            labels: [],
            section,
            assignee,
            due_date: null,
            sub_tasks: [],
        });
        if (e) {
            throw new Error(`Unhandled error: ${JSON.stringify(e)}`);
        }
        const { uuid } = task;
        await goto(getNewLabelUrl(uuid));
    }
</script>

<svelte:head>
    <title>{$_("onboarding.new-task.title")}</title>
</svelte:head>

<Onboarding
    stepCount={5}
    step={2}
    nextAction={{ kind: "submit", disabled, submit }}
>
    <svelte:fragment slot="title"
        >{$_("onboarding.new-task.heading")}</svelte:fragment
    >
    <svelte:fragment slot="prompt">
        <div class="flex flex-col gap-4">
            <p>
                {#if section}
                    {$_("onboarding.new-task.prompt.exists", {
                        values: { sectionTitle },
                    })}
                {:else}
                    {$_("onboarding.new-task.prompt.location", {
                        values: { sectionTitle },
                    })}
                {/if}
            </p>
            <p>{$_("onboarding.new-task.prompt.explanation")}</p>
        </div>
    </svelte:fragment>

    <svelte:fragment slot="inputs">
        <InputField
            style={{ inputType: "text" }}
            name="task-title"
            label={$_("onboarding.new-task.input.label")}
            placeholder={$_("onboarding.new-task.input.placeholder")}
            bind:value={taskTitle}
        />
    </svelte:fragment>

    <DashboardPlaceholder
        slot="content"
        {user}
        state={{
            kind: "new-task",
            workspace,
            project,
            sectionTitle,
            title: taskTitle ?? $_("onboarding.new-task.default-name"),
        }}
    />
</Onboarding>
