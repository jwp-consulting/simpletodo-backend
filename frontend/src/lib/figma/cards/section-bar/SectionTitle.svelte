<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { ChevronDown, ChevronRight, Plus } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    import { toggleSectionOpen } from "$lib/stores/dashboard/ui";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType } from "$lib/types/ui";
    import type {
        ProjectDetail,
        ProjectDetailSection,
    } from "$lib/types/workspace";
    import { getNewTaskUrl } from "$lib/urls";
    import type { CurrentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import { getContext } from "svelte";

    const currentTeamMemberCan = getContext<CurrentTeamMemberCan>(
        "currentTeamMemberCan",
    );

    export let project: ProjectDetail;
    export let section: ProjectDetailSection;
    export let open: boolean;

    const { uuid } = section;
    $: toggleOpen = toggleSectionOpen.bind(null, uuid);
    let dropDownMenuBtnRef: HTMLElement;

    async function openDropDownMenu() {
        const contextMenuType: ContextMenuType = {
            kind: "section",
            project,
            section,
        };
        await openContextMenu(contextMenuType, dropDownMenuBtnRef);
    }
</script>

<header
    class="sticky top-0 flex w-full flex-row items-center justify-between bg-foreground px-4 py-2"
>
    <div
        data-figma-name="Section header"
        class="flex min-w-0 shrink flex-row gap-4 text-base-content"
    >
        <button on:click={toggleOpen}>
            <Icon
                src={open ? ChevronDown : ChevronRight}
                class="h-6 w-6"
                theme="outline"
            />
            <div class="sr-only">
                {open
                    ? $_("dashboard.section.collapse.close")
                    : $_("dashboard.section.collapse.open")}
            </div>
        </button>
        <h1 class="line-clamp-1 min-w-0 shrink font-bold">
            {section.title}
        </h1>
    </div>
    <div
        class="flex shrink-0 flex-row items-center gap-1"
        data-figma-name="Right side"
    >
        {#if $currentTeamMemberCan("create", "task")}
            <Button
                action={{
                    kind: "a",
                    href: getNewTaskUrl(section),
                }}
                style={{
                    kind: "tertiary",
                    icon: { position: "left", icon: Plus },
                }}
                size="medium"
                color="blue"
                label={$_("dashboard.section.add-task")}
            />
        {/if}
        <div bind:this={dropDownMenuBtnRef}>
            <SquovalIcon
                ariaLabel={$_("dashboard.section.open-context-menu")}
                icon="ellipsis"
                state="active"
                active={false}
                action={{ kind: "button", action: openDropDownMenu }}
            />
        </div>
    </div>
</header>
