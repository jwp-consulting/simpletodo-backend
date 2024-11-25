// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { derived, writable } from "svelte/store";
import type { Readable } from "svelte/store";

import { searchAmong } from "$lib/stores/util";
import type { SearchInput } from "$lib/types/base";
import type { Label } from "$lib/types/workspace";
import { currentProject } from "./project";

type CurrentWorkspaceLabels = Readable<readonly Label[] | undefined>;
export const currentWorkspaceLabels: CurrentWorkspaceLabels = derived<
    [typeof currentProject],
    readonly Label[] | undefined
>(
    [currentProject],
    ([$currentProject], set) => {
        set($currentProject.value?.workspace.labels);
    },
    undefined,
);
// LabelFilter and Selection
function searchLabels(
    labels: readonly Label[],
    searchInput: SearchInput,
): readonly Label[] {
    if (searchInput === undefined) {
        return labels;
    }
    return searchAmong(["name"], labels, searchInput);
}

type LabelFilter = Readable<SearchInput>;
export function createLabelFilter(): LabelFilter {
    return writable<SearchInput>(undefined);
}

type LabelSearchResults = Readable<readonly Label[]>;

export function createLabelSearchResults(
    currentWorkspaceLabels: CurrentWorkspaceLabels,
    labelSearch: LabelFilter,
): LabelSearchResults {
    return derived<[CurrentWorkspaceLabels, LabelFilter], readonly Label[]>(
        [currentWorkspaceLabels, labelSearch],
        ([$currentWorkspaceLabels, $labelSearch], set) => {
            if ($currentWorkspaceLabels === undefined) {
                return;
            }
            set(searchLabels($currentWorkspaceLabels, $labelSearch));
        },
        [],
    );
}
