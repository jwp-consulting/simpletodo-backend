// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
import Sarus from "@anephenix/sarus";
import { writable } from "svelte/store";

import type {
    HasUuid,
    RepoGetter,
    SubscriptionType,
    WsResource,
    WsResourceContainer,
} from "$lib/types/stores";

import { browser } from "$app/environment";
import { backOff } from "exponential-backoff";
import { Mutex } from "$lib/utils/mutex";

function makeAbsoluteUrl(url: string): string {
    if (!url.startsWith("/")) {
        return url;
    }
    const { host, protocol } = window.location;
    const wsProtocol = protocol === "https:" ? "wss://" : "ws://";
    return `${wsProtocol}${host}${url}`;
}

type EventListener = (resp: WsResponse) => void;

type WsRequest =
    | { action: "subscribe"; resource: SubscriptionType; uuid: string }
    | { action: "unsubscribe"; resource: SubscriptionType; uuid: string };
type WsResponse =
    | {
          kind:
              | "already_subscribed"
              | "not_subscribed"
              | "not_found"
              | "gone"
              | "subscribed"
              | "unsubscribed";
          resource: SubscriptionType;
          uuid: string;
      }
    | {
          kind: "changed";
          resource: SubscriptionType;
          uuid: string;
          content: unknown;
      };

type ConnectionState =
    | { kind: "undefined" }
    | {
          kind: "connecting" | "opened" | "closed" | "reopened" | "errored";
          sarus: Sarus;
          listeners: Set<Listener>;
      };

let connectionState: ConnectionState = { kind: "undefined" };

interface Listener {
    resource: Resource;
    kind: WsResponse["kind"][];
    callback: EventListener;
    reconnect: Reconnector;
}

function onMessage(event: MessageEvent<string>) {
    if (connectionState.kind === "undefined") {
        throw new Error("Called onMessage while not connected");
    }
    const message = JSON.parse(event.data) as WsResponse;
    const handled = [...connectionState.listeners].some((listener) => {
        if (message.resource !== listener.resource.resource) {
            return false;
        }
        if (message.uuid !== listener.resource.uuid) {
            return false;
        }
        if (!listener.kind.includes(message.kind)) {
            return false;
        }
        listener.callback(message);
        return true;
    });
    if (!handled) {
        console.error("Message not handled:", message);
    }
}

function onOpen(_event: Event) {
    switch (connectionState.kind) {
        case "connecting":
            console.debug("Connection opened");
            connectionState.kind = "opened";
            break;
        case "closed": {
            console.debug("Connection reopened");
            connectionState.kind = "reopened";
            const reconnectingListeners = [...connectionState.listeners];
            // We flush the listeners, since otherwise we'd try to unsubscribe
            // the old "changed" listeners
            connectionState.listeners.clear();

            reconnectingListeners.forEach((listener) => {
                console.debug(
                    "Trying to reconnect listener for resource",
                    listener.resource.resource,
                    "uuid",
                    listener.resource.uuid,
                    "kinds",
                    listener.kind,
                );
                listener.reconnect();
            });
            break;
        }
        default:
            break;
    }
}

function onClose(_event: Event) {
    console.debug("Connection closed");
    connectionState.kind = "closed";
}

function onError(event: Event) {
    console.error("Error", event);
    connectionState.kind = "errored";
}

function sendWs(request: WsRequest) {
    if (connectionState.kind === "undefined") {
        const url = makeAbsoluteUrl(`${__WS_ENDPOINT__}/workspace/change`);
        const sarus = new Sarus({
            url,
            eventListeners: {
                open: [onOpen],
                close: [onClose],
                error: [onError],
                message: [onMessage],
            },
        });
        connectionState = {
            kind: "connecting",
            sarus,
            listeners: new Set(),
        };
    }
    console.debug("Sending ws message", request);
    connectionState.sarus.processMessage(JSON.stringify(request));
}

function addListener(listener: Listener) {
    if (connectionState.kind === "undefined") {
        throw new Error("Can't add listener if not connected");
    }
    if (connectionState.listeners.has(listener)) {
        console.error("Listener already added", listener);
        throw new Error("Listener already added");
    }
    connectionState.listeners.add(listener);
}

function removeListener(listener: Listener) {
    if (connectionState.kind === "undefined") {
        throw new Error("Can't add listener if not connected");
    }
    if (!connectionState.listeners.has(listener)) {
        console.error("Listener already removed:", listener);
        throw new Error("Listener already removed");
    }
    connectionState.listeners.delete(listener);
}

interface Resource {
    resource: SubscriptionType;
    uuid: string;
}

