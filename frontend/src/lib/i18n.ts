// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { addMessages, getLocaleFromNavigator, init } from "svelte-i18n";
// TODO use register

import en from "$messages/en";
import { browser } from "$app/environment";

const defaultLocale = "en";

function initializeI18n() {
    addMessages("en", en);
    const initialization = init({
        fallbackLocale: defaultLocale,
        initialLocale: browser ? getLocaleFromNavigator() : "en",
    });

    if (!initialization) {
        return;
    }

    initialization.catch((error: unknown) => {
        console.error("Something went wrong when adding messages:", error);
    });
}

initializeI18n();
