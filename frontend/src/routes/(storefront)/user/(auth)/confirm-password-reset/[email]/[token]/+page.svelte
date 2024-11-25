<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023, 2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import AuthScreen from "$lib/figma/screens/auth/AuthScreen.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { InputFieldValidation } from "$lib/funabashi/types";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { goto } from "$lib/navigation";
    import type { FormViewState } from "$lib/types/ui";
    import { requestPasswordResetUrl, resetPasswordUrl } from "$lib/urls/user";

    import type { PageData } from "./$types";
    import { openApiClient } from "$lib/repository/util";

    export let data: PageData;

    let state: FormViewState = { kind: "start" };

    const { email, token } = data;
    let password1: string | undefined = undefined;
    let password1Validation: InputFieldValidation | undefined = undefined;
    let password2: string | undefined = undefined;
    let password2Validation: InputFieldValidation | undefined = undefined;

    async function submit() {
        if (password1 === undefined) {
            throw new Error("Expected password1");
        }
        if (password2 === undefined) {
            throw new Error("Expected password1");
        }
        if (password1 !== password2) {
            state = {
                kind: "error",
                message: $_("auth.confirm-password-reset.validation.no-match"),
            };
            password1Validation = {
                ok: false,
                error: $_(
                    "auth.confirm-password-reset.password-1.validation.no-match",
                ),
            };
            password2Validation = {
                ok: false,
                error: $_(
                    "auth.confirm-password-reset.password-2.validation.no-match",
                ),
            };
            return;
        }
        password1Validation = password2Validation = undefined;
        state = { kind: "submitting" };
        const { error } = await openApiClient.POST(
            "/user/user/confirm-password-reset",
            { body: { email, token, new_password: password1 } },
        );
        if (error === undefined) {
            await goto(resetPasswordUrl);
            return;
        }
        if (error.code === 500) {
            state = {
                kind: "error",
                message: $_("auth.confirm-password-reset.errors.general"),
            };
            return;
        }
        const { details } = error;
        password1Validation = password2Validation = details.new_password
            ? {
                  ok: false,
                  error: details.new_password,
              }
            : {
                  ok: true,
                  result: $_(
                      "auth.confirm-password-reset.password-1.validation.valid",
                  ),
              };
        // TODO polish this error
        if (details.token) {
            throw new Error("Token was incorrect");
        }
        // TODO polish this error
        if (details.email) {
            throw new Error("Email was incorrect");
        }
        state = {
            kind: "error",
            message: $_("auth.confirm-password-reset.errors.field"),
        };
    }
</script>

<svelte:head>
    <title>{$_("auth.confirm-password-reset.title")}</title>
</svelte:head>

<AuthScreen title={$_("auth.confirm-password-reset.heading")} action={submit}>
    <div class="flex flex-col gap-6">
        <InputField
            placeholder={$_(
                "auth.confirm-password-reset.password-1.placeholder",
            )}
            style={{ inputType: "password" }}
            name="password-1"
            label={$_("auth.confirm-password-reset.password-1.label")}
            bind:value={password1}
            validation={password1Validation}
            required
        />
        <InputField
            placeholder={$_(
                "auth.confirm-password-reset.password-2.placeholder",
            )}
            style={{ inputType: "password" }}
            name="password-2"
            label={$_("auth.confirm-password-reset.password-2.label")}
            bind:value={password2}
            validation={password2Validation}
            required
        />
        {#if state.kind === "error"}
            <p>
                {state.message}
            </p>
            <Anchor
                label={$_(
                    "auth.confirm-password-reset.request-password-reset",
                )}
                href={requestPasswordResetUrl}
                size="normal"
            />
        {/if}
        <Button
            action={{
                kind: "submit",
                disabled: state.kind === "submitting",
            }}
            style={{ kind: "primary" }}
            color="blue"
            size="medium"
            label={state.kind == "submitting"
                ? $_("auth.confirm-password-reset.submit.submitting")
                : state.kind === "error"
                  ? $_("auth.confirm-password-reset.submit.error")
                  : $_("auth.confirm-password-reset.submit.start")}
        />
    </div>
</AuthScreen>
