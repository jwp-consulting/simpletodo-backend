import type { Handle, HandleFetch } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
    const response = await resolve(event, {
        // Potentially too broad
        // See https://github.com/sveltejs/kit/discussions/7027
        filterSerializedResponseHeaders: () => true,
    });

    return response;
};

// Rewrite /api and /ws URL to go to backend directly using the
// VITE_WS_ENDPOINT_REWRITE_TO and VITE_API_ENDPOINT_REWRITE_TO environment
// variables
export const handleFetch: HandleFetch = async ({ request, fetch }) => {
    if (request.url.startsWith(__API_ENDPOINT__)) {
        request = new Request(
            request.url.replace(__API_ENDPOINT__, __API_ENDPOINT_REWRITE_TO__),
            request,
        );
    }
    return fetch(request);
};
