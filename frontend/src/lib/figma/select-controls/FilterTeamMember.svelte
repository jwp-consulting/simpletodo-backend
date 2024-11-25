<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import Checkbox from "$lib/funabashi/select-controls/Checkbox.svelte";
    import type { TeamMemberSelectionInput } from "$lib/types/ui";
    import { getDisplayName } from "$lib/types/user";

    export let teamMemberSelectionInput: TeamMemberSelectionInput;
    export let active: boolean;
    export let count: number;

    export let onSelect: () => void;
    export let onDeselect: () => void;

    const id = crypto.randomUUID();
</script>

<div
    class="group flex w-full flex-row justify-between px-5 py-2 hover:bg-background"
>
    <div class="flex min-w-0 flex-row items-center gap-2">
        <div class="shrink-0">
            <Checkbox
                checked={active}
                disabled={false}
                contained={true}
                id="checkbox-{id}"
                {onSelect}
                {onDeselect}
            />
        </div>
        <div class="flex min-w-0 flex-row items-center gap-2">
            {#if teamMemberSelectionInput.kind === "teamMember"}
                <AvatarVariant
                    content={{
                        kind: "single",
                        user: teamMemberSelectionInput.teamMember.user,
                    }}
                    size="medium"
                />
            {:else}
                <AvatarVariant
                    content={{
                        kind: "single",
                    }}
                    size="medium"
                />
            {/if}
            <label class="text-regular min-w-0 truncate" for="checkbox-{id}">
                {#if teamMemberSelectionInput.kind === "unassigned"}
                    {$_("filter-team-member.assigned-nobody")}
                {:else if teamMemberSelectionInput.kind === "allTeamMembers"}
                    {$_("filter-team-member.all-users")}
                {:else if teamMemberSelectionInput.kind === "teamMember"}
                    {getDisplayName(teamMemberSelectionInput.teamMember.user)}
                {/if}
            </label>
        </div>
    </div>
    <div
        class="flex shrink-0 flex-row items-center gap-2 rounded-2.5xl bg-background px-2 py-0.5 text-primary group-hover:bg-foreground"
    >
        {count}
    </div>
</div>
