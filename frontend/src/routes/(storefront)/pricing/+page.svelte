<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _, json } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { signUpUrl } from "$lib/urls/user";
    import { helpUrl } from "$lib/urls/help";
    import type { PageData } from "./$types";

    export let data: PageData;
    const { user } = data;

    $: features = $json("pricing.features.list") as string[];
    $: limitations = $json("pricing.trial-mode.limitations.list") as string[];
</script>

<svelte:head>
    <title>{$_("pricing.title")}</title>
</svelte:head>

<main class="flex w-full flex-col items-center px-8 py-10">
    <div class="flex w-full max-w-xl flex-col gap-4 sm:items-center sm:gap-8">
        <!-- explain that we have one price to rule them all -->
        <header class="flex w-full flex-col gap-4">
            <h1 class="text-4xl font-bold sm:text-center sm:text-6xl">
                {$_("pricing.header.title")}
            </h1>
            <p class="sm:text-center sm:text-3xl sm:font-bold">
                {$_("pricing.header.subtitle")}
            </p>
        </header>
        <!-- list the features -->
        <section class="flex flex-col gap-2">
            <h2 class="text-2xl">
                {$_("pricing.features.title")}
            </h2>
            <ul class="list-inside list-disc">
                {#each features as feature}
                    <li>{feature}</li>
                {/each}
            </ul>
        </section>
        <!-- colorful box with CTA -->
        <section
            class="flex w-full max-w-xl flex-col gap-4 rounded-xl bg-background px-4 py-6 sm:items-center sm:gap-8"
        >
            <div class="flex flex-col gap-4">
                <h2 class="text-xl font-bold sm:text-center">
                    {$_("pricing.plan.title")}
                </h2>
                <strong class="text-4xl font-bold">
                    {$_("pricing.plan.price", { values: { price: 8 } })}
                </strong>
            </div>
            {#if user.kind === "authenticated"}
                <Button
                    action={{ kind: "a", href: helpUrl("billing") }}
                    size="medium"
                    color="blue"
                    style={{ kind: "primary" }}
                    label={$_("pricing.plan.cta-logged-in")}
                />
            {:else}
                <Button
                    action={{ kind: "a", href: signUpUrl }}
                    size="medium"
                    color="blue"
                    style={{ kind: "primary" }}
                    label={$_("pricing.plan.cta")}
                />
            {/if}
        </section>
        <!-- explain trial mode -->
        <section id="trial-mode" class="flex flex-col gap-2">
            <h2 class="text-2xl sm:text-center">
                {$_("pricing.trial-mode.title")}
            </h2>
            <p>
                {$_("pricing.trial-mode.explanation")}
            </p>
            <h3 class="text-xl sm:text-center">
                {$_("pricing.trial-mode.limitations.title")}
            </h3>
            <ul class="list-inside list-disc sm:self-center">
                {#each limitations as limitation}
                    <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                    <li>{@html limitation}</li>
                {/each}
            </ul>
        </section>
    </div>
</main>
