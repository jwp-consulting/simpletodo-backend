<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import SolutionsFeature from "$lib/components/solutions/SolutionsFeature.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";

    import Filters from "./assets/filters.png?enhanced";
    import OpenSource from "./assets/open-source.png?enhanced";
    import Privacy from "./assets/privacy.png?enhanced";
    import Responsive from "./assets/responsive.png?enhanced";
    import SubTask from "./assets/sub-task.png?enhanced";
    import TaskMenu from "./assets/task-menu.png?enhanced";
    import { signUpUrl } from "$lib/urls/user";
    import { dashboardUrl } from "$lib/urls/dashboard";
    import type { PageData } from "./$types";

    export let data: PageData;
    const { user } = data;
</script>

<svelte:head>
    <title>{$_("index.title")}</title>
</svelte:head>

<HeroLayout heroBackground={false}>
    <section
        slot="hero"
        class="grid grid-cols-1 items-center gap-4 sm:grid-cols-2"
    >
        <div class="flex flex-col gap-12">
            <header class="flex flex-col gap-10">
                <h1 class="text-4xl font-bold md:text-6xl">
                    {$_("index.hero.header")}
                </h1>
                <p>
                    {$_("index.hero.text")}
                </p>
            </header>
            {#if user.kind === "authenticated"}
                <Button
                    style={{ kind: "primary" }}
                    color="blue"
                    size="medium"
                    action={{ kind: "a", href: dashboardUrl }}
                    label={$_("index.hero.continue-to-dashboard")}
                    grow={false}
                />
            {:else}
                <Button
                    style={{ kind: "primary" }}
                    color="blue"
                    size="medium"
                    action={{ kind: "a", href: signUpUrl }}
                    label={$_("index.hero.button")}
                    grow={false}
                />
            {/if}
        </div>
        <div class="max-w-md">
            <enhanced:img src="./assets/hero.png" alt={$_("index.hero.alt")} />
        </div>
    </section>
    <div slot="content" class="flex flex-col gap-16">
        <section class="flex flex-col gap-4">
            <h2 class="text-center text-3xl font-bold md:text-5xl">
                <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                {@html $_("index.trust.header")}
            </h2>
            <h4 class="text-center text-2xl font-bold md:text-3xl">
                {$_("index.trust.text")}
            </h4>
        </section>
        <SolutionsFeature
            feature={{
                title: $_("index.features.feature-1.header"),
                text: $_("index.features.feature-1.text"),
                image: {
                    src: TaskMenu,
                    alt: $_("index.features.feature-1.alt"),
                    position: "right",
                },
            }}
        />

        <SolutionsFeature
            feature={{
                title: $_("index.features.feature-2.header"),
                text: $_("index.features.feature-2.text"),
                image: {
                    src: SubTask,
                    alt: $_("index.features.feature-2.alt"),
                    position: "left",
                },
            }}
        />

        <SolutionsFeature
            feature={{
                title: $_("index.features.feature-3.header"),
                text: $_("index.features.feature-3.text"),
                image: {
                    src: Filters,
                    alt: $_("index.features.feature-3.alt"),
                    position: "right",
                },
            }}
        />

        <SolutionsFeature
            feature={{
                title: $_("index.features.feature-5.header"),
                text: $_("index.features.feature-5.text"),
                image: {
                    src: Responsive,
                    alt: $_("index.features.feature-5.alt"),
                    position: "right",
                },
            }}
        />
        <section class="flex flex-col gap-7">
            <header class="flex flex-col gap-3">
                <h2 class="text-2xl font-bold sm:text-4xl">
                    {$_("index.solutions.header.title")}
                </h2>
                <p>
                    {$_("index.solutions.header.text")}
                </p>
            </header>
            <div class="flex flex-col gap-5 text-center">
                <div class="grid grid-cols-1 gap-8 sm:grid-cols-3">
                    <div class="flex flex-col gap-3">
                        <enhanced:img
                            src="./solutions/assets/hero-development-teams.png"
                            alt={$_(
                                "index.solutions.list.development-teams.alt",
                            )}
                        />
                        <Anchor
                            size="large"
                            href={"solutions/development-teams"}
                            label={$_(
                                "index.solutions.list.development-teams.text",
                            )}
                        />
                    </div>
                    <div class="flex flex-col gap-3">
                        <enhanced:img
                            src="./solutions/assets/hero-research.png"
                            alt={$_("index.solutions.list.research.alt")}
                        />
                        <Anchor
                            size="large"
                            href={"solutions/research"}
                            label={$_("index.solutions.list.research.text")}
                        />
                    </div>
                    <div class="flex flex-col gap-3">
                        <enhanced:img
                            src="./solutions/assets/hero-project-management.png"
                            alt={$_(
                                "index.solutions.list.project-management.alt",
                            )}
                        />
                        <Anchor
                            size="large"
                            href={"solutions/project-management"}
                            label={$_(
                                "index.solutions.list.project-management.text",
                            )}
                        />
                    </div>
                </div>
                <Anchor
                    size="large"
                    href={"solutions/"}
                    label={$_("index.solutions.more")}
                />
            </div>
        </section>
        <SolutionsFeature
            feature={{
                title: $_("index.features.feature-6.header"),
                text: $_("index.features.feature-6.text"),
                image: {
                    src: Privacy,
                    alt: $_("index.features.feature-6.alt"),
                    position: "right",
                },
            }}
        />
        <SolutionsFeature
            feature={{
                title: $_("index.features.feature-7.header"),
                text: $_("index.features.feature-7.text"),
                image: {
                    src: OpenSource,
                    alt: $_("index.features.feature-7.alt"),
                    position: "left",
                },
                learnMore: {
                    href: "/free-software",
                    label: $_("index.features.feature-7.link"),
                },
            }}
        />
    </div>
</HeroLayout>
