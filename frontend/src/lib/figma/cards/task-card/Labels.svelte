<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    // This is a partial used inside TaskCard
    // The label picker is TODO
    import { _ } from "svelte-i18n";

    import LabelPill from "$lib/figma/cards/task-card/LabelPill.svelte";
    import { updateTask } from "$lib/repository/workspace/task";
    import { createLabelAssignment } from "$lib/stores/dashboard/labelAssignment";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { LabelAssignment } from "$lib/types/stores";
    import type { ContextMenuType, FormViewState } from "$lib/types/ui";
    import type { ProjectDetailTask } from "$lib/types/workspace";
    import { cloneMutable } from "$lib/utils/type";
    import { getContext } from "svelte";
    import type { CurrentTeamMemberCan } from "$lib/stores/dashboard/teamMember";

    const currentTeamMemberCan = getContext<CurrentTeamMemberCan>(
        "currentTeamMemberCan",
    );

    export let task: ProjectDetailTask;

    let state: FormViewState = { kind: "start" };
    let labelPickerOpen = false;
    let labelAssignment: LabelAssignment;

    $: {
        if (!labelPickerOpen) {
            labelAssignment = createLabelAssignment(task);
        }
    }

    $: labels = $labelAssignment;

    async function openLabelPicker(event: MouseEvent) {
        labelPickerOpen = true;
        const anchor = event.target;
        if (!(anchor instanceof HTMLElement)) {
            throw new Error("Expected HTMLElement");
        }
        const contextMenuType: ContextMenuType = {
            kind: "updateLabel",
            labelAssignment,
        };
        // By locking labelAssignment with labelPickerOpen, we prevent the
        // following race condition from happening:
        // 1. update task 1's labels using the label picker
        // 2. while the update request is stil happening, open task 2's label
        // picker
        // 3. wait for task 1's request to finish - the project will
        // re-render
        // 4. click on any label, it the labels shown in the task card
        // will not refresh
        // Reason: labelAssignment is recreated (as a reactive dependency of
        // task). When we arrive in labels = $labelAssignment, we are
        // retrieving the newly created labelAssignment store's values.
        // Mitigation ideas:
        // 1. Lock the dashboard until the label is updated
        // 2. Ensure we don't recreate labelAssignment (what is a component
        // lifecycle in Svelte anyway?! Research)
        // TODO: Think on it
        try {
            await openContextMenu(contextMenuType, anchor);

            const labels = $labelAssignment;
            // TODO skip update when no changes detected
            state = { kind: "submitting" };
            const { error } = await updateTask(task, {
                ...cloneMutable(task),
                labels,
            });
            if (error) {
                state = {
                    kind: "error",
                    message: $_("dashboard.task-card.add-label.error"),
                };
            } else {
                state = { kind: "start" };
            }
        } finally {
            labelPickerOpen = false;
        }
        // TODO There is a brief flash after updateTask finishes, the task is
        // reloaded and labelAssignment is recreated
    }

    $: canUpdate = $currentTeamMemberCan("update", "taskLabel");
</script>

{#if state.kind === "submitting"}
    {$_("dashboard.task-card.add-label.saving")}
{:else if labels.length}
    <div
        class="flex w-full flex-row items-center justify-start gap-1 self-start overflow-x-auto"
    >
        {#each labels as label}
            <LabelPill
                {label}
                action={canUpdate ? openLabelPicker : undefined}
            />
        {/each}
    </div>
{:else if canUpdate}
    <button
        class="flex flex-row items-center self-start rounded-full px-4 py-1 font-bold text-primary outline-dashed outline-1 outline-primary focus:outline focus:outline-inherit"
        on:click|preventDefault={openLabelPicker}
    >
        {$_("dashboard.task-card.add-label.label")}</button
    >
{:else}
    <span />
{/if}
