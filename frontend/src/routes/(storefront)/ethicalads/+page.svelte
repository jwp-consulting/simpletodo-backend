<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<script lang="ts">
    import Storefront from "../+page.svelte";
    import type { PageData } from "./$types";

    export let data: PageData;
</script>

<Storefront {data} />
