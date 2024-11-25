<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import TaskCard from "$lib/figma/cards/TaskCard.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { getDashboardProjectUrl } from "$lib/urls";

    import type { PageData } from "./$types";
    import { getContext } from "svelte";
    import type { WsResource } from "$lib/types/stores";
    import type { ProjectDetail } from "$lib/types/workspace";

    const currentProject =
        getContext<WsResource<ProjectDetail>>("currentProject");

    export let data: PageData;
    $: project = $currentProject.value;
    $: backUrl = project ? getDashboardProjectUrl(project) : undefined;
</script>

{#if data.tasks.length}
    <div class="flex flex-col gap-6 bg-foreground px-4 pb-6 pt-4">
        <div class="flex flex-col gap-2">
            <h1 class="text-xl font-bold">
                {$_("dashboard.search.found.title", {
                    values: { search: data.search },
                })}
            </h1>
            {#if backUrl}
                <p>
                    <Anchor
                        label={$_("dashboard.search.found.back")}
                        size="normal"
                        href={backUrl}
                    />
                </p>
            {/if}
        </div>
        <table
            class="flex flex-col gap-1 rounded-b-2xl bg-foreground p-4 lg:grid lg:grid-cols-[8fr_3fr_max-content] lg:gap-4"
        >
            {#if project}
                {#each data.tasks as task}
                    <TaskCard {task} {project} />
                {/each}
            {/if}
        </table>
        {#if backUrl}
            <p>
                <Anchor
                    label={$_("dashboard.search.found.back")}
                    size="normal"
                    href={backUrl}
                />
            </p>
        {/if}
    </div>
{:else if backUrl}
    <div class="flex items-center justify-center py-6">
        <div class="flex flex-col gap-4 rounded-md bg-base-100 p-6 shadow-sm">
            <p class="font-bold">
                {$_("dashboard.search.not-found.title", {
                    values: { search: data.search },
                })}
            </p>
            <p class="max-w-md">
                {$_("dashboard.search.not-found.explanation")}
            </p>
            <p>
                <Anchor
                    label={$_("dashboard.search.not-found.back")}
                    size="normal"
                    href={backUrl}
                />
            </p>
        </div>
    </div>
{/if}
