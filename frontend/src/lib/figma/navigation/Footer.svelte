<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import PolyLogo from "./polylogo.svg?url";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { signUpUrl } from "$lib/urls/user";
    import { backToHomeUrl } from "$lib/urls";
    import type { CurrentUser } from "$lib/types/user";

    export let user: CurrentUser;

    const buildData = {
        buildDate: __BUILD_DATE__,
        commitHash: __GIT_COMMIT_HASH__,
        commitDate: __GIT_COMMIT_DATE__,
        branchName: __GIT_BRANCH_NAME__,
    };
</script>

<footer class="flex w-full flex-col gap-6 border-t border-border p-8">
    <div class="flex flex-col gap-8 sm:flex-row sm:flex-wrap">
        <!-- Header -->
        <div class="flex flex-col gap-6">
            <a class="flex flex-col gap-2" href={backToHomeUrl}>
                <div class="flex flex-row items-center gap-2">
                    <img
                        src={PolyLogo}
                        alt={$_("navigation.footer.logo.alt")}
                    />
                </div>
                <p>{$_("navigation.footer.logo.heading")}</p>
            </a>
            {#if user.kind !== "authenticated"}
                <Button
                    action={{ kind: "a", href: signUpUrl }}
                    style={{ kind: "primary" }}
                    color="blue"
                    size="medium"
                    grow={false}
                    label={$_("navigation.footer.cta")}
                />
            {/if}
        </div>
        <!-- Nav -->
        <nav class="flex flex-col gap-12 sm:flex-row">
            <section class="flex flex-col gap-1">
                <h6 class="font-bold">
                    {$_("navigation.footer.nav.product.title")}
                </h6>
                <ul class="flex flex-col gap-2">
                    <li>
                        <Anchor
                            href="/pricing"
                            label={$_("navigation.footer.nav.product.pricing")}
                        />
                    </li>
                    <li>
                        <Anchor
                            href="/solutions"
                            label={$_(
                                "navigation.footer.nav.product.solutions",
                            )}
                        />
                    </li>
                </ul>
            </section>
            <section class="flex flex-col gap-1">
                <h6 class="font-bold">
                    {$_("navigation.footer.nav.resources.title")}
                </h6>
                <ul class="flex flex-col gap-2">
                    <li>
                        <Anchor
                            href="/help"
                            label={$_(
                                "navigation.footer.nav.resources.help-and-tips",
                            )}
                            openBlank
                        />
                    </li>
                    <li>
                        <Anchor
                            href="/help/keyboard-shortcuts"
                            label={$_(
                                "navigation.footer.nav.resources.keyboard-shortcuts",
                            )}
                            openBlank
                        />
                    </li>
                    <li>
                        <Anchor
                            href="https://www.jwpconsulting.net/tags/projectify/"
                            label={$_("navigation.footer.nav.resources.blog")}
                            openBlank
                        />
                    </li>
                    <li>
                        <Anchor
                            href="https://github.com/jwpconsulting/projectify"
                            label={$_(
                                "navigation.footer.nav.resources.github",
                            )}
                            openBlank
                        />
                    </li>
                </ul>
            </section>
            <section class="flex flex-col gap-1">
                <h6 class="font-bold">
                    {$_("navigation.footer.nav.company.title")}
                </h6>
                <ul class="flex flex-col gap-2">
                    <li>
                        <Anchor
                            href="/accessibility"
                            label={$_(
                                "navigation.footer.nav.company.accessibility-statement",
                            )}
                        />
                    </li>
                    <li>
                        <Anchor
                            href="/contact-us"
                            label={$_(
                                "navigation.footer.nav.company.contact-us",
                            )}
                        />
                    </li>
                    <li>
                        <Anchor
                            href="https://www.jwpconsulting.net"
                            label={$_(
                                "navigation.footer.nav.company.corporate-info",
                            )}
                            openBlank
                        />
                    </li>
                </ul>
            </section>
            <section class="flex flex-col gap-1">
                <h6 class="font-bold">
                    {$_("navigation.footer.nav.security.title")}
                </h6>
                <ul class="flex flex-col gap-2">
                    <li>
                        <Anchor
                            label={$_(
                                "navigation.footer.nav.security.general",
                            )}
                            href="/security/general"
                        />
                    </li>
                    <li>
                        <Anchor
                            label={$_(
                                "navigation.footer.nav.security.disclose",
                            )}
                            href="/security/disclose"
                        />
                    </li>
                </ul>
            </section>
            <section class="flex flex-col gap-1">
                <h6 class="font-bold">
                    {$_("navigation.footer.nav.legal.title")}
                </h6>
                <ul class="flex flex-col gap-2">
                    <li>
                        <Anchor
                            label={$_("navigation.footer.nav.legal.privacy")}
                            href="/privacy"
                        />
                    </li>
                    <li>
                        <Anchor
                            label={$_("navigation.footer.nav.legal.tos")}
                            href="/tos"
                        />
                    </li>
                    <li>
                        <Anchor
                            label={$_("navigation.footer.nav.legal.credits")}
                            href="/credits"
                        />
                    </li>
                    <li>
                        <Anchor
                            label={$_(
                                "navigation.footer.nav.legal.free-software",
                            )}
                            href="/free-software"
                        />
                    </li>
                </ul>
            </section>
        </nav>
        <!-- epilogue -->
        <section class="flex flex-col gap-4">
            <p>
                {$_("navigation.footer.epilogue.copyright")}
                <br />
                {$_("navigation.footer.epilogue.free-software")}
                <Anchor
                    href="/free-software"
                    label={$_("navigation.footer.epilogue.details")}
                />
            </p>
            <p class="text-utility">
                {$_("navigation.footer.epilogue.build", {
                    values: buildData,
                })}
            </p>
        </section>
    </div>
</footer>
