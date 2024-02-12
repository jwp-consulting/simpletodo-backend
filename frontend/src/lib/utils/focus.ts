// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
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
function getFirstAndLastFocusable(inside: HTMLElement): {
    first: HTMLElement;
    last: HTMLElement;
} {
    const focusables = inside.querySelectorAll("a, button, input");
    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    if (!(first instanceof HTMLElement)) {
        throw new Error("Expected HTMLElement");
    }
    if (!(last instanceof HTMLElement)) {
        throw new Error("Expected HTMLElement");
    }
    return { first, last };
}

export function keepFocusInside(inside: HTMLElement): () => void {
    const listener = ({ target }: FocusEvent) => {
        if (!target) {
            throw new Error("Expected target");
        }
        if (!(target instanceof Node)) {
            throw new Error("Expected Node");
        }
        const { first, last } = getFirstAndLastFocusable(inside);
        const position = target.compareDocumentPosition(inside);
        const contained = position & Node.DOCUMENT_POSITION_CONTAINS;
        const preceding = position & Node.DOCUMENT_POSITION_PRECEDING;
        const following = position & Node.DOCUMENT_POSITION_FOLLOWING;
        if (contained) {
            // We are inside, nothing to do
            return;
        }
        if (preceding) {
            last.focus();
        } else if (following) {
            first.focus();
        } else {
            throw new Error(`Unexpected position ${position}`);
        }
    };
    document.addEventListener("focusin", listener);
    return () => {
        document.removeEventListener("focusin", listener);
    };
}
