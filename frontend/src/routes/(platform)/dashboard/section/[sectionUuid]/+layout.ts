// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { error } from "@sveltejs/kit";

import { getSection } from "$lib/repository/workspace/section";
import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import type { SectionDetail } from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

import type { LayoutLoadEvent } from "./$types";
import { backOff } from "exponential-backoff";

interface Data {
    section: SectionDetail;
}

export async function load({
    params: { sectionUuid },
}: LayoutLoadEvent): Promise<Data> {
    const section = await backOff(() => getSection(sectionUuid));
    if (!section) {
        error(
            404,
            `The section with UUID '${sectionUuid}' could not be found`,
        );
    }
    const project = section.project;
    const { uuid: workspaceUuid } = unwrap(
        project.workspace,
        "Expected workspace",
    );
    currentWorkspace.loadUuid(workspaceUuid).catch((reason: unknown) => {
        console.error(
            "Tried to load currentWorkspace in background, but failed with",
            reason,
        );
    });
    return { section };
}

export const prerender = false;
