<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { Plus, User } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import SideNavMenuCategory from "$lib/figma/buttons/SideNavMenuCategory.svelte";
    import FilterTeamMember from "$lib/figma/composites/FilterTeamMember.svelte";
    import { toggleUserExpandOpen } from "$lib/stores/dashboard/ui";
    import { selectedTeamMember } from "$lib/stores/dashboard/teamMemberFilter";
    import { currentWorkspace } from "$lib/stores/dashboard/workspace";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import { getSettingsUrl } from "$lib/urls";
    import type { CurrentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import { getContext } from "svelte";
    import type { Readable } from "svelte/store";

    const userExpandOpen = getContext<Readable<boolean>>("userExpandOpen");
    const currentTeamMemberCan = getContext<CurrentTeamMemberCan>(
        "currentTeamMemberCan",
    );
</script>

<SideNavMenuCategory
    label={$_("dashboard.side-nav.filter-team-members.title")}
    icon={User}
    open={$userExpandOpen}
    on:click={toggleUserExpandOpen}
    filtered={$selectedTeamMember.kind !== "allTeamMembers"}
/>
{#if $userExpandOpen}
    <!-- TODO evaluate removing this shrink class here -->
    <div class="shrink">
        <FilterTeamMember mode={{ kind: "filter" }} />
        {#if $currentWorkspace.value && $currentTeamMemberCan("create", "teamMemberInvite")}
            <ContextMenuButton
                kind={{
                    kind: "a",
                    href: getSettingsUrl(
                        $currentWorkspace.value,
                        "team-members",
                    ),
                }}
                icon={Plus}
                color="primary"
                label={$_("dashboard.side-nav.filter-team-members.add")}
            />
        {/if}
    </div>
{/if}
