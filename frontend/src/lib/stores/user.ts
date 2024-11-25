// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
import { dataOrThrow, openApiClient } from "$lib/repository/util";
import { backOff } from "exponential-backoff";
import { currentWorkspaces } from "./dashboard/workspace";

const fetchUserBackOff = () =>
    backOff(() => dataOrThrow(openApiClient.GET("/user/user/current-user")));

export const currentUser = {
    async load() {
        const { data } = await fetchUserBackOff();
        return data;
    },
};

export async function logIn(email: string, password: string) {
    const { data, error } = await openApiClient.POST("/user/user/log-in", {
        body: { email, password },
    });
    // TODO invalidate user
    return { data, error };
}

async function _logOut() {
    const promise = openApiClient.POST("/user/user/log-out");
    const { data, error } = await promise;
    if (error?.code === 403) {
        return { error, data: undefined };
    }
    if (error) {
        throw new Error("Couldn't log out");
    }
    // TODO invalidate user
    return { data, error: undefined };
}

export async function logOut() {
    const { data, error } = await backOff(_logOut);
    // In the future we'd like want to test for 401 here
    currentWorkspaces.reset();
    // TODO invalidate user
    return { data, error };
}

export async function updateUserProfile(preferred_name: string | null) {
    const { data, error } = await openApiClient.PUT(
        "/user/user/current-user/update",
        { body: { preferred_name } },
    );
    if (data) {
        return { data };
    }
    // TODO invalidate user
    return { error };
}
