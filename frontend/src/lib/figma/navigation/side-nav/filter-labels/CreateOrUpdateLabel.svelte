<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<script lang="ts">
    import { onMount } from "svelte";
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { InputFieldValidation } from "$lib/funabashi/types";
    import { createLabel, updateLabel } from "$lib/repository/workspace/label";
    import { currentWorkspace } from "$lib/stores/dashboard/workspace";
    import { getContext } from "svelte";
    import type { WsResource } from "$lib/types/stores";
    import type { ProjectDetail } from "$lib/types/workspace";

    const currentProject =
        getContext<WsResource<ProjectDetail>>("currentProject");
    import type { FormViewState } from "$lib/types/ui";
    import type { Label } from "$lib/types/workspace";
    import {
        getIndexFromLabelColor,
        getLabelColorFromIndex,
        labelColors,
        type LabelColor,
    } from "$lib/utils/colors";

    import LabelRadio from "./LabelRadio.svelte";
    import { getLogInWithNextUrl } from "$lib/urls/user";
    import { getDashboardWorkspaceUrl } from "$lib/urls";
    import { goto } from "$lib/navigation";

    export let state: { kind: "create" } | { kind: "update"; label: Label };
    export let onFinished: () => void;

    let chosenColor: LabelColor | undefined = undefined;
    let chosenColorValidation: InputFieldValidation | undefined = undefined;
    let labelName: string | undefined = undefined;
    let labelNameValidation: InputFieldValidation | undefined = undefined;

    let editState: FormViewState = { kind: "start" };

    onMount(() => {
        if (state.kind === "create") {
            return;
        }
        const { label } = state;
        const labelColor = getLabelColorFromIndex(label.color);
        if (!labelColor) {
            console.warn("No color found for", label);
        }
        chosenColor = labelColor ?? labelColors[0];
        labelName = label.name;
    });

    // We can only save if
    // 1) both fields are non-empty,
    // 2) we are not submitting already
    $: canSave =
        chosenColor !== undefined &&
        labelName !== undefined &&
        editState.kind != "submitting";

    async function create() {
        if (!chosenColor) {
            throw new Error("Expected chosenColor");
        }
        if (!labelName) {
            throw new Error("Expected labelName");
        }
        if (state.kind !== "create") {
            throw new Error("Expected create state");
        }

        const workspace =
            $currentWorkspace.value ?? $currentProject.value?.workspace;
        if (workspace === undefined) {
            throw new Error("Expected workspace");
        }

        editState = { kind: "submitting" };
        labelNameValidation = undefined;
        chosenColorValidation = undefined;

        const color = getIndexFromLabelColor(chosenColor);
        const { error, data } = await createLabel(workspace, {
            name: labelName,
            color,
        });
        if (data) {
            editState = { kind: "start" };
            onFinished();
            return;
        }
        if (error.code === 403) {
            await goto(
                getLogInWithNextUrl(getDashboardWorkspaceUrl(workspace)),
            );
            return;
        }
        if (error.code === 500) {
            editState = {
                kind: "error",
                message: $_("dashboard.side-nav.filter-labels.errors.general"),
            };
            return;
        }
        const { details } = error;
        labelNameValidation = details.name
            ? { ok: false, error: details.name }
            : undefined;
        chosenColorValidation = details.color
            ? { ok: false, error: details.color }
            : undefined;
        editState = {
            kind: "error",
            message:
                error.general ??
                $_("dashboard.side-nav.filter-labels.errors.create"),
        };
    }

    async function update() {
        if (!chosenColor) {
            throw new Error("Expected chosenColor");
        }
        if (!labelName) {
            throw new Error("Expected labelName");
        }
        if (state.kind !== "update") {
            throw new Error("Expected update state");
        }

        editState = { kind: "submitting" };
        labelNameValidation = undefined;
        chosenColorValidation = undefined;

        const color = getIndexFromLabelColor(chosenColor);
        const { error, data } = await updateLabel({
            ...state.label,
            name: labelName,
            color,
        });
        if (data) {
            editState = { kind: "start" };
            onFinished();
            return;
        }
        if (error.code === 403) {
            const workspace =
                $currentWorkspace.value ?? $currentProject.value?.workspace;
            if (workspace === undefined) {
                throw new Error("Expected workspace");
            }
            await goto(
                getLogInWithNextUrl(getDashboardWorkspaceUrl(workspace)),
            );
            return;
        }
        if (error.code !== 400) {
            editState = {
                kind: "error",
                message: $_("dashboard.side-nav.filter-labels.errors.general"),
            };
            return;
        }
        labelNameValidation = error.details.name
            ? { ok: false, error: error.details.name }
            : undefined;
        chosenColorValidation = error.details.color
            ? { ok: false, error: error.details.color }
            : undefined;
        editState = {
            kind: "error",
            message:
                error.general ??
                $_("dashboard.side-nav.filter-labels.errors.update"),
        };
    }
</script>

<!-- all this px-4 bizniz is sub-optimal -->
<form
    class="flex flex-col gap-4 px-4"
    on:submit|preventDefault={state.kind === "create" ? create : update}
>
    <p>
        {#if state.kind === "update"}
            {$_("dashboard.side-nav.filter-labels.state.update", {
                values: { label: state.label.name },
            })}
        {:else}
            {$_("dashboard.side-nav.filter-labels.state.create")}
        {/if}
    </p>
    <div class="flex flex-col gap-4">
        <InputField
            style={{ inputType: "text" }}
            placeholder={state.kind === "update"
                ? $_(
                      "dashboard.side-nav.filter-labels.update-input.placeholder",
                  )
                : $_(
                      "dashboard.side-nav.filter-labels.create-input.placeholder",
                  )}
            label={state.kind === "update"
                ? $_("dashboard.side-nav.filter-labels.update-input.label")
                : $_("dashboard.side-nav.filter-labels.create-input.label")}
            name="label-name"
            bind:value={labelName}
            validation={labelNameValidation}
            required
        />
        <LabelRadio bind:chosenColor />
        {#if chosenColorValidation && !chosenColorValidation.ok}
            <p>{chosenColorValidation.error}</p>
        {/if}
    </div>
    {#if editState.kind === "error"}
        <p>
            {editState.message}
        </p>
    {/if}
    <div class="flex flex-row gap-4">
        <Button
            style={{ kind: "secondary" }}
            color="blue"
            size="medium"
            label={$_("dashboard.side-nav.filter-labels.cancel")}
            action={{
                kind: "button",
                action: onFinished,
                disabled: editState.kind === "submitting",
            }}
        />
        <Button
            style={{ kind: "primary" }}
            color="blue"
            size="medium"
            label={$_("dashboard.side-nav.filter-labels.save")}
            action={{ kind: "submit", disabled: !canSave }}
        />
    </div>
</form>
