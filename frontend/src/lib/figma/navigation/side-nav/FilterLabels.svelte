<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { Tag, Plus } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import SideNavMenuCategory from "$lib/figma/buttons/SideNavMenuCategory.svelte";
    import FilterLabelMenu from "$lib/figma/composites/FilterLabelMenu.svelte";
    import type { FilterLabelMenuState } from "$lib/figma/types";
    import {
        labelExpandOpen,
        toggleLabelDropdownClosedNavOpen,
    } from "$lib/stores/dashboard/ui";
    import { selectedLabels } from "$lib/stores/dashboard/labelFilter";
    import type { Label } from "$lib/types/workspace";

    import CreateOrUpdateLabel from "./filter-labels/CreateOrUpdateLabel.svelte";
    import type { CurrentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import { getContext } from "svelte";

    const currentTeamMemberCan = getContext<CurrentTeamMemberCan>(
        "currentTeamMemberCan",
    );

    // Still exporting this one for better testability in storybook
    // TODO or perhaps we can refactor the form to a new component?
    export let state: FilterLabelMenuState = { kind: "list" };

    function startCreateLabel() {
        state = { kind: "create" };
    }

    function startUpdate(label: Label) {
        state = { kind: "update", label };
    }

    function onCreateOrUpdateFinish() {
        state = { kind: "list" };
    }
</script>

<SideNavMenuCategory
    label={$_("dashboard.side-nav.filter-labels.title")}
    icon={Tag}
    on:click={toggleLabelDropdownClosedNavOpen}
    open={$labelExpandOpen}
    filtered={$selectedLabels.kind !== "allLabels"}
/>
{#if $labelExpandOpen}
    {#if state.kind === "list"}
        <FilterLabelMenu mode={{ kind: "filter", startUpdate }} />
        <!-- Some left padding issues here, not aligned with the rest above -->
        {#if $currentTeamMemberCan("create", "label")}
            <ContextMenuButton
                label={$_("dashboard.side-nav.filter-labels.create-new-label")}
                icon={Plus}
                color="primary"
                kind={{
                    kind: "button",
                    action: startCreateLabel,
                }}
            />
        {/if}
    {:else}
        <CreateOrUpdateLabel onFinished={onCreateOrUpdateFinish} {state} />
    {/if}
{/if}
