// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { searchTasks } from "$lib/stores/dashboard/task";
import type { SearchInput } from "$lib/types/base";
import type { TaskWithSection } from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

import type { PageLoadEvent } from "./$types";

interface Data {
    tasks: readonly TaskWithSection[];
    search: SearchInput;
}
export async function load({ url, parent }: PageLoadEvent): Promise<Data> {
    const search: SearchInput = url.searchParams.get("search") ?? undefined;
    const data = await parent();
    const { sections } = data.project;
    const tasks = searchTasks(unwrap(sections, "Expected sections"), search);
    return { tasks, search };
}
