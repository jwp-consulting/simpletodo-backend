<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023, 2024 JWP Consulting GK -->
<script lang="ts">
    import {
        ArrowDown,
        ArrowUp,
        Pencil,
        Selector,
        Trash,
        X,
    } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import {
        toggleSectionOpen,
        sectionClosed,
    } from "$lib/stores/dashboard/ui";
    import {
        openConstructiveOverlay,
        openDestructiveOverlay,
    } from "$lib/stores/globalUi";
    import type {
        ProjectDetail,
        ProjectDetailSection,
    } from "$lib/types/workspace";
    import { openApiClient } from "$lib/repository/util";
    import type { CurrentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import { getContext } from "svelte";

    const currentTeamMemberCan = getContext<CurrentTeamMemberCan>(
        "currentTeamMemberCan",
    );

    export let project: ProjectDetail;
    export let section: ProjectDetailSection;

    // RPC
    async function moveSection(
        { uuid: section_uuid }: ProjectDetailSection,
        order: number,
    ) {
        const { error } = await openApiClient.POST(
            "/workspace/section/{section_uuid}/move",
            { params: { path: { section_uuid } }, body: { order } },
        );
        if (error) {
            throw new Error("Could not move section");
        }
    }

    let closed: boolean;
    $: {
        closed = $sectionClosed.has(section.uuid);
    }

    let sections: readonly ProjectDetailSection[] = [];
    $: sections = project.sections;

    // TODO this might have to be refactored to check if previous or next section exists

    let sectionIndex: number | undefined;
    let previousIndex: number | undefined;
    let nextIndex: number | undefined;
    let previousSection: ProjectDetailSection | undefined;
    let nextSection: ProjectDetailSection | undefined;

    $: {
        sectionIndex = sections.findIndex(
            (s: ProjectDetailSection) => s.uuid == section.uuid,
        );
        previousIndex = sectionIndex > 0 ? sectionIndex - 1 : undefined;
        nextIndex =
            sectionIndex < sections.length - 1 ? sectionIndex + 1 : undefined;
        previousSection =
            previousIndex !== undefined ? sections[previousIndex] : undefined;
        nextSection =
            nextIndex !== undefined ? sections[nextIndex] : undefined;
    }

    async function updateSection() {
        await openConstructiveOverlay({
            kind: "updateSection",
            section,
        });
    }

    async function deleteSection() {
        await openDestructiveOverlay({
            kind: "deleteSection",
            section,
        });
        const { error } = await openApiClient.DELETE(
            "/workspace/section/{section_uuid}",
            { params: { path: { section_uuid: section.uuid } } },
        );
        if (error) {
            throw new Error("Could not move section");
        }
    }
</script>

<Layout>
    <ContextMenuButton
        kind={{
            kind: "button",
            action: toggleSectionOpen.bind(null, section.uuid),
        }}
        label={closed
            ? $_("overlay.context-menu.section.expand-section")
            : $_("overlay.context-menu.section.collapse-section")}
        icon={closed ? Selector : X}
    />
    {#if $currentTeamMemberCan("update", "section")}
        {#if previousSection}
            <ContextMenuButton
                kind={{
                    kind: "button",
                    action: moveSection.bind(
                        null,
                        section,
                        previousSection._order,
                    ),
                }}
                label={$_("overlay.context-menu.section.switch-previous")}
                icon={ArrowUp}
            />
        {/if}
        {#if nextSection}
            <ContextMenuButton
                kind={{
                    kind: "button",
                    action: moveSection.bind(
                        null,
                        section,
                        nextSection._order,
                    ),
                }}
                label={$_("overlay.context-menu.section.switch-next")}
                icon={ArrowDown}
            />
        {/if}
        <ContextMenuButton
            kind={{
                kind: "button",
                action: updateSection,
            }}
            label={$_("overlay.context-menu.section.edit-title")}
            icon={Pencil}
        />
    {/if}
    {#if $currentTeamMemberCan("delete", "section")}
        <ContextMenuButton
            kind={{
                kind: "button",
                action: deleteSection,
            }}
            label={$_("overlay.context-menu.section.delete-section")}
            icon={Trash}
            color="destructive"
        />
    {/if}
</Layout>
