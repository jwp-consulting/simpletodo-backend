<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<script lang="ts">
    import { workspace, project, user1 } from "$lib-stories/storybook";
    import Dashboard from "$routes/(platform)/dashboard/project/[projectUuid]/+page.svelte";

    const data = {
        project: {
            ...project,
            archived: null,
            description: null,
            sections: [],
            workspace,
        },
        user: user1,
    };
</script>

<Dashboard {data} />
