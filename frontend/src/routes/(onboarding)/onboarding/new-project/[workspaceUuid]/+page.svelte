<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _, json } from "svelte-i18n";

    import DashboardPlaceholder from "$lib/components/onboarding/DashboardPlaceholder.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { goto } from "$lib/navigation";
    import { getNewProjectUrl, getNewTaskUrl } from "$lib/urls/onboarding";

    import type { PageData } from "./$types";
    import type { InputFieldValidation } from "$lib/funabashi/types";
    import { openApiClient } from "$lib/repository/util";
    import type { FormViewState } from "$lib/types/ui";
    import { getLogInWithNextUrl } from "$lib/urls/user";

    export let data: PageData;

    const { user, workspace, project } = data;

    let state: FormViewState = { kind: "start" };

    let title: string | undefined = undefined;
    let titleValidation: InputFieldValidation | undefined = undefined;

    $: disabled = title === undefined || state.kind === "submitting";

    async function submit() {
        if (!title) {
            throw new Error("Expected title");
        }
        state = { kind: "submitting" };

        const { data, error } = await openApiClient.POST(
            "/workspace/project/",
            {
                body: {
                    workspace_uuid: workspace.uuid,
                    title,
                    description: null,
                },
            },
        );
        if (data) {
            const { uuid } = data;
            const nextStep = getNewTaskUrl(uuid);
            await goto(nextStep);
            return;
        }
        if (error.code === 403) {
            await goto(getLogInWithNextUrl(getNewProjectUrl(workspace.uuid)));
            return;
        }
        if (error.code === 500) {
            state = {
                kind: "error",
                message: $_("onboarding.new-project.errors.general"),
            };
            return;
        }
        titleValidation = error.details.title
            ? { ok: false, error: error.details.title }
            : {
                  ok: true,
                  result: $_("onboarding.new-project.fields.title.valid"),
              };
        state = {
            kind: "error",
            message: $_("onboarding.new-project.errors.field"),
        };
    }

    $: prompts = $json("onboarding.new-project.prompt") as string[];
</script>

<svelte:head><title>{$_("onboarding.new-project.title")}</title></svelte:head>

<Onboarding
    stepCount={5}
    step={1}
    nextAction={{
        kind: "submit",
        disabled,
        submit,
    }}
>
    <svelte:fragment slot="title"
        >{$_("onboarding.new-project.heading")}</svelte:fragment
    >
    <svelte:fragment slot="prompt">
        <div class="flex flex-col gap-8">
            {#if project}
                <div class="flex flex-col gap-4">
                    <p>
                        {$_("onboarding.new-project.project-exists.message", {
                            values: { title: project.title },
                        })}
                    </p>
                    <p>
                        <Anchor
                            label={$_(
                                "onboarding.new-project.project-exists.prompt",
                                { values: { title: project.title } },
                            )}
                            size="large"
                            href={getNewTaskUrl(project.uuid)}
                        />
                    </p>
                </div>
            {:else}
                <div class="flex flex-col gap-3">
                    {#each prompts as prompt}
                        <p>{prompt}</p>
                    {/each}
                </div>
            {/if}
        </div>
    </svelte:fragment>

    <svelte:fragment slot="inputs">
        <InputField
            style={{ inputType: "text" }}
            name="title"
            label={$_("onboarding.new-project.fields.title.label")}
            placeholder={$_("onboarding.new-project.fields.title.placeholder")}
            bind:value={title}
            required
            validation={titleValidation}
        />
        {#if state.kind === "error"}
            <p>{state.message}</p>
        {/if}
    </svelte:fragment>

    <DashboardPlaceholder
        slot="content"
        {user}
        state={{
            kind: "new-project",
            workspace,
            project,
            title:
                title ??
                project?.title ??
                $_("onboarding.new-project.default-name"),
        }}
    />
</Onboarding>
