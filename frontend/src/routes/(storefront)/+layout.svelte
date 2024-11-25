<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import Footer from "$lib/figma/navigation/Footer.svelte";
    import Continue from "$lib/figma/navigation/header/Continue.svelte";
    import Landing from "$lib/figma/navigation/header/Landing.svelte";
    import MobileMenuOverlay from "$lib/figma/overlays/MobileMenuOverlay.svelte";
    import { mobileMenuState } from "$lib/stores/globalUi";
    import type { PageData } from "./$types";

    export let data: PageData;
    const { user } = data;
</script>

<div class="flex grow flex-col">
    {#if user.kind === "authenticated"}
        <Continue />
    {:else}
        <Landing />
    {/if}
    <div class="flex grow flex-col">
        {#if $mobileMenuState.kind === "visible"}
            <div class="w-full border-b-2 border-border md:hidden">
                <MobileMenuOverlay
                    minHScreen={false}
                    target={$mobileMenuState.target}
                />
            </div>
        {/if}
        <div class="flex grow flex-col justify-between">
            <slot />
        </div>
    </div>
</div>
<Footer {user} />
