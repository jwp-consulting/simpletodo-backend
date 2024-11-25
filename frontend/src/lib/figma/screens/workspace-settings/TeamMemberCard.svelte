<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { X } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import { openDestructiveOverlay } from "$lib/stores/globalUi";
    import { teamMemberRoles } from "$lib/types/teamMemberRole";
    import type { EditableViewState } from "$lib/types/ui";
    import { getDisplayName } from "$lib/types/user";
    import type {
        TeamMemberRole,
        WorkspaceDetailTeamMember,
    } from "$lib/types/workspace";
    import { getMessageNameForRole } from "$lib/utils/i18n";
    import { openApiClient } from "$lib/repository/util";
    import type {
        CurrentTeamMember,
        CurrentTeamMemberCan,
    } from "$lib/stores/dashboard/teamMember";
    import { getContext } from "svelte";

    const currentTeamMember =
        getContext<CurrentTeamMember>("currentTeamMember");
    const currentTeamMemberCan = getContext<CurrentTeamMemberCan>(
        "currentTeamMemberCan",
    );

    export let teamMember: WorkspaceDetailTeamMember;

    let preferredName: string;
    $: preferredName = getDisplayName(teamMember.user);
    let jobTitle: string;
    $: jobTitle =
        teamMember.job_title ??
        $_("workspace-settings.team-members.no-job-title");
    let role: string;
    $: role = getMessageNameForRole($_, teamMember.role);

    let mode: EditableViewState = { kind: "viewing" };

    let roleSelected: TeamMemberRole | undefined = undefined;

    async function removeUser() {
        await openDestructiveOverlay({
            kind: "deleteTeamMember",
            teamMember,
        });
        const { error } = await openApiClient.DELETE(
            "/workspace/team-member/{team_member_uuid}",
            { params: { path: { team_member_uuid: teamMember.uuid } } },
        );
        if (error) {
            throw new Error("Could not remove user");
        }
    }

    function startEdit() {
        mode = { kind: "editing" };
        roleSelected = teamMember.role;
    }

    async function changeRole() {
        if (roleSelected === undefined) {
            throw new Error("Expected roleSelected");
        }
        console.debug(roleSelected);
        mode = { kind: "saving" };
        const { error } = await openApiClient.PUT(
            "/workspace/team-member/{team_member_uuid}",
            {
                params: { path: { team_member_uuid: teamMember.uuid } },
                body: {
                    role: roleSelected,
                },
            },
        );
        if (error) {
            throw new Error("Could not change role");
        }
        mode = { kind: "viewing" };
    }
    $: isCurrentUser = teamMember.uuid === $currentTeamMember?.uuid;
</script>

<tr class="contents">
    <td class="col-span-2 flex flex-row items-center gap-2">
        <AvatarVariant
            content={{ kind: "single", user: teamMember.user }}
            size="medium"
        />
        <div class="flex flex-col gap-1">
            <span class="font-bold">
                {preferredName}
            </span>
            <span>{jobTitle}</span>
        </div>
    </td>
    <td class="flex flex-row items-center gap-2">
        {#if mode.kind === "viewing"}
            <span>
                {role}
            </span>
            {#if $currentTeamMemberCan("update", "teamMember")}
                <CircleIcon
                    icon="edit"
                    size="medium"
                    ariaLabel={isCurrentUser
                        ? $_("workspace-settings.team-members.edit-role.self")
                        : $_(
                              "workspace-settings.team-members.edit-role.label",
                          )}
                    action={{
                        kind: "button",
                        action: startEdit,
                        disabled: isCurrentUser,
                    }}
                />
            {/if}
        {:else if mode.kind === "editing"}
            <select bind:value={roleSelected} on:change={changeRole}>
                {#each teamMemberRoles as teamMemberRole}
                    <option value={teamMemberRole}>
                        {getMessageNameForRole($_, teamMemberRole)}
                    </option>
                {/each}
            </select>
        {:else}
            {$_("workspace-settings.team-members.edit-role.saving")}
        {/if}
    </td>
    <td
        >{#if $currentTeamMemberCan("delete", "teamMember")}<Button
                label={$_("workspace-settings.team-members.actions.remove")}
                action={{
                    kind: "button",
                    action: removeUser,
                    disabled: isCurrentUser,
                }}
                style={{
                    kind: "tertiary",
                    icon: { position: "left", icon: X },
                }}
                color="red"
                size="medium"
            />{/if}</td
    >
</tr>
