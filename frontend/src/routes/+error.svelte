<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { page } from "$app/stores";
    import Landing from "$lib/figma/navigation/header/Landing.svelte";
    import Footer from "$lib/figma/navigation/Footer.svelte";
    import type { LayoutData } from "./$types";

    export let data: LayoutData;
    const { user } = data;
</script>

<svelte:head>
    {#if $page.status == 404}
        <title>
            {$_("error-page.404-not-found.title")}
        </title>
    {:else if $page.error}
        <title>
            {$_("error-page.other.title")}
        </title>
    {:else}
        <title>
            {$_("error-page.no-error.title")}
        </title>
    {/if}
</svelte:head>

<Landing />
<div class="flex grow flex-col items-center gap-12 p-20">
    <main class="flex max-w-lg flex-col gap-6">
        <h1 class="text-5xl font-bold">
            {#if $page.status == 404}
                {$_("error-page.404-not-found.title")}
            {:else if $page.error}
                {$_("error-page.other.title")}
            {:else}
                {$_("error-page.no-error.title")}
            {/if}
        </h1>
        {#if $page.status == 404}
            <enhanced:img
                alt={$_("error-page.404-not-found.img-alt")}
                class="max-w-sm"
                src="./assets/status404Image.png"
            />
            <p>{$_("error-page.404-not-found.explanation")}</p>
            <p>{$_("error-page.404-not-found.what-to-do")}</p>
            <Anchor
                label={$_("error-page.404-not-found.contact")}
                href="/contact-us"
            />
        {:else if $page.error}
            <enhanced:img
                alt={$_("error-page.other.img-alt")}
                class="max-w-sm"
                src="./assets/status500Image.png"
            />
            <p>{$_("error-page.other.explanation")}</p>
            <pre>{JSON.stringify($page.error)}</pre>
            <p>{$_("error-page.other.what-to-do")}</p>
            <Anchor
                label={$_("error-page.other.contact")}
                href="/contact-us"
            />
        {:else}
            {$_("error-page.no-error.body")}
        {/if}
    </main>
</div>
<Footer {user} />
