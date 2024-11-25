<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<!-- TODO At some point we will add the tab bar and bread crumbs here -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import type { LayoutData } from "./$types";
    import { createWsStore } from "$lib/stores/wsSubscription";
    import type { TaskDetail } from "$lib/types/workspace";
    import { openApiClient } from "$lib/repository/util";
    import { setContext } from "svelte";

    export let data: LayoutData;

    $: task = $currentTask.or(data.task);

    const currentTask = createWsStore<TaskDetail>(
        "task",
        async (task_uuid: string) => {
            const { data, error } = await openApiClient.GET(
                "/workspace/task/{task_uuid}",
                { params: { path: { task_uuid } } },
            );
            if (error?.code === 500) {
                throw new Error("Server error 500");
            }
            if (data) {
                return data;
            }
            return undefined;
        },
    );
    setContext("currentTask", currentTask);
</script>

<svelte:head>
    <title>
        {$_("task.title", { values: { title: task.title } })}
    </title>
</svelte:head>

<slot />
