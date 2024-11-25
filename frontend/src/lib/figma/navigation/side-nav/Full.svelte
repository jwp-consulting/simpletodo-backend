<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import FilterLabels from "$lib/figma/navigation/side-nav/FilterLabels.svelte";
    import FilterTeamMembers from "$lib/figma/navigation/side-nav/FilterTeamMembers.svelte";
    import Projects from "$lib/figma/navigation/side-nav/Projects.svelte";
    import WorkspaceSelector from "$lib/figma/navigation/side-nav/WorkspaceSelector.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { getContext } from "svelte";
    import type { WsResource } from "$lib/types/stores";
    import type { ProjectDetail } from "$lib/types/workspace";

    const showFilters = getContext<Readable<boolean>>("showFilters");

    const currentProject =
        getContext<WsResource<ProjectDetail>>("currentProject");
    import { currentWorkspace } from "$lib/stores/dashboard/workspace";
    import type { Readable } from "svelte/store";

    $: workspace = $currentWorkspace.value ?? $currentProject.value?.workspace;
</script>

<!-- XXX temporary fix to alleviate long side nav inside mobile menu -->
<nav class="flex flex-col py-4">
    <WorkspaceSelector {workspace} open={true} />
    {#if workspace}
        {#if workspace.quota.workspace_status === "trial"}
            <p class="px-4">
                <strong>
                    {$_("dashboard.side-nav.quota.status.trial.label")}
                </strong>
                <Anchor
                    label={$_("dashboard.side-nav.quota.status.trial.help")}
                    href="/help/trial"
                    size="normal"
                    openBlank
                />
            </p>
        {:else if workspace.quota.workspace_status === "inactive"}
            <p class="px-4">
                <strong>
                    {$_("dashboard.side-nav.quota.status.inactive.label")}
                </strong>
                <Anchor
                    label={$_("dashboard.side-nav.quota.status.inactive.help")}
                    href="/help/billing"
                    size="normal"
                    openBlank
                />
            </p>
        {/if}
        <div class="flex flex-col">
            <Projects {workspace} />
            {#if $showFilters}
                <FilterTeamMembers />
                <FilterLabels />
            {/if}
        </div>
    {:else}
        <div class="flex flex-col gap-4 px-4">
            <p class="font-bold">
                {$_("dashboard.side-nav.no-workspace.title")}
            </p>
            <p>
                {$_("dashboard.side-nav.no-workspace.message")}
            </p>
        </div>
    {/if}
</nav>
