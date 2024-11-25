<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<script lang="ts">
    import { sectionDetail, user1 } from "$lib-stories/storybook";
    import CreateTask from "$routes/(platform)/dashboard/section/[sectionUuid]/create-task/+page.svelte";

    const data = {
        section: sectionDetail,
        user: user1,
    };
</script>

<CreateTask {data} />
