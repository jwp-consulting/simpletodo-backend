<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import FilterLabelsClosed from "$lib/figma/navigation/side-nav/FilterLabelsClosed.svelte";
    import FilterTeamMembersClosed from "$lib/figma/navigation/side-nav/FilterTeamMembersClosed.svelte";
    import WorkspaceSelector from "$lib/figma/navigation/side-nav/WorkspaceSelector.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    import { selectProjectUuid, showFilters } from "$lib/stores/dashboard/ui";
    import { getDashboardProjectUrl } from "$lib/urls";
    import { getContext } from "svelte";
    import type { WsResource } from "$lib/types/stores";
    import type { ProjectDetail } from "$lib/types/workspace";

    const currentProject =
        getContext<WsResource<ProjectDetail>>("currentProject");
    import { currentWorkspace } from "$lib/stores/dashboard/workspace";

    $: workspace = $currentWorkspace.value ?? $currentProject.value?.workspace;
</script>

<nav class="inline-flex h-full flex-col items-center gap-12 bg-foreground p-4">
    <div class="flex flex-col items-center justify-between">
        <div class="flex flex-col items-center gap-12">
            <div
                class="flex flex-col items-center gap-6 border-b border-border pb-12"
            >
                <WorkspaceSelector {workspace} open={false} />
                <div class="flex flex-col items-center gap-6">
                    <div class="flex flex-col items-center gap-4">
                        {#if workspace?.projects}
                            {#each workspace.projects as project}
                                <SquovalIcon
                                    ariaLabel={$_(
                                        "dashboard.side-nav.projects.open-project",
                                        { values: { title: project.title } },
                                    )}
                                    icon="board"
                                    state="active"
                                    action={{
                                        kind: "a",
                                        href: getDashboardProjectUrl(project),
                                        onInteract: selectProjectUuid.bind(
                                            null,
                                            workspace.uuid,
                                            project.uuid,
                                        ),
                                    }}
                                />
                            {/each}
                        {/if}
                    </div>
                </div>
            </div>
            {#if workspace !== undefined && $showFilters}
                <div class="flex flex-col gap-8">
                    <div class="flex flex-col items-center gap-6">
                        <FilterTeamMembersClosed />
                        <FilterLabelsClosed />
                    </div>
                </div>
            {/if}
        </div>
    </div>
</nav>
