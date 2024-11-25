<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import { updateTask } from "$lib/repository/workspace/task";
    import { createTeamMemberAssignment } from "$lib/stores/dashboard/teamMemberAssignment";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType, FormViewState } from "$lib/types/ui";
    import { getDisplayName } from "$lib/types/user";
    import type { ProjectDetailTask } from "$lib/types/workspace";
    import { cloneMutable } from "$lib/utils/type";
    import type { CurrentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import { getContext } from "svelte";

    const currentTeamMemberCan = getContext<CurrentTeamMemberCan>(
        "currentTeamMemberCan",
    );

    export let task: ProjectDetailTask;

    let userPickerBtnRef: HTMLElement;
    let state: FormViewState = { kind: "start" };

    $: teamMemberAssignment = createTeamMemberAssignment(task);

    $: assignee = $teamMemberAssignment;

    async function openUserPicker() {
        const contextMenuType: ContextMenuType = {
            kind: "updateTeamMember",
            teamMemberAssignment,
        };
        await openContextMenu(contextMenuType, userPickerBtnRef);
        const teamMember = $teamMemberAssignment;
        // XXX need to investigate what happens when sub tasks change while
        // the user picker is open. Possibly, a sub task can be deleted if
        // it is added
        state = { kind: "submitting" };
        const { error } = await updateTask(task, {
            ...cloneMutable(task),
            assignee: teamMember,
        });
        if (error) {
            state = {
                kind: "error",
                message: $_("dashboard.task-card.assign-team-member.error"),
            };
        } else {
            state = { kind: "start" };
        }
    }

    $: canUpdate = $currentTeamMemberCan("update", "task");
</script>

{#if state.kind === "submitting"}
    {$_("dashboard.task-card.assign-team-member.saving")}
{:else}
    <button
        bind:this={userPickerBtnRef}
        on:click|preventDefault={canUpdate ? openUserPicker : undefined}
    >
        <AvatarVariant
            content={{ kind: "single", user: assignee?.user }}
            size="medium"
        />
        <div class="sr-only">
            {#if assignee}
                {$_("dashboard.task-card.assign-team-member.assigned", {
                    values: { name: getDisplayName(assignee.user) },
                })}
            {:else}
                {$_("dashboard.task-card.assign-team-member.not-assigned")}
            {/if}
        </div>
    </button>
{/if}
