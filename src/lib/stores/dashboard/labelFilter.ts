import { writable } from "svelte/store";

import {
    createLabelFilter,
    createLabelSearchResults,
    currentWorkspaceLabels,
} from "./label";

import type { LabelFilter } from "$lib/types/stores";
import type { LabelSelection, LabelSelectionInput } from "$lib/types/ui";

/*
 * Here come the shared methods for filtering all tasks by one or more labels
 */
export const selectedLabels = writable<LabelSelection>({ kind: "allLabels" });

export function filterByLabel(selection: LabelSelectionInput) {
    selectedLabels.update((selectedLabels) => {
        if (selection.kind == "label") {
            if (selectedLabels.kind === "labels") {
                selectedLabels.labelUuids.add(selection.labelUuid);
                return selectedLabels;
            } else {
                return {
                    kind: "labels",
                    labelUuids: new Set([selection.labelUuid]),
                };
            }
        } else if (selection.kind == "noLabel") {
            return { kind: "noLabel" };
        } else {
            return { kind: "allLabels" };
        }
    });
}
export function unfilterByLabel(selection: LabelSelectionInput) {
    selectedLabels.update((selectedLabels) => {
        if (selection.kind == "label") {
            if (selectedLabels.kind === "labels") {
                selectedLabels.labelUuids.delete(selection.labelUuid);
                if (selectedLabels.labelUuids.size === 0) {
                    return { kind: "allLabels" };
                }
                return selectedLabels;
            } else {
                return selectedLabels;
            }
        } else if (selection.kind == "noLabel") {
            return { kind: "allLabels" };
        } else {
            return { kind: "noLabel" };
        }
    });
}

export const labelSearch = createLabelFilter();
// All the variables in this module should have labelFilter themed names
export const labelFilterSearchResults = createLabelSearchResults(
    currentWorkspaceLabels,
    labelSearch
);

export const labelSearchModule: LabelFilter = {
    select: filterByLabel,
    deselect: unfilterByLabel,
    selected: selectedLabels,
};
