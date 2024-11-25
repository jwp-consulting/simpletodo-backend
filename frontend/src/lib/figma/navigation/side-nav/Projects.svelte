<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { Folder, Plus } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import SideNavMenuCategory from "$lib/figma/buttons/SideNavMenuCategory.svelte";
    import SelectProject from "$lib/figma/navigation/side-nav/SelectProject.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import {
        projectExpandOpen,
        toggleProjectExpandOpen,
    } from "$lib/stores/dashboard/ui";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";
    import type { ProjectDetailWorkspace } from "$lib/types/workspace";
    import { getArchiveUrl } from "$lib/urls";
    import type { CurrentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import { getContext } from "svelte";

    const currentTeamMemberCan = getContext<CurrentTeamMemberCan>(
        "currentTeamMemberCan",
    );

    export let workspace: ProjectDetailWorkspace;

    async function openCreateProject() {
        await openConstructiveOverlay({
            kind: "createProject",
            workspace,
        });
    }
</script>

<SideNavMenuCategory
    label={$_("dashboard.projects")}
    icon={Folder}
    open={$projectExpandOpen}
    on:click={toggleProjectExpandOpen}
    filtered={false}
/>
{#if $projectExpandOpen}
    <!-- TODO evaluate revmoing this shrink class here -->
    <div class="flex shrink flex-col">
        {#if workspace.projects.length === 0}
            <div class="flex flex-col gap-2 p-4">
                <p>
                    {$_("dashboard.side-nav.projects.empty.message")}
                </p>
                <p>
                    <Anchor
                        label={$_("dashboard.side-nav.projects.empty.archive")}
                        href={getArchiveUrl(workspace)}
                        size="normal"
                    />
                </p>
            </div>
        {:else}
            {#each workspace.projects as project (project.uuid)}
                <SelectProject {workspace} {project} />
            {/each}
        {/if}
    </div>
    {#if $currentTeamMemberCan("create", "project")}
        <ContextMenuButton
            label={$_("dashboard.create-project")}
            icon={Plus}
            color="primary"
            kind={{ kind: "button", action: openCreateProject }}
        />
    {/if}
{/if}