async function unsubscribeFromResource(resource: Resource) {
    console.debug("Unsubscribing from", resource);
    sendWs({ action: "unsubscribe", ...resource });
    const done = new Promise<"clean" | "crashed">((resolve, reject) => {
        const disconnectedCb = (response: WsResponse) => {
            if (response.kind === "not_subscribed") {
                reject(
                    new Error(
                        `Never subscribed to resource: ${JSON.stringify(
                            resource,
                        )}`,
                    ),
                );
                return;
            }
            console.debug("Unsubscribed from", resource);
            removeListener(unsubscribeListener);
            resolve("clean");
        };
        const unsubscribeListener: Listener = {
            resource,
            kind: ["unsubscribed", "not_subscribed"],
            callback: disconnectedCb,
            reconnect() {
                resolve("crashed");
            },
        };
        addListener(unsubscribeListener);
    });
    return await done;
}

type Reconnector = () => void;

type AsyncUnsubscriber = () => Promise<void>;

type SubscribeResult =
    | { kind: "subscribed"; unsubscriber: AsyncUnsubscriber }
    | { kind: "server" };

async function subscribeToResource(
    resource: Resource,
    listener: EventListener,
    reconnect: Reconnector,
): Promise<SubscribeResult> {
    if (!browser) {
        return { kind: "server" };
    }
    let state:
        | "subscribing"
        | "subscribed"
        | "unsubscribing"
        | "unsubscribed" = "subscribing";
    const messageListener: Listener = {
        resource,
        kind: ["gone", "changed"],
        callback: listener,
        reconnect,
    };

    const unsubscribe = async () => {
        if (state === "unsubscribed") {
            throw new Error("Already unsubscribed");
        } else if (state === "unsubscribing") {
            console.debug("Already unsubscribing");
            return;
        } else if (state === "subscribing") {
            throw new Error("Never subscribed");
        }
        state = "unsubscribing";
        console.debug("Cleaning up listener for", resource);
        const result = await unsubscribeFromResource(resource);
        if (result === "clean") {
            removeListener(messageListener);
        } else {
            console.info(
                "Connection crashed while unsubscribing from",
                resource,
            );
        }
        state = "unsubscribed";
    };
    sendWs({ action: "subscribe", ...resource });

    const established = new Promise<AsyncUnsubscriber>((resolve, reject) => {
        const establishedConnectionCb = (response: WsResponse) => {
            if (response.kind === "not_found") {
                reject(
                    new Error(
                        `Resource ${JSON.stringify(resource)} not found`,
                    ),
                );
                return;
            }
            if (response.kind === "already_subscribed") {
                console.info("Already subscribed to resource", resource);
            }

            console.debug(
                "Subscribed to resource",
                resource.resource,
                "uuid",
                resource.uuid,
            );
            state = "subscribed";
            removeListener(subscribedListener);
            addListener(messageListener);
            resolve(unsubscribe);
        };
        const subscribedListener: Listener = {
            resource,
            kind: ["not_found", "already_subscribed", "subscribed"],
            callback: establishedConnectionCb,
            reconnect() {
                reject(
                    new Error(
                        `Reconnected while subscribing to ${JSON.stringify(
                            resource,
                        )}`,
                    ),
                );
            },
        };
        addListener(subscribedListener);
    });
    return { kind: "subscribed", unsubscriber: await established };
}

/* Subscribable WS Store
 *
 *  ┌─────┐   loadUuid  ┌─────┐ ──────────────┐
 *  │Start│────────────►│Ready│               │ subscription update:
 *  └─────┘             └─────┘ ◄─────────────┘ set(newValue)
 *       .---.          | ▲ │
 *       |SSR|<---------. │ │ loadUuid
 *       .---.  !browser  │ │ reconnect
 *                        └─┘
 *
 * This thing basically just passes on ws updates to subscribers, plus
 * one initial load
 * Now, it also contains code to handle SSR
 */

type WsStoreState<T> =
    | {
          kind: "start";
      }
    | {
          kind: "ssr";
          value: T | undefined;
          uuid: string;
      }
    | {
          kind: "ready";
          uuid: string;
          unsubscriber: AsyncUnsubscriber;
          value: T | undefined;
      };

