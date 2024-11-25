// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
/**
 * Team member related store
 * Following use cases:
 *
 * - Selecting a user to be assigned to task (teamMemberAssignment)
 * - Filtering tasks inside a ws board by ws user
 * (teamMemberFilter)
 * Before I wrote these two things to be the same, even though that meant
 * unnecessarily shoehorning unrelated features into the same thing
 */
import { derived } from "svelte/store";
import type { Readable } from "svelte/store";

import type { WorkspaceDetailTeamMember } from "$lib/types/workspace";

import { currentProject } from "./project";
import { currentWorkspace } from "./workspace";
import type { Resource, Verb } from "$lib/rules/workspace";

export type CurrentTeamMembers = Readable<
    readonly WorkspaceDetailTeamMember[] | undefined
>;

export const currentTeamMembers: CurrentTeamMembers = derived<
    [typeof currentWorkspace, typeof currentProject],
    readonly WorkspaceDetailTeamMember[] | undefined
>(
    [currentWorkspace, currentProject],
    ([$currentWorkspace, $currentProject], set) => {
        set(
            $currentWorkspace.value?.team_members ??
                $currentProject.value?.workspace.team_members,
        );
    },
    undefined,
);

export type CurrentTeamMember = Readable<
    WorkspaceDetailTeamMember | undefined
>;

export type CurrentTeamMemberCan = Readable<
    (verb: Verb, resource: Resource) => boolean
>;
