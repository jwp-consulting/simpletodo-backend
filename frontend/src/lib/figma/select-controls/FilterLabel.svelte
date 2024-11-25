<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import SelectLabelCheckBox from "$lib/figma/select-controls/SelectLabelCheckBox.svelte";
    import type { SelectLabel } from "$lib/figma/types";
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import { openDestructiveOverlay } from "$lib/stores/globalUi";
    import { openApiClient } from "$lib/repository/util";
    import type { CurrentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import { getContext } from "svelte";

    const currentTeamMemberCan = getContext<CurrentTeamMemberCan>(
        "currentTeamMemberCan",
    );

    export let label: SelectLabel;
    export let checked: boolean;

    export let onCheck: () => void;
    export let onUncheck: () => void;
    export let onEdit: (() => void) | undefined = undefined;

    const id = crypto.randomUUID();

    async function onDelete() {
        if (label.kind !== "label") {
            throw new Error("Expected label");
        }
        const {
            label: l,
            label: { uuid: label_uuid },
        } = label;
        await openDestructiveOverlay({ kind: "deleteLabel", label: l });
        const { error } = await openApiClient.DELETE(
            "/workspace/label/{label_uuid}",
            { params: { path: { label_uuid } } },
        );
        if (error) {
            throw new Error("Could not delete label");
        }
    }
</script>

<div
    class="group flex w-full flex-row items-center justify-between px-5 hover:bg-background"
>
    <div class="flex min-w-0 flex-row items-center gap-2">
        <SelectLabelCheckBox
            id="checkbox-{id}"
            {label}
            bind:checked
            {onCheck}
            {onUncheck}
        />
        <label class="text-regular truncate" for="checkbox-{id}">
            {#if label.kind === "allLabels"}
                {$_("filter-label.all")}
            {:else if label.kind === "noLabel"}
                {$_("filter-label.none")}
            {:else if label.kind === "label"}
                {label.label.name}
            {/if}
        </label>
    </div>
    <div class="flex flex-row items-center gap-2">
        {#if label.kind === "label" && onEdit}
            <CircleIcon
                size="medium"
                icon="edit"
                action={{
                    kind: "button",
                    action: onEdit,
                    disabled: !$currentTeamMemberCan("update", "label"),
                }}
                ariaLabel={$_("filter-label.edit-label")}
            />
            <CircleIcon
                size="medium"
                icon="delete"
                action={{
                    kind: "button",
                    action: onDelete,
                    disabled: !$currentTeamMemberCan("delete", "label"),
                }}
                ariaLabel={$_("filter-label.delete-label")}
            />
        {/if}
    </div>
</div>
