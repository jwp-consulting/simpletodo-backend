<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { goto } from "$lib/navigation";
    import { updateUserProfile } from "$lib/stores/user";
    import { aboutYouUrl, newWorkspaceUrl } from "$lib/urls/onboarding";

    import type { PageData } from "./$types";
    import type { InputFieldValidation } from "$lib/funabashi/types";
    import type { FormViewState } from "$lib/types/ui";
    import { getLogInWithNextUrl } from "$lib/urls/user";

    export let data: PageData;
    const { user } = data;

    let state: FormViewState = { kind: "start" };
    let preferredName: PageData["user"]["preferred_name"] =
        user.preferred_name;
    let preferredNameValidation: InputFieldValidation | undefined = undefined;

    async function submit() {
        state = { kind: "submitting" };
        const { error, data } = await updateUserProfile(preferredName);
        if (data) {
            await goto(newWorkspaceUrl);
            return;
        }
        if (error.code === 500) {
            state = {
                kind: "error",
                message: $_("onboarding.about-you.errors.server", {
                    values: { error: JSON.stringify(error) },
                }),
            };
            return;
        }
        if (error.code === 403) {
            await goto(getLogInWithNextUrl(aboutYouUrl));
            return;
        }
        const { details } = error;
        preferredNameValidation = details.preferred_name
            ? { ok: false, error: details.preferred_name }
            : undefined;
        state = {
            kind: "error",
            message: $_("onboarding.about-you.errors.fields"),
        };
    }
</script>

<svelte:head><title>{$_("onboarding.about-you.title")}</title></svelte:head>

<Onboarding
    nextAction={{
        kind: "submit",
        submit: submit,
        disabled: state.kind === "submitting",
    }}
>
    <svelte:fragment slot="title"
        >{$_("onboarding.about-you.heading")}</svelte:fragment
    >
    <svelte:fragment slot="prompt">
        {$_("onboarding.about-you.prompt")}
    </svelte:fragment>
    <svelte:fragment slot="inputs">
        <InputField
            bind:value={preferredName}
            label={$_("onboarding.about-you.input.label")}
            placeholder={$_("onboarding.about-you.input.placeholder")}
            style={{ inputType: "text" }}
            name="full-name"
            validation={preferredNameValidation}
        />
        {#if state.kind === "error"}
            <p>{state.message}</p>
        {/if}
    </svelte:fragment>

    <svelte:fragment slot="content">
        <h1
            class="w-full overflow-hidden text-ellipsis text-center text-4xl font-bold"
        >
            {#if preferredName !== null && preferredName !== ""}
                {$_("onboarding.about-you.greeting.with-name", {
                    values: { name: preferredName },
                })}
            {:else}
                {$_("onboarding.about-you.greeting.without-name")}
            {/if}
        </h1>
    </svelte:fragment>
</Onboarding>
