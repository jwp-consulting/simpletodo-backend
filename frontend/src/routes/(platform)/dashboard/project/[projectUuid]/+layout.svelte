<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { Search } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { ProjectDetailSection } from "$lib/types/workspace";
    import { getProjectSearchUrl } from "$lib/urls/dashboard";
    import type { LayoutData } from "./$types";
    import { getContext } from "svelte";
    import type { WsResource } from "$lib/types/stores";
    import type { ProjectDetail } from "$lib/types/workspace";

    const currentProject =
        getContext<WsResource<ProjectDetail>>("currentProject");
    export let data: LayoutData;

    currentProject
        .loadUuid(data.project.uuid)
        .catch((e: unknown) => console.error(e));

    $: project = $currentProject.value;
    let searchInput: string | undefined = undefined;

    $: canSearch = searchInput !== undefined;
    $: projectHasTasks =
        project &&
        project.sections.some((s: ProjectDetailSection) => s.tasks.length > 0);
</script>

<main class="flex h-full flex-col items-center gap-4 bg-background py-4">
    {#if project && projectHasTasks}
        <form
            role="search"
            action={getProjectSearchUrl(project)}
            class="flex w-full max-w-md flex-col gap-2 rounded-xl bg-foreground px-4 py-4"
        >
            <!-- XXX definitely not ideal, placeholder will disappear after input -->
            <InputField
                style={{ inputType: "search" }}
                label={$_("dashboard.search-task.input.label")}
                placeholder={$_("dashboard.search-task.input.placeholder")}
                name="search"
                bind:value={searchInput}
                showClearButton={false}
                required
            />
            <Button
                label={$_("dashboard.search-task.button")}
                action={{ kind: "submit", disabled: !canSearch }}
                style={{
                    kind: "tertiary",
                    icon: { position: "left", icon: Search },
                }}
                size="medium"
                color="blue"
                grow={false}
            />
        </form>
    {/if}
    <!-- shared layout for project and search results -->
    <div class="flex w-full grow flex-col gap-4 md:p-2">
        <slot />
    </div>
</main>
