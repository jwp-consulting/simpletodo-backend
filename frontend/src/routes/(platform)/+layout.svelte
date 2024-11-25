<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<!--
With no overflow, we needed to change h-screen -> min-h-screen,
otherwise the footer will be placed inside the dashboard.
TODO evaluate whether grow is still necessary. Seems that with grow set, we
wouldn't need min-h-screen, really.
-->
<script lang="ts" context="module">
    import type { Readable } from "svelte/store";
    export type SelectedProjectUuids =
        | Readable<Map<string, string>>
        | {
              selectProjectUuid(
                  workspaceUuid: string,
                  projectUuid: string,
              ): void;
          };
    export type UserExpandOpen =
        | Readable<boolean>
        | {
              toggleUserExpandOpen(): void;
          };
</script>

<script lang="ts">
    import { derived, readonly } from "svelte/store";
    import { persisted } from "svelte-local-storage-store";

    import { page } from "$app/stores";
    import ConnectionStatus from "$lib/components/ConnectionStatus.svelte";
    import ContextMenuContainer from "$lib/components/ContextMenuContainer.svelte";
    import OverlayContainer from "$lib/components/OverlayContainer.svelte";
    import Footer from "$lib/figma/navigation/Footer.svelte";
    import HeaderDashboard from "$lib/figma/navigation/header/Dashboard.svelte";
    import SideNav from "$lib/figma/navigation/SideNav.svelte";
    import ConstructiveOverlay from "$lib/figma/overlays/constructive/ConstructiveOverlay.svelte";
    import DestructiveOverlay from "$lib/figma/overlays/DestructiveOverlay.svelte";
    import MobileMenuOverlay from "$lib/figma/overlays/MobileMenuOverlay.svelte";
    import { setContext } from "svelte";

    import { can, type Resource, type Verb } from "$lib/rules/workspace";
    import {
        mobileMenuState,
        resolveConstructiveOverlay,
        constructiveOverlayState,
        destructiveOverlayState,
        rejectDestructiveOverlay,
        rejectConstructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { PageData } from "./dashboard/$types";
    import { currentWorkspace } from "$lib/stores/dashboard/workspace";
    import {
        type CurrentTeamMember,
        type CurrentTeamMemberCan,
    } from "$lib/stores/dashboard/teamMember";
    import type { WorkspaceDetailTeamMember } from "$lib/types/workspace";
    import { createWsStore } from "$lib/stores/wsSubscription";
    import { getProject } from "$lib/stores/dashboard/project";

    export let data: PageData;
    const { user } = data;

    const currentProject = createWsStore("project", getProject);
    setContext("currentProject", currentProject);

    /*
     * Store which workspace we have seen last.
     * When we fetch a workspace based on this uuid, we must invalidate it
     * on a 404 workspace not found
     */
    const _selectedWorkspaceUuid = persisted<string | null>(
        "selected-workspace-uuid",
        null,
    );
    export const selectedWorkspaceUuid = readonly(_selectedWorkspaceUuid);
    export function selectWorkspaceUuid(uuid: string) {
        _selectedWorkspaceUuid.set(uuid);
    }
    /*
     * Clear a selected workspace uuid, if it matches the uuid arg
     */
    export function clearSelectedWorkspaceUuidIfMatch(uuid: string) {
        _selectedWorkspaceUuid.update(($uuid) => {
            if ($uuid === uuid) {
                return null;
            }
            return $uuid;
        });
    }

    const _selectedProjectUuids = persisted<Map<string, string>>(
        "selected-project-uuid",
        new Map(),
        {
            serializer: {
                // XXX Using json.parse, maybe a security problem?
                parse(value: string): Map<string, string> {
                    const values = JSON.parse(value) as [string, string][];
                    try {
                        return new Map(values);
                    } catch {
                        return new Map();
                    }
                },
                stringify(map: Map<string, string>): string {
                    const values: [string, string][] = Array.from(map);
                    return JSON.stringify(values);
                },
            },
        },
    );
    const selectedProjectUuids: SelectedProjectUuids = {
        ...readonly(_selectedProjectUuids),
        selectProjectUuid(workspaceUuid: string, projectUuid: string) {
            _selectedProjectUuids.update(($selectedProjectUuids) => {
                $selectedProjectUuids.set(workspaceUuid, projectUuid);
                return $selectedProjectUuids;
            });
        },
    };
    setContext("selectedProjectUuids", selectedProjectUuids);

    const _projectExpandOpen = persisted("board-expand-open", true);
    const projectExpandOpen = readonly(_projectExpandOpen);
    setContext("projectExpandOpen", projectExpandOpen);
    export function toggleProjectExpandOpen() {
        _projectExpandOpen.update((state) => !state);
    }

    const _userExpandOpen = persisted("user-expand-open", true);
    const userExpandOpen = readonly(_userExpandOpen);
    setContext("userExpandOpen", userExpandOpen);
    export function toggleUserExpandOpen() {
        _userExpandOpen.update((state) => !state);
    }

    const _labelExpandOpen = persisted("label-expand-open", true);
    export const labelExpandOpen = readonly(_labelExpandOpen);
    // TODO rename toggleLabelExpandOpen
    export function toggleLabelDropdownClosedNavOpen() {
        _labelExpandOpen.update((state) => !state);
    }

    const _sideNavOpen = persisted("side-nav-open", true);
    export const sideNavOpen = readonly(_sideNavOpen);
    export function toggleSideNavOpen() {
        _sideNavOpen.update((state) => !state);
    }

    const _sectionClosed = persisted("section-closed", new Set<string>(), {
        serializer: {
            // XXX Using json.parse, maybe a security problem?
            parse(value: string): Set<string> {
                const values = JSON.parse(value) as string[];
                try {
                    return new Set(values);
                } catch {
                    return new Set();
                }
            },
            stringify(set: Set<string>): string {
                const values: string[] = [...set];
                return JSON.stringify(values);
            },
        },
    });
    export const sectionClosed = readonly(_sectionClosed);

    export function toggleSectionOpen(sectionUuid: string) {
        _sectionClosed.update(($sectionClosed) => {
            if ($sectionClosed.has(sectionUuid)) {
                $sectionClosed.delete(sectionUuid);
            } else {
                $sectionClosed.add(sectionUuid);
            }
            return $sectionClosed;
        });
    }

    // Adjust this if the dashboard URLs ever change
    const showFilterRouteIds = ["/(platform)/dashboard/project/[projectUuid]"];

    /*
     * showFilters is true only for pages for which we show the user
     * the filter user / label options
     */
    export const showFilters = derived<typeof page, boolean>(
        page,
        ($page, set) => {
            const { route } = $page;
            const { id } = route;
            set(showFilterRouteIds.find((i) => i === id) !== undefined);
        },
        false,
    );

    /**
     * Find current team member belonging to logged in user
     */
    const currentTeamMember: CurrentTeamMember = derived<
        [typeof currentWorkspace, typeof currentProject],
        WorkspaceDetailTeamMember | undefined
    >(
        [currentWorkspace, currentProject],
        ([$currentWorkspace, $currentProject], set) => {
            const teamMembers =
                $currentWorkspace.value?.team_members ??
                $currentProject.value?.workspace.team_members;
            if (teamMembers === undefined) {
                set(undefined);
                return;
            }
            const wsUser = teamMembers.find(
                (wsUser) => wsUser.user.email === user.email,
            );
            if (wsUser === undefined) {
                throw new Error("Couldn't find currentTeamMember");
            }
            set(wsUser);
        },
        undefined,
    );

    /**
     * A store that returns a function that allows permission checking for the
     * currently active, logged in user's team member.
     */
    const currentTeamMemberCan: CurrentTeamMemberCan = derived<
        [
            typeof currentTeamMember,
            typeof currentWorkspace,
            typeof currentProject,
        ],
        (verb: Verb, resource: Resource) => boolean
    >(
        [currentTeamMember, currentWorkspace, currentProject],
        ([$currentTeamMember, $currentWorkspace, $currentProject], set) => {
            if ($currentTeamMember === undefined) {
                console.warn("teamMember was undefined");
                set(() => false);
                return;
            }
            const quota =
                $currentWorkspace.value?.quota ??
                $currentProject.value?.workspace.quota;
            if (quota === undefined) {
                console.warn("no quota found");
                set(() => false);
                return;
            }
            const fn = (verb: Verb, resource: Resource) =>
                can(verb, resource, $currentTeamMember, quota);
            set(fn);
        },
        () => false,
    );
    setContext<CurrentTeamMember>("currentTeamMember", currentTeamMember);
    setContext<CurrentTeamMemberCan>(
        "currentTeamMemberCan",
        currentTeamMemberCan,
    );
</script>

<div class="flex min-h-screen grow flex-col">
    <HeaderDashboard {user} />
    {#if $mobileMenuState.kind === "visible"}
        <MobileMenuOverlay target={$mobileMenuState.target} />
    {/if}
    <div class="flex min-h-0 shrink grow flex-row">
        <!-- this breakpoint is in tune with the mobile menu breakpoint -->
        <div class="hidden h-full shrink-0 md:block">
            <SideNav />
        </div>
        <!-- not inserting min-w-0 will mean that this div will extend as much as
    needed around whatever is inside the slot -->
        <div class="min-w-0 grow" role="presentation">
            <slot />
        </div>
    </div>
</div>

<ConnectionStatus />

<OverlayContainer
    closeOverlay={rejectDestructiveOverlay}
    store={destructiveOverlayState}
    let:target
>
    <DestructiveOverlay {target} />
</OverlayContainer>

<OverlayContainer
    closeOverlay={rejectConstructiveOverlay}
    store={constructiveOverlayState}
    let:target
>
    <ConstructiveOverlay {target} on:cancel={resolveConstructiveOverlay} />
</OverlayContainer>

<ContextMenuContainer />

<Footer {user} />
