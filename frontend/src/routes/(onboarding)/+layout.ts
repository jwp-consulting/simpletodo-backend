// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
import { load } from "../(platform)/+layout";

// We re-export load from platform to have same functionality without
// duplication
export { load };

// Perhaps something in this hierarchy can be prerendered?
// TODO check
export const prerender = false;
