<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<script lang="ts">
    import ConnectionStatus from "$lib/components/ConnectionStatus.svelte";
    import ContextMenuContainer from "$lib/components/ContextMenuContainer.svelte";
    import HeaderDashboard from "$lib/figma/navigation/header/Dashboard.svelte";
    import type { LayoutData } from "./$types";

    export let data: LayoutData;
    const { user } = data;
</script>

<div class="flex grow flex-col overflow-y-auto">
    <HeaderDashboard {user} />
    <slot />
</div>

<ConnectionStatus />
<ContextMenuContainer />
