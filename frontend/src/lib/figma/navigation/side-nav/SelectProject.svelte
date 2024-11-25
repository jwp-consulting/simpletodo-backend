<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { Folder } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { _ } from "svelte-i18n";

    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import type { WsResource } from "$lib/types/stores";
    import type { ProjectDetail } from "$lib/types/workspace";

    const currentProject =
        getContext<WsResource<ProjectDetail>>("currentProject");
    import { openContextMenu } from "$lib/stores/globalUi";
    import type {
        WorkspaceDetail,
        WorkspaceDetailProject,
    } from "$lib/types/workspace";
    import { getDashboardProjectUrl } from "$lib/urls";
    import { selectProjectUuid } from "$lib/stores/dashboard/ui";
    import type { CurrentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import { getContext } from "svelte";

    const currentTeamMemberCan = getContext<CurrentTeamMemberCan>(
        "currentTeamMemberCan",
    );

    $: currentProjectUuid = $currentProject.value?.uuid;

    export let project: WorkspaceDetailProject;
    export let workspace: WorkspaceDetail;

    let buttonRef: HTMLElement;
    let contextMenuOpen = false;

    async function toggleMenu() {
        contextMenuOpen = true;
        // TODO: When the context menu is open, we should indicate that it
        // belongs to a certain board by highlighting the board in blue (using
        // the hover color)
        try {
            await openContextMenu(
                {
                    kind: "project",
                    workspace,
                    project,
                },
                buttonRef,
            );
        } finally {
            contextMenuOpen = false;
        }
    }
</script>

<a
    class="group block flex w-full flex-row justify-between gap-1 px-4 py-1 hover:bg-base-200"
    class:bg-base-200={contextMenuOpen}
    href={getDashboardProjectUrl(project)}
    on:click={() => selectProjectUuid(workspace.uuid, project.uuid)}
>
    <div class="flex min-w-0 flex-row items-center gap-2">
        <div
            class={`rounded-md p-1 ${
                project.uuid === currentProjectUuid ? "bg-primary-focus" : ""
            }`}
        >
            <Icon
                src={Folder}
                theme="outline"
                class={`h-4 w-4 ${
                    project.uuid === currentProjectUuid ? "text-base-100" : ""
                }`}
            />
        </div>
        <div class="line-clamp-1 min-w-0 font-bold">
            {project.title}
        </div>
    </div>
    {#if $currentTeamMemberCan("update", "project")}
        <div class="shrink-0" bind:this={buttonRef}>
            <CircleIcon
                size="medium"
                icon="ellipsis"
                action={{ kind: "button", action: toggleMenu }}
                ariaLabel={$_("dashboard.side-nav.projects.context-menu")}
            />
        </div>
    {/if}
</a>
