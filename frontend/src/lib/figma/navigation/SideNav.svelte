<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import Collapsed from "$lib/figma/navigation/side-nav/Collapsed.svelte";
    import Full from "$lib/figma/navigation/side-nav/Full.svelte";
    import { getContext } from "svelte";
    import type { Readable } from "svelte/motion";

    const sideNavOpen = getContext<Readable<boolean>>("sideNavOpen");
</script>

{#if $sideNavOpen}
    <div class="max-w-xs 2xl:max-w-md">
        <Full />
    </div>
{:else}
    <!-- Figma says 72px but we only have 64 or 80 (16, 29 rem respectively)-->
    <!-- Might we refactor this into something separate? -->
    <div class="w-20">
        <Collapsed />
    </div>
{/if}
