// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
import { getCookie } from "$lib/utils/cookie";
import createClient, {
    createFinalURL,
    createQuerySerializer,
} from "openapi-fetch";
import type { Middleware } from "openapi-fetch";

import type { paths } from "$lib/types/schema";
import { invalidate } from "$app/navigation";
import { withLock } from "superlock";

const baseUrl = __API_ENDPOINT__;

// TODO consider adding content type and accept here? Perhaps based on
// if GET or else

const csrfMiddleWare: Middleware = {
    onRequest(request: Request) {
        // If GET then no CSRF token is required anyway
        if (request.method === "GET") {
            return request;
        }
        const csrftoken = getCookie("csrftoken");
        if (csrftoken === undefined) {
            console.warn("No csrf token found");
            return request;
        }
        request.headers.set("X-CSRFToken", csrftoken);
        return request;
    },
};

const lock = withLock(10);

export function overrideClient(fetch: typeof global.fetch) {
    const wrapped = async (...args: Parameters<typeof global.fetch>) => {
        return lock(() => fetch(...args));
    };
    openApiClient = createClientCustom(wrapped);
}

function createClientCustom(fetch?: typeof global.fetch) {
    const client = createClient<paths>({
        baseUrl,
        credentials: "include",
        fetch,
    });
    client.use(csrfMiddleWare);
    return client;
}

type Client = ReturnType<typeof createClient<paths>>;

const querySerializer = createQuerySerializer();

export let openApiClient: Client = createClientCustom();

// https://stackoverflow.com/a/69852402
type OmitNever<T> = { [K in keyof T as T[K] extends never ? never : K]: T[K] };
// Filter out paths by those that are gettable
type GetPath = OmitNever<{
    [T in keyof paths]: paths[T] extends { get: unknown } ? paths[T] : never;
}>;
// Then, allow an API caller to invalidate a resource
export async function invalidateGettableUrl<T extends keyof GetPath>(
    pathname: T,
    path?: Record<string, unknown>,
) {
    const url = createFinalURL<paths>(pathname, {
        querySerializer,
        baseUrl,
        params: { path },
    });
    await invalidate(url);
}

// https://github.com/drwpow/openapi-typescript/issues/1687
// thx
export async function dataOrThrow<TData, TResponse, TError>(
    apiResponse: Promise<{
        response: TResponse;
        data?: TData;
        error?: TError;
    }>,
): Promise<{
    data: TData;
}> {
    const { data, error } = await apiResponse;
    if (error !== undefined || data === undefined) {
        console.error("hit error", error);
        const exc = error
            ? new Error(JSON.stringify(error))
            : new Error("No data");
        throw exc;
    }

    return {
        data: data,
    };
}