export function createWsStore<T extends HasUuid>(
    resource: SubscriptionType,
    getter: RepoGetter<T>,
): WsResource<T> {
    type State = WsStoreState<T>;
    let state: State = { kind: "start" };
    const loadMutex = new Mutex();

    const { subscribe, set } = writable<WsResourceContainer<T>>(
        {
            or: (t: T) => t,
            orPromise: (t: Promise<T>) => t,
            value: undefined,
        },
        () => stop,
    );

    const reset = () => {
        set({
            or: (t: T) => t,
            orPromise: (t: Promise<T>) => t,
            value: undefined,
        });
        state = { kind: "start" };
    };

    const resetAndUnsubscribe = async () => {
        if (state.kind === "start") {
            console.error("Already reset");
            return;
        }
        if (state.kind === "ssr") {
            return;
        }
        console.debug("Resetting resource", resource, "uuid", state.uuid);

        const release = await loadMutex.obtain();
        try {
            await state.unsubscriber();
        } finally {
            release();
        }

        reset();
    };

    const stop = () => {
        if (state.kind === "start") {
            return;
        }
        if (state.kind === "ssr") {
            return;
        }
        resetAndUnsubscribe().catch((error: unknown) =>
            console.error("Error when resetting", error),
        );
    };

    const onMessage: EventListener = (resp: WsResponse) => {
        if (state.kind === "start") {
            throw new Error("State.kind is start");
        }
        if (resp.kind === "gone") {
            reset();
        } else if (resp.kind === "changed") {
            const value = resp.content as T;
            set({
                or: () => value,
                value,
                orPromise: () => Promise.resolve(value),
            });
        } else {
            throw new Error("resp.kind is not 'changed'");
        }
    };

    const reconnect: Reconnector = async () => {
        if (state.kind !== "ready") {
            // This happens when
            // 1. loadUuid is called
            // 2. backOff(subscribeToResource) is called
            // 3. connection crashes after calling addListener(messageListener),
            // 4. reconnect is called before backOff can resolve, state not set
            // to "ready"
            // This is a race condition, since loadUuid might finish earlier
            // and set the state to ready, in which case we will not encounter
            // this error
            // Since the inner of backOff will be rejected, we can ignore the
            // race condition for now, backOff will do its thing again.
            console.info(
                "Trying to reconnect, despite not being ready on resource",
                resource,
            );
            return;
        }
        const { uuid } = state;
        console.error(
            "Connection closed, reconnecting to resource",
            resource,
            "uuid",
            uuid,
        );

        const release = await loadMutex.obtain();
        try {
            const result = await backOff(() =>
                subscribeToResource({ resource, uuid }, onMessage, reconnect),
            );
            if (result.kind === "server") {
                console.error("Trying to reconnect in server");
                return;
            }
            console.debug("Reconnected to resource", resource, "uuid", uuid);
            state = { ...state, unsubscriber: result.unsubscriber };
        } finally {
            release();
        }
    };

    const loadUuid = async (uuid: string): Promise<T | undefined> => {
        const oldState = state;
        type Result =
            | { kind: "newUuid"; value: T; unsubscriber?: AsyncUnsubscriber }
            | { kind: "noResult"; value: undefined }
            | {
                  kind: "sameUuid";
                  value: T | undefined;
                  unsubscriber?: AsyncUnsubscriber;
              };
        let result: Result | undefined = undefined;
        const release = await loadMutex.obtain();
        try {
            switch (oldState.kind) {
                case "ssr":
                case "ready": {
                    if (oldState.uuid === uuid) {
                        if (oldState.kind === "ready") {
                            result = {
                                kind: "sameUuid",
                                value: oldState.value,
                                unsubscriber: oldState.unsubscriber,
                            };
                        } else {
                            result = {
                                kind: "sameUuid",
                                value: oldState.value,
                            };
                        }
                    } else {
                        if (oldState.kind === "ready") {
                            await oldState.unsubscriber();
                        }
                        const getterResult = await backOff(() => getter(uuid));
                        if (getterResult) {
                            const subscriptionResult = await backOff(() =>
                                subscribeToResource(
                                    { resource, uuid },
                                    onMessage,
                                    reconnect,
                                ),
                            );
                            result = {
                                kind: "newUuid",
                                value: getterResult,
                                unsubscriber:
                                    subscriptionResult.kind === "subscribed"
                                        ? subscriptionResult.unsubscriber
                                        : undefined,
                            };
                        } else {
                            result = {
                                kind: "noResult",
                                value: getterResult,
                            };
                        }
                    }
                    break;
                }
                case "start": {
                    const getterResult = await backOff(() => getter(uuid));
                    if (getterResult === undefined) {
                        result = { kind: "noResult", value: getterResult };
                    } else {
                        const subscriptionResult = await backOff(() =>
                            subscribeToResource(
                                { resource, uuid },
                                onMessage,
                                reconnect,
                            ),
                        );
                        result = {
                            kind: "newUuid",
                            value: getterResult,
                            unsubscriber:
                                subscriptionResult.kind === "subscribed"
                                    ? subscriptionResult.unsubscriber
                                    : undefined,
                        };
                    }
                    break;
                }
            }
        } finally {
            release();
        }

        switch (result.kind) {
            case "sameUuid":
                return result.value;
            case "newUuid": {
                const { value } = result;
                set({
                    or: () => value,
                    orPromise: () => Promise.resolve(value),
                    value,
                });
                if (result.unsubscriber) {
                    state = {
                        ...oldState,
                        kind: "ready",
                        uuid,
                        unsubscriber: result.unsubscriber,
                        value,
                    };
                } else {
                    state = {
                        ...oldState,
                        kind: "ssr",
                        uuid,
                        value,
                    };
                }
                return result.value;
            }
            case "noResult": {
                const { value } = result;
                set({
                    or: (t: T) => t,
                    orPromise: (t: Promise<T>) => t,
                    value,
                });
                return result.value;
            }
        }
    };

    return { loadUuid, subscribe };
}
// Online connection

export const online = writable(true);

if (browser) {
    setTimeout(() => {
        online.set(navigator.onLine);
    }, 1000);

    window.addEventListener("offline", () => {
        online.set(false);
    });

    window.addEventListener("online", () => {
        online.set(true);
    });
}
