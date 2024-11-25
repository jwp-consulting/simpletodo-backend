<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import TabElement from "$lib/figma/buttons/TabElement.svelte";
    import type { SettingKind } from "$lib/types/dashboard";
    import type { WorkspaceDetail } from "$lib/types/workspace";
    import { getSettingsUrl } from "$lib/urls";
    import type { CurrentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import { getContext } from "svelte";

    const currentTeamMemberCan = getContext<CurrentTeamMemberCan>(
        "currentTeamMemberCan",
    );

    export let workspace: WorkspaceDetail;
    export let activeSetting: SettingKind;
</script>

<div class="flex flex-row flex-wrap">
    <TabElement
        href={getSettingsUrl(workspace, "index")}
        label={$_("workspace-settings.general.heading")}
        active={activeSetting === "index"}
    />
    <TabElement
        href={getSettingsUrl(workspace, "team-members")}
        label={$_("workspace-settings.team-members.heading")}
        active={activeSetting === "team-members"}
    />
    {#if $currentTeamMemberCan("read", "customer")}
        <TabElement
            href={getSettingsUrl(workspace, "billing")}
            label={$_("workspace-settings.billing.heading")}
            active={activeSetting === "billing"}
        />
    {/if}
    <TabElement
        href={getSettingsUrl(workspace, "quota")}
        label={$_("workspace-settings.quota.heading")}
        active={activeSetting === "quota"}
    />
    <div class="grow border-b-2 border-border" />
</div>
