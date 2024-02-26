// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023-2024 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
import { readonly, writable } from "svelte/store";

import {
    getUser,
    updateUser,
    updateProfilePicture,
} from "$lib/repository/user";
import * as userRepository from "$lib/repository/user";
import type { RepositoryContext } from "$lib/types/repository";
import type { User } from "$lib/types/user";

const _user = writable<User | undefined>(undefined);
export const user = readonly(_user);

export async function logIn(
    email: string,
    password: string,
    repositoryContext: RepositoryContext,
) {
    const response = await userRepository.logIn(
        email,
        password,
        repositoryContext,
    );
    if (response.ok) {
        _user.set(response.data);
    }
    return response;
}

export async function logOut(repositoryContext: RepositoryContext) {
    await userRepository.logOut(repositoryContext);
    _user.set(undefined);
}

export async function fetchUser(
    repositoryContext: RepositoryContext,
): Promise<User | undefined> {
    const userData = await getUser(repositoryContext);
    _user.set(userData);
    return userData;
}

export async function updateUserProfile(
    preferredName: string | undefined,
    picture:
        | { kind: "keep" }
        | { kind: "update"; imageFile: File }
        | { kind: "clear" },
    repositoryContext: RepositoryContext,
    // TODO Promise<ApiResponse<User, ...>>
): Promise<User> {
    if (picture.kind === "update") {
        await updateProfilePicture(picture.imageFile);
    } else if (picture.kind === "clear") {
        await updateProfilePicture(undefined);
    }
    const response = await updateUser(
        {
            // Kind of confusing logic here, tbh
            // All we want to do is to clear the preferred name when it's empty
            preferred_name:
                preferredName === "" ? null : preferredName ?? null,
        },
        repositoryContext,
    );
    if (!response.ok) {
        throw new Error("Expected response.ok");
    }
    _user.set(response.data);
    return response.data;
}
