<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { browser } from "$app/environment";
    import Avatar from "$lib/figma/navigation/AvatarMarble.svelte";
    import type {
        AvatarStateSize,
        AvatarVariantContent,
    } from "$lib/figma/types";
    import { getDisplayName } from "$lib/types/user";
    import { tw } from "$lib/utils/ui";

    export let content: AvatarVariantContent;
    export let size: AvatarStateSize;
    $: user = content.user;

    $: outerSize = {
        large: tw`h-24 w-24`,
        medium: tw`h-6 w-6`,
    }[size];
    type Size = 32 | 96;
    let innerSize: Size;
    const sizes: Record<AvatarStateSize, Size> = {
        large: 96,
        medium: 32,
    } as const;
    $: innerSize = sizes[size];
    $: profilePicture = user ? user.profile_picture : undefined;
    $: name = user ? getDisplayName(user) : undefined;
</script>

<div
    class="flex flex-row {outerSize} items-center rounded-full border border-primary"
    class:bg-background={user === undefined}
>
    {#if profilePicture}
        <img
            src={profilePicture}
            alt={name}
            class="h-full w-full overflow-x-auto rounded-full object-cover object-center"
        />
    {:else if name && browser}
        <!-- TODO workaround since name is not reactive inside Avatar -->
        {#key name}
            <!-- TODO Avatar needs accessible label -->
            <Avatar size={innerSize} {name} />
        {/key}
    {/if}
</div>
