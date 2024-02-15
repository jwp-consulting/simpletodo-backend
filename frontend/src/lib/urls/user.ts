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
/*
 * Contain user related URL constants
 */
export const changePasswordUrl = "/user/profile/change-password";
export const changedPasswordUrl = "/user/profile/changed-password";
export const updateEmailAddressUrl = "/user/profile/update-email-address";
// These two URLs are needed for the email change flow, but not implemented yet
// TODO
export const requestedEmailAddressUpdateUrl =
    "/user/profile/update-email-address/requested";
export const confirmedEmailAddressUpdateUrl =
    "/user/profile/update-email-address/confirmed";
// Auth
export const logInUrl = "/user/log-in";
export const logOutUrl = "/user/log-out";
export const signUpUrl = "/user/sign-up";
export const requestPasswordResetUrl = "/user/request-password-reset";
// For when a reset request has been sent out
export const requestedPasswordResetUrl = "/user/requested-password-reset";
// For when the user has reset their password
export const resetPasswordUrl = "/user/reset-password";
export const sentEmailConfirmationLinkUrl =
    "/user/sent-email-confirmation-link";

export function getLogInWithNextUrl(next: string): string {
    const encoded = encodeURIComponent(next);
    return `/user/log-in?next=${encoded}`;
}
