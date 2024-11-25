// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
/**
 * Contain the HttpStore, a store that can be updated using a fetch-like getter
 *
 */
import { writable } from "svelte/store";
import type { Readable } from "svelte/store";

import { backOff } from "exponential-backoff";

// TODO This could be RepoGetter, except that RepoGetter takes a uuid
type HttpStore<T> = Readable<T | undefined> & {
    load: () => Promise<T>;
    reset: () => void;
};

/*
 * Similar to createWsStore, but has to manually refetch
 */
export function createHttpStore<T>(getter: () => Promise<T>): HttpStore<T> {
    let value: T | undefined = undefined;
    const { set, subscribe } = writable<T | undefined>(undefined);
    const load = async (): Promise<T> => {
        value = await backOff(() => getter());
        set(value);
        return value;
    };
    return {
        subscribe,
        load,
        reset() {
            set(undefined);
            value = undefined;
        },
    };
}
