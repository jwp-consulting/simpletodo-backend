<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import DashboardPlaceholder from "$lib/components/onboarding/DashboardPlaceholder.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { getDashboardProjectUrl, getSettingsUrl } from "$lib/urls";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { user, task, assignee, project, section, workspace, label } = data;

    const taskTitle = task.title;
</script>

<svelte:head
    ><title
        >{$_("onboarding.assign-task.title", { values: { taskTitle } })}</title
    ></svelte:head
>

<Onboarding
    stepCount={5}
    step={5}
    nextLabel={$_("onboarding.assign-task.continue")}
    nextAction={{
        kind: "a",
        href: getDashboardProjectUrl(project),
    }}
>
    <svelte:fragment slot="title"
        >{$_("onboarding.assign-task.heading", {
            values: { taskTitle },
        })}</svelte:fragment
    >
    <svelte:fragment slot="prompt">
        <div class="flex flex-col gap-4">
            <p>{$_("onboarding.assign-task.prompt.finished")}</p>
            <p>{$_("onboarding.assign-task.prompt.adding-team-members")}</p>
            <Anchor
                href="/help/billing"
                label={$_("onboarding.assign-task.follow-up.billing-help")}
                openBlank
            />
            <Anchor
                href={getSettingsUrl(workspace, "billing")}
                label={$_(
                    "onboarding.assign-task.follow-up.go-to-billing-settings",
                )}
                openBlank
            />
        </div>
    </svelte:fragment>

    <DashboardPlaceholder
        slot="content"
        {user}
        state={{
            kind: "assign-task",
            task,
            label,
            workspace,
            project,
            section,
            assignee,
        }}
    />
</Onboarding>
