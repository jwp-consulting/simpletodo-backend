<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { X } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import TeamMemberCard from "$lib/figma/screens/workspace-settings/TeamMemberCard.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { InputFieldValidation } from "$lib/funabashi/types";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { currentWorkspace } from "$lib/stores/dashboard/workspace";
    import { currentTeamMembers } from "$lib/stores/dashboard/teamMember";
    import type { FormViewState } from "$lib/types/ui";
    import { coerceIsoDate } from "$lib/utils/date";

    import type { PageData } from "./$types";
    import { openApiClient } from "$lib/repository/util";
    import Loading from "$lib/components/Loading.svelte";
    import type { CurrentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import { getContext } from "svelte";

    const currentTeamMemberCan = getContext<CurrentTeamMemberCan>(
        "currentTeamMemberCan",
    );

    export let data: PageData;

    $: workspace = $currentWorkspace.or(data.workspace);

    async function uninvite(email: string) {
        const { error } = await openApiClient.POST(
            "/workspace/workspace/{workspace_uuid}/uninvite-team-member",
            {
                params: { path: { workspace_uuid: workspace.uuid } },
                body: { email },
            },
        );
        if (error) {
            console.error(error);
            throw new Error("Could not uninvite user");
        }
    }

    // Invite form
    let inviteEmail: string | undefined;
    let inviteEmailValidation: InputFieldValidation | undefined = undefined;

    let state: FormViewState = { kind: "start" };

    async function performInviteUser() {
        if (inviteEmail === undefined) {
            throw new Error("No email");
        }
        state = { kind: "submitting" };
        const { error, data } = await openApiClient.POST(
            "/workspace/workspace/{workspace_uuid}/invite-team-member",
            {
                params: { path: { workspace_uuid: workspace.uuid } },
                body: { email: inviteEmail },
            },
        );
        if (data) {
            state = { kind: "start" };
            inviteEmail = undefined;
            inviteEmailValidation = undefined;
            return;
        }
        if (error.code !== 400) {
            state = {
                kind: "error",
                message: $_(
                    "workspace-settings.team-members.invite.error.general",
                ),
            };
            return;
        }
        const { details } = error;
        inviteEmailValidation = details.email
            ? {
                  ok: false,
                  error: details.email,
              }
            : {
                  ok: true,
                  result: $_(
                      "workspace-settings.team-members.invite.form.email.validation.ok",
                  ),
              };
        state = {
            kind: "error",
            message: inviteEmailValidation.ok
                ? $_("workspace-settings.team-members.invite.error.general")
                : $_("workspace-settings.team-members.invite.error.field"),
        };
    }
</script>

<svelte:head>
    <title
        >{$_("workspace-settings.team-members.title", {
            values: { title: workspace.title },
        })}</title
    >
</svelte:head>

{#if $currentTeamMemberCan("create", "teamMemberInvite")}
    <form
        class="flex flex-col gap-4"
        on:submit|preventDefault={performInviteUser}
    >
        <InputField
            name="project-name"
            bind:value={inviteEmail}
            label={$_(
                "workspace-settings.team-members.invite.form.email.label",
            )}
            placeholder={$_(
                "workspace-settings.team-members.invite.form.email.placeholder",
            )}
            style={{ inputType: "email" }}
            required
            validation={inviteEmailValidation}
        />
        {#if state.kind === "error"}
            <p>{state.message}</p>
        {/if}
        <Button
            action={{ kind: "submit", disabled: state.kind === "submitting" }}
            label={$_("workspace-settings.team-members.invite.invite")}
            style={{ kind: "primary" }}
            size="medium"
            color="blue"
        />
    </form>
{/if}
<section class="flex flex-col gap-4">
    <h2 class="text-xl font-bold">
        {$_("workspace-settings.team-members.heading")}
    </h2>
    {#if $currentTeamMembers}
        <table class="grid w-full grid-cols-4 items-center gap-y-4">
            <thead class="contents">
                <tr class="contents">
                    <th
                        class="col-span-2 border-b border-border text-left font-bold"
                        >{$_(
                            "workspace-settings.team-members.team-member",
                        )}</th
                    >
                    <th class="border-b border-border text-left font-bold"
                        >{$_("workspace-settings.team-members.role")}</th
                    >
                    <th class="border-b border-border text-left font-bold"
                        >{$_(
                            "workspace-settings.team-members.actions.action",
                        )}</th
                    >
                </tr>
            </thead>
            <tbody class="contents">
                {#each $currentTeamMembers as teamMember}
                    <TeamMemberCard {teamMember} />
                {:else}
                    <td class="col-span-4">
                        {$_(
                            "workspace-settings.team-members.no-team-members-found",
                        )}
                    </td>
                {/each}
            </tbody>
        </table>
    {:else}
        <Loading />
    {/if}
</section>
<section class="flex flex-col gap-4">
    <h2 class="text-xl font-bold">
        {$_("workspace-settings.team-members.invites.title")}
    </h2>
    <table class="grid w-full grid-cols-4 items-center gap-y-4">
        <thead class="contents">
            <tr class="contents">
                <th
                    class="col-span-2 border-b border-border text-left font-bold"
                    >{$_("workspace-settings.team-members.invites.email")}</th
                >
                <th class="border-b border-border text-left font-bold"
                    >{$_("workspace-settings.team-members.invites.date")}</th
                >
                <th class="border-b border-border text-left font-bold"
                    >{$_("workspace-settings.team-members.actions.action")}</th
                >
            </tr>
        </thead>
        <tbody class="contents">
            {#each workspace.team_member_invites as invite}
                <td class="col-span-2 overflow-x-auto">
                    {invite.email}
                </td>
                <td>{coerceIsoDate(invite.created)}</td>
                <td
                    ><Button
                        style={{
                            kind: "tertiary",
                            icon: { position: "left", icon: X },
                        }}
                        color="red"
                        action={{
                            kind: "button",
                            action: uninvite.bind(null, invite.email),
                        }}
                        size="medium"
                        label={$_(
                            "workspace-settings.team-members.actions.uninvite",
                        )}
                        grow={false}
                    />
                </td>
            {:else}
                <td class="col-span-3">
                    {$_("workspace-settings.team-members.invites.empty")}
                </td>
            {/each}
        </tbody>
    </table>
</section>
<hr />
<section class="flex flex-col gap-2">
    <strong>{$_("workspace-settings.team-members.help.title")}</strong>
    <ul class="flex list-inside list-disc flex-col gap-2">
        <li>
            <Anchor
                href="/help/team-members"
                label={$_(
                    "workspace-settings.team-members.help.about-team-members",
                )}
                size="normal"
                openBlank
            />
        </li>
        <li>
            <Anchor
                href="/help/roles"
                label={$_("workspace-settings.team-members.help.about-roles")}
                size="normal"
                openBlank
            />
        </li>
    </ul>
</section>
