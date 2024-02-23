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

import BasicsHelpPage from "./en/help/basics.md?raw";
import BillingHelpPage from "./en/help/billing.md?raw";
import FiltersHelpPage from "./en/help/filters.md?raw";
import LabelsHelpPage from "./en/help/labels.md?raw";
import QuotaHelpPage from "./en/help/quota.md?raw";
import RolesHelpPage from "./en/help/roles.md?raw";
import TasksHelpPage from "./en/help/tasks.md?raw";
import TrialHelpPage from "./en/help/trial.md?raw";
import WorkspaceBoardSectionsHelpPage from "./en/help/workspace-board-sections.md?raw";
import WorkspaceBoardsHelpPage from "./en/help/workspace-boards.md?raw";
import WorkspaceUsersHelpPage from "./en/help/workspace-users.md?raw";
import WorkspacesHelpPage from "./en/help/workspaces.md?raw";
import type { MessageDirectory } from "./types";

const messages: MessageDirectory = {
    "overlay": {
        "constructive": {
            "update-workspace-board": {
                title: "Edit workspace board",
                form: {
                    title: {
                        label: "workspace board name",
                        placeholder: "Enter a workspace board name",
                    },
                },
                cancel: "Cancel",
                save: "Save",
            },
            "create-workspace-board": {
                "title": "Create workspace board",
                "form": {
                    title: {
                        label: "Workspace board name",
                        placeholder: "Enter a workspace board name",
                    },
                },
                "cancel": "Cancel",
                "create-board": "Create",
            },
            "invite-workspace-user": {
                title: "Invite workspace user",
                form: {
                    email: {
                        label: "Enter the email address of the user you would like to invite",
                        placeholder: "workspace-user@mail.com",
                        validation: {
                            ok: "Email address looks good",
                        },
                    },
                },
                error: {
                    general: "An unknown error occured",
                    field: "Please correct the errors above and submit one more time",
                },
                cancel: "Cancel",
                invite: "Invite",
            },
            "create-workspace-board-section": {
                "title": "Create new workspace board section",
                "form": {
                    title: {
                        label: "New workspace board section name",
                        placeholder: "New workspace board section name",
                    },
                },
                "cancel": "Cancel",
                "create-section": "Create",
            },
            "update-workspace-board-section": {
                title: "Edit workspace board section",
                form: {
                    title: {
                        label: "Workspace board section title",
                        placeholder: "Enter new workspace board section title",
                    },
                },
                cancel: "Cancel",
                update: "Save",
            },
            "recover-workspace-board": {
                title: "Recover workspace board ''{title}''?",
                notice: "Recovering this workspace board returns it to the dashboard. You will be redirected to the workspace board after the recovery has finished.",
                cancel: "Cancel",
                submit: {
                    start: "Recover workspace board",
                    submitting: "Recovering ...",
                },
                error: "An error has happened while recovering the workspace board. The error details are {details}",
            },
        },
        "destructive": {
            "delete-label": {
                title: "Delete label",
                body: "Would you like to delete the ''{label}'' label?",
                button: "Delete",
                warning: "This action cannot be undone.",
            },
            "delete-workspace-user": {
                title: "Remove workspace user",
                body: "Would you like to remove ''{workspaceUser}'' from this workspace?",
                warning: "This action cannot be undone.",
                button: "Remove",
            },
            "delete-workspace-board-section": {
                title: "Delete workspace board section",
                body: "Would you like to delete the ''{workspaceBoardSection}'' workspace board section?",
                warning:
                    "Deleting this section will also delete all tasks within it.",
                button: "Delete",
            },
            "delete-task": {
                title: "Delete task",
                body: "Would you like to delete the ''{task}'' task?",
                warning: "This action cannot be undone.",
                button: "Delete",
            },
            "delete-selected-tasks": {
                title: "Delete selected tasks",
                body: "Would you like to delete {count, number} selected tasks?",
                warning: "This action cannot be undone.",
                button: "Delete",
            },
            "archive-workspace-board": {
                title: "Archive workspace board",
                body: "Would you like to archive this ''{workspaceBoard}'' workspace board? You will be redirected to the workspace board archive page after archival has finished.",
                warning:
                    "You can always review and recover archived workspace boards in the archives section",
                button: "Archive",
            },
            "delete-workspace-board": {
                title: "Delete workspace board",
                body: "Would you like to delete this ''{workspaceBoard}'' workspace board?",
                warning: "This action cannot be undone",
                button: "Delete",
            },
            "cancel": "Cancel",
        },
        "context-menu": {
            "profile": {
                "my-profile": "My profile",
                "log-out": "Log out",
            },
            "workspace": {
                "select-workspace": "Switch to workspace:",
            },
            "side-nav": {
                "minimise-sidebar": "Minimise sidebar",
                "expand-sidebar": "Expand sidebar",
                "go-to-archive": "Go to archive",
                "workspace-settings": "Workspace settings",
            },
            "workspace-board": {
                "edit-board": "Edit board",
                "archive-workspace-board": "Archive board",
            },
            "workspace-board-section": {
                "expand-section": "Expand section",
                "collapse-section": "Collapse section",
                "switch-previous": "Switch with previous section",
                "switch-next": "Switch with next section",
                "edit-title": "Edit section title",
                "delete-workspace-board-section": "Delete section",
            },
            "task": {
                "open-task": "Open task",
                "move-to-section": "Move to section",
                "move-to-top": "Move to top",
                "move-to-bottom": "Move to bottom",
                "copy-link": "Copy link",
                "delete-task": "Delete task",
            },
            "help": {
                "help-and-tips": "Help and tips",
                "blog": "Blog",
            },
            "permissions": {
                "all-roles": "All roles",
                "owner": "Owner",
                "maintainer": "Maintainer",
                "member": "Member",
                "observer": "Observer",
            },
        },
    },
    // TODO find out if we can factor this into somewhere
    "label": {
        "apply-label": "Assign label",
    },
    "dashboard": {
        "actions": {
            "add-workspace-board-section": "Add workspace board section",
        },
        "task-card": {
            "add-label": "Assign label",
            "task-number": "#{number}",
        },
        "search": {
            "not-found": {
                title: "No tasks found for ''{search}''",
                explanation:
                    "No tasks were found for the search terms you specified. You can either try a new search using the search form above or go back and view entire the workspace board.",
                back: "Go back to workspace board",
            },
            "found": {
                title: "Showing results for ''{search}''",
                back: "Go back to workspace board",
            },
        },
        "create-board": "Create new workspace board",
        "boards": "Workspace boards",
        "workspace-users": "Workspace users",
        "workspace-user-name": "Workspace user name",
        "filter-workspace-users": "Filter workspace users",
        "search-task": {
            button: "Search tasks",
            input: { placeholder: "Enter search terms", label: "Task search" },
        },
        "assign-user": "Assign workspace user",
        "no-sections": {
            message: "There are no sections in this workspace board.",
            prompt: "Add a section",
        },
        "section": {
            "empty": {
                message: "No tasks in this section.",
                prompt: "Add a task here",
            },
            "add-task": "Add task",
        },
        "no-user-assigned": "No workspace user assigned",
        "error": {
            "title": "Error:",
            "description":
                "We apologize for the error. There was an error loading your dashboard. The error details are as follows:",
            "what-to-do": {
                message:
                    "Unfortunately this means we are unable to load this page properly. To help resolve this:",
                options: {
                    "help": "Visit the help page for common solutions",
                    "contact-us": "Contact us",
                },
            },
        },
        "side-nav": {
            "no-workspace": {
                title: "No workspace selected",
                message:
                    "To use a workspace, click the workspace selector above and select the workspace you would like to use.",
            },
            "workspace-selector": {
                "select": "Select a workspace",
                "context-menu": "Open workspace context menu",
            },
            "quota": {
                status: {
                    trial: { label: "Trial workspace", help: "Learn more" },
                    inactive: {
                        label: "Inactive workspace",
                        help: "Learn more",
                    },
                },
            },
            "workspace-boards": {
                empty: {
                    message:
                        "You have no workspace boards available. Please check the workspace board archive and recover a workspace board from there. Alternatively you can also create a new workspace board using the button below.",
                    archive: "Go to archive",
                },
            },
            "filter-labels": {
                "title": "Filter labels",
                "create-new-label": "Create new label",
                "input": {
                    label: "Label name",
                    placeholder: "Filter by label name",
                },
                "create-input": {
                    label: "Label name",
                    placeholder: "New label name",
                },
                "color": {
                    prompt: "Select label color",
                    colors: {
                        orange: "Orange",
                        pink: "Pink",
                        blue: "Blue",
                        purple: "Purple",
                        yellow: "Yellow",
                        red: "Red",
                        green: "Green",
                    },
                },
                "update-input": {
                    label: "Label name",
                    placeholder: "New name for label",
                },
                "state": {
                    update: "Updating label {label}",
                    create: "New label",
                },
                "errors": {
                    create: "The label could not be created. Please make sure you entered a valid name and color and try again.",
                    update: "The label could not be updated. Please make sure you entered a valid name and color and try again.",
                },
                "save": "Save",
                "cancel": "Cancel",
            },
        },
    },
    "workspace-board-archive": {
        title: "Workspace board archive",
        card: {
            recover: "Recover",
            delete: "Delete",
            archived: "Archived on {archived, date, medium}",
        },
        empty: "No workspace boards have been archived.",
    },
    // Factor this into a general error section
    "page404": {
        title: "Lost your way?",
        body: "The page you're looking for doesn't exist.",
        home: "Take me home",
    },
    // Factor this into a general error section
    "connection-status": {
        "disconnected": "Not connected to Projectify",
        "back-to-landing": "Back to landing page",
    },
    // TODO factor this into "dashboard"?
    "filter-label": {
        all: "All labels",
        none: "No label",
    },
    // TODO factor this into "dashboard"?
    "filter-workspace-user": {
        "all-users": "All users",
        "assigned-nobody": "Assigned to nobody",
    },
    "onboarding": {
        "continue": "Continue",
        "back": "Back",
        "welcome": {
            title: "Welcome",
            prompt: [
                "In the following steps you will create a new workspace and create your first task.",
                "You can use the workspace in trial mode at the beginning, and upgrade to a paid version anytime by going to the workspace settings.",
            ],
            help: {
                "trial-mode-features":
                    "Learn more about features available during trial mode",
            },
        },
        "about-you": {
            title: "About you",
            input: {
                label: "Preferred name (optional)",
                placeholder: "Your preferred name",
            },
            prompt: "Tell us your preferred name. You can also keep it empty and continue by clicking the button below.",
            greeting: {
                "with-name": "Welcome, {name}! 👋",
                "without-name": "Welcome! 👋",
            },
        },
        "new-workspace": {
            "title": {
                "with-name": "Let’s set up your first workspace, {who}.",
                "without-name": "Let's set up your first workspace.",
            },
            "prompt": "You can create and manage numerous workspaces",
            "has-workspace":
                "It looks like you already have a workspace, would you like to create a workspace board?",
            "label": "Workspace name",
            "placeholder": "e.g. the name of your company",
            "default-name": "Your workspace",
        },
        "new-workspace-board": {
            "title": "Add your first board",
            "prompt": [
                "You can create unlimited boards per workspace.",
                "They help you to focus on different projects you may be working on.",
            ],
            "input": {
                label: "Board title",
                placeholder: "Release spring Aug 2023",
            },
            "default-name": "Your board",
            "workspace-board-exists": {
                message:
                    'It looks like you already have a workspace board called "{title}". Would you like to continue adding a task for it?',
                prompt: 'Continue adding task to "{title}"',
            },
        },
        "new-task": {
            "title": "What is a task you’d like to complete?",
            "workspace-board-section-title": "To do",
            "default-name": "Your task",
            "prompt": {
                location:
                    'This task will be placed in a section called "{workspaceBoardSectionTitle}"',
                exists: 'It looks like you already have a workspace board section called "{workspaceBoardSectionTitle}". We will now create a task  and place it into that workspace board section.',
                explanation:
                    "Tasks can be further divided into sub tasks and contain detailed descriptions.",
            },
            "input": {
                label: "Task name",
                placeholder: "E.g., 'Add user permission dropdown'",
            },
        },
        "new-label": {
            "title": 'Create a label for "{taskTitle}"',
            "prompt": "Labels help you to filter between the types of tasks.",
            "input": {
                placeholder: "e.g., Bug",
                label: "Label name",
            },
            "error":
                "Please check the label name you have specified one more time and try again.",
            "default-name": "Your label",
        },
        "assign-task": {
            "title": 'Task "{taskTitle}" has been assigned to you!',
            "continue": "Get started",
            "prompt": {
                "finished": "You’re all set!",
                "adding-workspace-users":
                    "If you wish to add new workspace users to your workspace, please go to the workspace settings menu next to your workspace name.",
            },
            "follow-up": {
                "billing-help": "Learn more about workspace billing settings",
                "go-to-billing-settings": "Go to workspace billing settings",
            },
        },
        "error": {
            "title": "Onboarding failed",
            "message":
                "The last onboarding step did not finish correctly. Please try the onboarding process more time by clicking the button below.",
            "error-detail": "Error message:",
            "try-again": "Continue onboarding",
        },
    },
    "auth": {
        "sign-up": {
            "title": "Sign up",
            "sub-title": "Sign up and start a free trial",
            "email": {
                label: "Email",
                placeholder: "Enter your email",
                missing: "Must enter email",
            },
            "password": {
                label: "Password",
                placeholder: "Enter your password",
                missing: "Must enter password",
            },
            "tos": {
                label: "I agree to the Terms of Service",
                missing: "Must agree to Terms of Service",
            },
            "privacy-policy": {
                label: "I agree to the Privacy Policy",
                missing: "Must agree to Privacy Policy",
            },
            "submit": {
                ready: "Sign up",
                submitting: "Signing you up",
            },
            "already-have-an-account": "Already have an account?",
            "generic-error":
                "We are unable to sign you up with these credentials. Please confirm whether you have not signed up with this email already.",
            "log-in-here": "Log in here",
        },
        "confirmation-link-sent": {
            "header": "Email confirmation link sent",
            "illustration-alt":
                "Happy bird mascot indicating that a email confirm email is on its way to you",
            "body": "Please go to your email and follow the instructions to activate your account",
            "back-to-homepage": "Back to homepage",
        },
        "logout": {
            "success": "You have been logged out",
            "log-back-in": "Log in again",
            "landing": "Go to landing",
        },
        "log-in": {
            "title": "Log in",
            "email": {
                label: "Email",
                placeholder: "Enter your email",
                missing: "Must enter email",
                valid: "Email address found",
            },
            "password": {
                label: "Password",
                placeholder: "Enter your password",
                missing: "Must enter password",
            },
            "forgot-password": "Forgot password",
            "submit": {
                start: "Log in",
                submitting: "Logging you in...",
            },
            "no-account": "Don't have an account yet?",
            "error": {
                credentials:
                    "Invalid credentials. Please see the errors above.",
                other: "Invalid credentials. Please check email and password.",
            },
            "sign-up-here": "Sign up here",
        },
        "request-password-reset": {
            "title": "Reset your password",
            "explanation":
                "Enter the email associated with your account and we'll send you a link to reset your password.",
            "email": {
                label: "Email",
                placeholder: "Enter your email",
            },
            "submit": {
                start: "Send password reset link",
                submitting: "Submitting form...",
            },
            "return-to-log-in": "Return to log in",
            "error": {
                generic:
                    "Something went wrong when requesting your password reset link. Please try again using this form, or contact support if you have any questions",
                validation:
                    "Please check the fields above again for errors and submit again",
            },
        },
        "requested-password-reset": {
            "title": "Password reset requested",
            "message":
                "You have requested for your password to be reset and will receive an email with password reset instructions soon. Please check your email inbox.",
            "troubleshooting":
                "If you do not receive any email, you can request a new password email to be sent by using the email. Please contact support if you have any questions.",
            "request-again": "Request password reset again",
        },
        "confirm-password-reset": {
            "title": "Reset your password",
            "password-1": {
                label: "New password",
                placeholder: "Enter new password",
                validation: {
                    "no-match":
                        "The password entered here must match the password entered under 'Confirm new password'",
                },
            },
            "password-2": {
                label: "Confirm new password",
                placeholder: "Confirm new password",
                validation: {
                    "no-match":
                        "The password entered here must match the password entered under 'New password'",
                },
            },
            "validation": {
                "no-match":
                    "The two passwords you have entered do not match. Please check one more time if you have entered the same password in both fields.",
            },
            "submit": {
                start: "Reset password",
                submitting: "Resetting password...",
                error: "Reset password (try again)",
            },
            "error":
                "Your password could not be reset. Please try again. If you have previously reset your password using this form, please try requesting a password reset one more time using the link below.",
            "request-password-reset": "Request password reset again",
        },
        "reset-password": {
            title: "Password reset complete",
            message:
                "Your password was reset successfully. You may now proceed and log in with your email address and the password that you have just entered.",
            continue: "Continue to log in",
        },
        "confirm-email": {
            success: {
                title: "Email address confirmed",
                message:
                    "Your email address was confirmed successfully. You may now proceed to log in.",
                continue: "Continue to log in",
            },
            error: {
                title: "Error while confirming email address",
                message:
                    "Unfortunately your email address could not be confirmed. The error code from the API was:",
                continue: "Contact support",
            },
        },
    },
    "task-screen": {
        "update": {
            "update": "Update task",
            "update-continue-editing": "Update task and stay",
        },
        "create": {
            "create": "Create task",
            "create-continue-editing": "Create task and stay",
        },
        "sub-tasks": {
            "title": "Sub tasks",
            "completion": "{progress, number, percent} complete",
            "empty-state":
                "You have not added any sub tasks yet. You can add a sub task by clicking the add sub task button.",
            "empty-state-read-only":
                "This task has no sub tasks. You can add sub tasks by going to the task edit screen and clicking the add sub task button from there.",
            "add-sub-task": {
                button: "Add sub task",
            },
        },
        "new-task-breadcrumb": "New task (currently creating)",
        // TODO organize this as "form": {} with labels and placeholders
        "new-task-name": "New task name",
        "description": "Description",
        "labels": "Labels",
        "select-due-date": "Select due date",
        "due-date": "Due date",
        "edit": "Edit",
        "task-title": "Task title",
        "assignee": "Assignee",
        "enter-a-subtask": "Enter a subtask",
    },
    "user-account-settings": {
        "title": "User account settings",
        "overview": {
            "preferred-name": {
                label: "Preferred name (optional)",
                placeholder: "Enter your preferred name",
            },
            "current-email-address": {
                "label": "Your current email address",
                "update-email-address": "Update email address",
            },
            "profile-picture": {
                prompt: "Upload a profile picture",
                current: "Your current profile picture",
                remove: "Remove profile picture",
            },
            "other-actions": {
                "title": "Other settings",
                "change-password": "Change password",
            },
            "delete-account": {
                title: "Account deletion",
                message:
                    "If you would like to delete your account, please send us an email using the link below. We have not implemented self-serve account deletion at this point, and would like to apologize for the inconvenience.",
                label: "Request account deletion (opens email client)",
                email: "mailto:hello@projectifyapp.com?subject=Account+deletion",
            },
            "cancel": "Cancel",
            "save": "Save changes",
        },
        "update-email-address": {
            "title": "Update email address",
            "current-email": "Your current email address is ''{email}''.",
            "current-password": {
                label: "Current password",
                placeholder: "Enter your current password",
                valid: "Correct password",
            },
            "new-email": {
                label: "New email",
                placeholder: "Enter your new email address",
                valid: "Valid new email",
            },
            "cancel": "Go back",
            "save": "Update email",
            "error": {
                general:
                    "An unknown error has occured and your email update has not finished",
                field: "Please check the errors above and try one more time",
            },
            "requested": {
                "title": "Email address update requested",
                "message":
                    "We will send an email with to your new email address containing a link that you can click to confirm your new email address. Please follow the instructions in the email.",
                "back-to-profile": "Go back to profile",
            },
            "confirm": {
                title: "Confirming new email address",
                submitting:
                    "We are confirming your new email address using the token that is contained in this page's URL.",
                error: {
                    "general":
                        "An unknown error has occured and your email address could not be updated. Please try again or contact us if you have any questions",
                    "confirmation-token":
                        "The confirmation token provided in the URL you used to open this page is not valid. This means that you might have already changed your email address, or that you have requested for your email address to be changed multiple times. Please try updating your email address one more time by following the link below. The error was: ''{error}''.",
                    "what-to-do": {
                        "title": "What to do",
                        "try-again":
                            "Try updating your email address one more time",
                        "contact-us": {
                            label: "Contact us via email",
                            email: "mailto:hello@projectifyapp.com?subject=Update+emai+address",
                        },
                    },
                },
            },
            "confirmed": {
                "title": "Email address updated successfully",
                "message":
                    "Your email address has been updated succesfully. You may now use your new email address to log in.",
                "back-to-profile": "Go back to profile",
            },
        },
        "change-password": {
            "title": "Change password",
            "current-password": {
                label: "Current password",
                placeholder: "Enter your password",
                correct: "Current password matches",
            },
            "new-password": {
                label: "New password",
                placeholder: "Enter the new password",
                correct: "This is a valid new password.",
            },
            "confirm-password": {
                label: "Confirm password",
                placeholder: "Confirm the new password",
            },
            "cancel": "Go back",
            "submit": {
                start: "Change password",
                submitting: "Changing password...",
            },
            "validation": {
                "must-match":
                    "'New password' and 'Confirm password' must match.",
                "field-errors":
                    "Please check any errors in the above fields and try submitting again.",
                "general-error":
                    "There was an error when changing your password. Please try again or contact support. The error details are: {details}",
            },
        },
        "changed-password": {
            "title": "Password changed",
            "message":
                "Your password has been changed. An email has been sent out to your email address to confirm the password change. You can use your new password to log in from now on.",
            "back-to-profile": "Back to profile",
        },
    },
    "workspace-settings": {
        "title": "Workspace settings",
        "general": {
            "title": "General",
            "save": "Save",
            "cancel": "Cancel",
            "workspace-name": {
                label: "Workspace name",
                placeholder: "Enter a workspace name",
            },
            "description": {
                label: "Description",
                placeholder: "Enter a description",
            },
            "picture": {
                "alt": "A picture used to identify this workspace",
                "no-picture": "No picture uploaded.",
                "label": "Upload a picture",
                "remove-picture": "Remove picture",
            },
        },
        "workspace-users": {
            "title": "Workspace users",
            "no-job-title": "No job title",
            "no-workspace-users-found":
                "No workspace users found for this search query. Please try another search.",
            "role": "Role",
            "workspace-user": "Workspace user",
            "invite-new-workspace-users": "Invite new workspace users",
            "invites": {
                title: "Workspace user invites",
                email: "Invited email",
                date: "Invited on",
                empty: "You have no open invites",
            },
            "edit-role": {
                label: "Edit role",
                self: "Can't edit own role",
                saving: "Saving...",
            },
            "actions": {
                action: "Action",
                remove: "Remove",
                uninvite: "Uninvite",
            },
            "help": {
                "title": "Help",
                "about-roles": "About roles",
                "about-workspace-users": "About workspace users",
            },
        },
        "billing": {
            "title": "Billing",
            "active": {
                "status": {
                    title: "Subscription status: Paid workspace",
                    explanation:
                        "You have a paid workspace. You can review your billing details and seat count using the 'Edit billing details' button below.",
                },
                "monthly-total": {
                    title: "Monthly total ({pricePerSeat, number, ::currency/USD} per seat/month):",
                    status: "{total, number, ::currency/USD}",
                },
                "seats": {
                    title: "Number of seats:",
                    status: "{seats} seats in total, {seatsRemaining} {seatsRemaining, plural, one {seat} other {seats}} remaining",
                    unlimited: "unlimited",
                },
                "edit-billing-details": "Edit billing details",
            },
            "unpaid": {
                status: {
                    title: "Trial mode",
                    explanation:
                        "You are currently using this workspace in trial mode. To create a subscription and use all available features for this workspace, please continue using the checkout below. Alternatively, you can enter a coupon code further below.",
                },
                cancelled: {
                    title: "Subscription cancelled",
                    explanation:
                        "Your subscription has been cancelled. If you want to reactivate your subscription, please resubscribe using the checkout form below.",
                },
                checkout: {
                    title: "Checkout",
                    seats: {
                        explanation:
                            "Select the amount of workspace seats. For each workspace user that is invited or added, a seat is used up.",
                        placeholder: "Number of workspace seats",
                        label: "Workspace seats",
                    },
                    action: "Go to checkout",
                },
                coupon: {
                    "title": "Use a coupon code",
                    "description":
                        "If someone has given you a coupon code, you can use it here to upgrade your workspace. Please refer to the details given to you for more information on what features will be unlocked for your workspace. If you have any questions, please ask the person who gave you the coupon code or contact us.",
                    "code": {
                        placeholder: "Enter coupon code",
                        label: "Coupon code",
                    },
                    "unknown-error": "An unknown error has occured",
                    "action": "Redeem coupon code",
                },
            },
            "custom": {
                status: {
                    title: "Custom subscription active",
                    explanation:
                        "You have activated a custom subscription for this workspace using a coupon code. If you have any questions about your subscription or if you would like to make changes, please contact us.",
                },
            },
            "contact-us":
                "Contact us if you have any questions regarding billing.",
            "billing-contact": "hello@projectifyapp.com",
        },
        "quota": {
            "title": "Quota",
            "explanation": {
                "quota-for":
                    "These are the quotas for the ''{title}'' workspace:",
                "no-quota": "No quotas apply to your workspace.",
            },
            "workspace-status": {
                label: "Workspace status:",
                full: "Full workspace",
                trial: "Trial workspace",
                inactive: "Inactive workspace",
            },
            "columns": {
                resource: "Resource",
                current: "Current",
                limit: "Limit",
            },
            "resource": {
                "labels": "Labels",
                "sub-tasks": "Sub tasks",
                "tasks": "Tasks",
                "task-labels": "Task labels",
                "workspace-boards": "Workspace boards",
                "workspace-board-sections": "Workspace board sections",
                "workspace-users-and-invites": "Workspace users and invites",
            },
            "rows": {
                unlimited: "Unlimited",
                na: "n/a",
            },
            "help": {
                title: "Learn more about workspace quotas",
                trial: "Quotas for trial workspaces",
                paid: "Quotas for paid workspaces",
            },
        },
    },
    "index": {
        hero: {
            header: "Manage projects the right way.",
            text: "Warp drive your way to success with software that helps you to collaborate on and manage projects efficiently, with speed.",
            button: "Start a free trial",
            alt: "An illustration showing the look and feel of tasks in Projectify's user interface",
        },
        trust: {
            header: 'Everything you need to <span class="text-primary">stay organized</span> and <span class="text-primary">deliver faster</span>',
            text: "The go-to project management tool for developers.",
        },
        features: {
            "feature-1": {
                header: "Task cards that are accessible and keyboard friendly",
                text: "No more drag and drop disasters! Create and move tasks around the board with ease and speed. Organize and prioritize your workload with peace of mind.",
                alt: "A screenshot from the Projectify dashboard showing how the interface can be used without drag and drop",
            },
            "feature-2": {
                header: "Transform mammoth tasks into smaller, feasible ones",
                text: "Sub tasks break up the workload to allow for large tasks and progress to become more realistic and achievable. Add, reorder, edit and delete limitless sub tasks.",
                alt: "A screenshot from a task in the Projectify UI showing how sub tasks can be assigned to tasks",
            },
            "feature-3": {
                header: "Full control of your workspaces",
                text: "List and column views allow you to organize workflows and see the bigger picture. Split your workspace into boards to enable multi-project management. Filter by labels, workspace users, or keywords to focus on specific tasks.",
                alt: "An illustration showing how tasks can be filtered by workspace users or labels",
            },
            "feature-4": {
                header: "Keep an eye on important updates",
                text: "Whether it's a question about a task, a change of assignee, or simply a task moving to the next stage of development, notifications immediately let you know when there's an update.",
                alt: "An illustration showing notifications in the Projectify UI informing the user of recent updates to their tasks",
            },
            "feature-5": {
                header: "Responsive for on-the-go",
                text: "Need to access your projects while away from the office? No app. No problem. A fully responsive experience to stay connected and keep projects on track.",
                alt: "An illustration of a smartphone showing the Projectify UI in a landscape orientation.",
            },
            "feature-6": {
                header: "We never sell your data. Ever.",
                text: "Our platform fully complies with GDPR regulations, amongst others, so you can be rest assured that your private information stays private.",
                alt: "An illustration showing our mascot Poly safekeeping your data",
            },
            "feature-7": {
                header: "Projectify is 100% Free Software",
                text: "We respect your freedom and privacy and provide you the source code under a Free Software license. The Projectify application is licensed under the GNU Affero General Public License (AGPL) version 3.0 or later.",
                link: "Learn more here",
                alt: "Birds freed from their gilded cage",
            },
        },
        solutions: {
            header: {
                title: "Meeting diverse needs with practical solutions.",
                text: "From companies big and small to individuals working alone, Projectify can be used to manage all kinds of tasks.",
            },
            list: {
                "development-teams": {
                    text: "Development teams",
                    alt: "An illustration showing our mascot Poly working at a computer",
                },
                "research": {
                    text: "Research",
                    alt: "An illustration showing our mascot researching in a laboratory",
                },
                "project-management": {
                    text: "Project management",
                    alt: "An illustration showing our mascot overseeing our factory",
                },
            },
            more: "See more use cases",
        },
    },
    "pricing": {
        "header": {
            title: "Pricing",
            subtitle: "One plan. One price. All features.",
        },
        "plan": {
            title: "Universal Plan",
            price: "{price, number, ::currency/USD} / seat per month",
            cta: "Start a free trial",
        },
        "features": {
            title: "What's included?",
            list: [
                "Unlimited tasks",
                "Unlimited workspace boards",
                "Collaborate with workspace users",
                "Add multiple labels",
                "Role permissions",
                // "Set due dates",
                "Customize your workspace",
                "Archive completed workspace boards",
                // "Real-time notifications",
                // "File storage of 3 GB",
                "Filter by label or assignee",
                "Accessible interface",
            ],
        },
        "trial-mode": {
            title: "Trial mode available",
            explanation:
                "You can use a Projectify workspace in trial mode free of charge. The trial allows you to evaluate whether the Projectify project management software suits your needs. While your workspace is in trial mode, the following limitations will apply.",
            limitations: {
                title: "Trial mode limitations",
                list: [
                    // TODO mention chat messages when available -
                    "A workspace can have up to <strong>2</strong> workspace users",
                    "A workspace can hold up to <strong>10</strong> workspace boards",
                    "You can create up to <strong>100</strong> workspace board sections",
                    "You can create up to <strong>1000</strong> tasks",
                    "You can create up to <strong>1000</strong> sub tasks",
                    "You can create up to <strong>10</strong> labels",
                ],
            },
        },
    },
    "solutions": {
        "index": {
            hero: {
                title: "Solutions for every type of user",
                text: "Explore the different ways users are using Projectify to meet due dates, reach targets and be productive.",
                illustration: {
                    alt: "An illustration showing users of different backgrounds",
                },
            },
            solutions: {
                "development": {
                    title: "Development teams",
                    description:
                        "Monitor team progress throughout the whole software lifecyle.",
                    illustration: {
                        alt: "Our mascot Poly sitting in front of a computer, developing software and looking content",
                    },
                },
                "research": {
                    title: "Research",
                    description:
                        "Keep track of testing processes and results with incredible detail.",
                    illustration: {
                        alt: "Two content looking Polys (our mascot) researching in a laboratory and taking down notes on a chalkboard",
                    },
                },
                "project-management": {
                    title: "Project management",
                    description:
                        "Faciliate rapid delivery across multiple projects for any industry.",
                    illustration: {
                        alt: "Two Polys in a factory pointing at machines symbolized by huge gears. The mascot on the left holds a wrench.",
                    },
                },
                "academic": {
                    title: "Academic endeavours",
                    description:
                        "Structure a thesis, organise a project or keep track of assignments.",
                    illustration: {
                        alt: "Our mascot Poly celebrating their graduation from an educiational institution, wearing an academic dress, throwing a square academic cap into the air",
                    },
                },
                "remote-work": {
                    title: "Remote work",
                    description:
                        "Asynchronous communication whether you're at home or away.",
                    illustration: {
                        alt: "Our mascot Poly working at the beach looking happy",
                    },
                },
                "personal-use": {
                    title: "Personal use",
                    description:
                        "Log an exercise routine, create a new diet or plan an adventure. The possibilities are endless.",
                    illustration: {
                        alt: "Our mascot Poly thinking about all the things they want to do, among them being running, taking pictures and eating something tasty, each thing symbolized by a thought bubble",
                    },
                },
            },
            more: "Learn more",
        },
        "development": {
            hero: {
                title: "Development solutions",
                text: "How development teams can use Projectify to create tasks, monitor pulls requests and deploy faster.",
            },
            features: {
                "feature-1": {
                    title: "Organise with labels and task numbers",
                    text: "Use labels with terms like bug, enhancement or backend to categorize tasks. Filter with labels or search by task number to quickly locate what you're looking for.",
                    illustration: {
                        alt: "A illustration showing the label context menu used in Projectify",
                    },
                },
                "feature-2": {
                    title: "Live notifications",
                    text: "Notifications provide you with all the information you need whilst also giving you conveniant 'reply' and 'go to task' actions. The notification center houses updates from all workspaces so you never miss a beat.",
                    illustration: {
                        alt: "An illustration showing the live notifications a user can receive in Projectify",
                    },
                },
                "feature-3": {
                    title: "Plan and execute",
                    text: "Set up and monitor pull requests, merges, bug fixes and more for multiple workspace users of your team.",
                    illustration: {
                        alt: "An illlustration showing tasks in a section called 'In Progress'",
                    },
                },
            },
        },
        "research": {
            hero: {
                title: "Research solutions",
                text: "How researchers teams can use Projectify to collaborate on data with colleagues and meticulously catalogue findings.",
            },
            features: {
                "feature-1": {
                    title: "Categorize data with labels and numbers",
                    text: "Labels simplify the process of categorizing tasks. Automatically assigned task numbers take organisation one step further",
                    illustration: {
                        alt: "An illustration showing tasks in a section called 'In Progress'",
                    },
                },
                "feature-2": {
                    title: "Provide and request updates on any task",
                    text: "The updates sections allows you and your colleagues to share new details about how a test, experiment or study has gone.",
                    illustration: {
                        alt: "An illustration showing updates posted in a task by various users discussing organizing a meeting",
                    },
                },
                "feature-3": {
                    title: "Create and monitor multiple projects",
                    text: "With unlimited project boards and tasks per workspace, you're free to perform as much research and testing as you require.",
                    illustration: {
                        alt: "An illustration suggesting the different ways labels can be assigned to different team members depending on their role, such as design or marketing",
                    },
                },
            },
        },
        "project-management": {
            hero: {
                title: "Project management solutions",
                text: "How project managers can use Projectify to efficiently manage tasks, projects and workspace users of their team.",
            },
            features: {
                "feature-1": {
                    title: "An ethical approach to management",
                    text: "View how many tasks a workspace user has assigned to them, so the workload can be divided equally. Filter by workspace user to see what individual colleagues are working on.",
                    illustration: {
                        alt: "An illustration showing how Projectify displays each workspace users assigned task count",
                    },
                },
                "feature-2": {
                    title: "Live notifications",
                    text: "Notifications provide you with all the information you need whilst also giving you convenient 'reply' and 'go to task' actions. The notification center houses updates from all workspaces so you never miss a beat.",
                    illustration: {
                        alt: "An illustration showing notifications arriving about tasks being updated",
                    },
                },
                "feature-3": {
                    title: "Full control of your workspaces",
                    text: "List and column views allow you to organise workflows and see the bigger picture. Split your workspace into boards to enable multi-project management. Filter by labels, users or keyboards to focus on specific tasks.",
                    illustration: {
                        alt: "An illustration showing a collapsed dashboard side bar and various workspace users and labels",
                    },
                },
                "feature-4": {
                    title: "Permissions to control access",
                    text: "Make sure nothing important gets deleted. With permission roles - Owner, Maintainer, Member and Observer, you can be safe in knowing there won't be any accidentally data loss.",
                    illustration: {
                        alt: "An illustration of a settings screen showing workspace users belonging to a workspace user and their role within the workspace. The illustration also shows a button allowing filtering by role and another button letting a user invite new workspace users",
                    },
                },
            },
        },
        "academic": {
            hero: {
                title: "Academic solutions",
                text: "How students can use Projectify to plan a thesis, collaborate, or keep track of assignments.",
            },
            features: {
                "feature-1": {
                    title: "Deadlines become a lifeline",
                    text: "Projectify notifies you of upcoming due dates for assignments, so you'll never miss a paper's due date.",
                    illustration: {
                        alt: "An illustration showing how Projectify will inform a user of different task due dates and other important updates",
                    },
                },
                "feature-2": {
                    title: "Checklists that aid your progress",
                    text: "We know that projects and dissertations can be daunting, but we're here to help. Breaking tasks into smaller sub tasks allow you to micro-achieve your way to completion.",
                    illustration: {
                        alt: "An illustration showing how users can track subtask progress for each task",
                    },
                },
                "feature-3": {
                    title: "Create notes on each task and coordinate with friends",
                    text: "Invite friends and classmates into your workspace to collaborate, share ideas and more.",
                    illustration: {
                        alt: "An illustration showing the various features the task view has to offer, such as description, sub tasks, tracking task updates, and more",
                    },
                },
            },
        },
        "remote-work": {
            hero: {
                title: "Remote solutions",
                text: "How remote workers can use Projectify to keep in tune with projects and stay connected.",
            },
            features: {
                "feature-1": {
                    title: "Work together across timezones",
                    text: "Asynchronous communication is vital for all teams be they remote or in the office. Assign tasks, create new projects and provide updates, anywhere, anytime.",
                    illustration: {
                        alt: "An illustration showing the updates screen of a task where two workspace users decide on when to organize a remote meeting",
                    },
                },
                "feature-2": {
                    title: "Notifications and updates on any task",
                    text: "Notifications allow for important information to be delivered, even if you're not around. When you're away from your computer, updates to task will stay unread in the notification center until you get back.",
                    illustration: {
                        alt: "An illustration showing a notification popup telling the user about recent updates to the tasks in their workspace",
                    },
                },
                "feature-3": {
                    title: "Assign tasks to users all over the world",
                    text: "Whether it's Leo in the Phillipines or Valerie in Brazil, once you assign a task to someone they will be notified immediately with a pop-up.",
                    illustration: {
                        alt: "An illustration showing the 'In Progress' section of a workspace board with tasks being assigned to different users",
                    },
                },
            },
        },
        "personal-use": {
            hero: {
                title: "Personal solutions",
                text: "How people can use Projectify for everyday life, whether it be keeping track fo your health or creating an itinerary for a trip.",
            },
            features: {
                "feature-1": {
                    title: "Create tasks with ease",
                    text: "Organise your tasks into individual projects with sections such as 'To do', 'In progress' and 'Done'. Provide descriptions for each task and set due dates. Labels simplify the process of catergorizing tasks.",
                    illustration: {
                        alt: "An illustration showing a 'To do' and 'Done' section, showing personal tasks that a user assigned to themselves, such as 'Book a ticket to Paris' or 'Learn French for beginners'",
                    },
                },
                "feature-2": {
                    title: "Check off sub tasks as you go",
                    text: "Need to plan an event? Want to create a list of achievements? Sub tasks help you to check off small tasks bit by bite.",
                    illustration: {
                        alt: "An illustration showing various sub tasks that a user has created within a task, such as 'Swim freestyle for 10 lengths'",
                    },
                },
                "feature-3": {
                    title: "Add friends and family to your space",
                    text: "Get everyone on the same page by assigning task to different workspace users.",
                    illustration: {
                        alt: "An illustration showing how different tasks in the 'In progress' section of a workspace board have been assigned to friends and family. The tasks are 'Trim back overgrown hedges', 'Polish wooden furnishings', and 'Replace extractor fan grating'",
                    },
                },
            },
        },
    },
    "terms-of-service": {
        nav: {
            "title": "Terms of service",
            "japanese": "Japanese (original)",
            "english": "English (translation)",
            "go-back": "Jump back to top",
        },
    },
    "privacy-policy": {
        nav: {
            "title": "Privacy Policy",
            "japanese": "Japanese Privacy Policy (original)",
            "english": "English Privacy Policy (translation)",
            "japanese-gdpr": "Japanese GDPR Privacy Policy (original)",
            "english-gdpr": "English GDPR Privacy Policy (translation)",
            "go-back": "Jump back to top",
        },
    },
    "free-software": {
        "hero": "Free Software and License Information",
        "header": "Projectify project management software is created by:",
        "license":
            "This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.",
        "warranty":
            "This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.",
        "find-copy":
            "You can retrieve a copy of the source code and the LICENSE here:",
        "source": {
            frontend: "Projectify Frontend",
            backend: "Projectify Backend",
        },
        "trademark": "<strong>Projectify</strong> is a registered trademark.",
    },
    "contact-us": {
        title: "Contact",
        body: {
            title: "Contact information",
            text: "Should you have any questions, suggestions, or other inquiries regarding Projectify, please contact us using the following email address written below. We try to answer all inquiries within two working days. Please be patient if it takes longer.",
        },
        email: {
            href: "mailto:hello@projectifyapp.com?subject=Projectify contact",
            label: "hello@projectifyapp.com",
        },
        illustration: {
            alt: "An illustration of a phone booth",
        },
    },
    "accessibility": {
        hero: {
            title: "Accessibility statement",
            illustration: {
                alt: "Accessibility logo",
            },
        },
        goals: {
            title: "Accessibility goals",
            text: "Projectify is committed to ensuring digital inclusivity and accessibility for people with diverse disabilities. We are continually improving the user experience for everyone, and applying the relevant accessibility standards. We are also aiming to improve the use of both our website and platform for users who employ assistive technologies.",
        },
        measures: {
            title: "Measures we take to support accessiblity",
            list: [
                "Include accessibility as part of our mission statement",
                "Ensure designs meet a minimum accessibilty level (WCAG 2.1 level AA)",
                "Compatibility with different web browsers and assistive technology",
                "Include people with disabilities in our user personas",
                "Conduct usability tests with people who have disabilities",
            ],
        },
        conformance: {
            title: "Conformance status",
            text: "The Web Content Accessibility Guidelines (WCAG) standard defines requirements to improve accessibility for people with disabilities. It defines three levels of conformance: Level A, Level AA, and Level AAA. 'Fully conforms' means that the content meets all of the WCAG requirements at the specified Level without exceptions. Although our goal is WCAG 2.1 Level AA conformance, we have also applied some Level AAA Success Criteria: Images of text are only used for decorative purposes. Content posted since May 2022 fully conforms to WCAG 2.1 Level AA. It partially conforms to Level AAA.Older content conforms to earlier versions of WCAG, for example, WCAG 2.0.",
        },
        compatibility: {
            title: "Compatibility with browsers and assistive technologies",
            text: "The Projectify website and platform is designed to be compatible with assistive technologies and the last two versions of major browsers. The website and platform are not designed for Internet Explorer 11 and earlier versions.",
        },
        platform: {
            title: "Platform",
            text: "We are currently in the process of making our platform conform to accessiblity standards. Our main focus is to improve color contrast in both the light and dark modes of our platform, increase discoverability of features for users with vision impairments and enhance the usability of our main components.",
        },
        website: {
            title: "Website",
            list: [
                "Keyboard navigation: All menus, buttons , inputs and actions are accessible from a keyboard",
                "Screen reader compatibility: Our code supports the use of screen readers for users who digest information through audio means",
                "Images: All images are supported with descriptive and accurate alternative text which can be read by screen readers",
                "Text: Our text size, weight and font style have been carefully chosen to be accessible to users with dyslexia and/or visual impairment. WCAG 2.0 level AA requires a contrast ratio of at least 4.5:1 for normal text and 3:1 for large text.",
                "Color: WCAG 2.1 requires a contrast ratio of at least 3:1 for graphics and user interface components, which we meet",
                "Magnification: For sight impaired users, all pages and content can be magnified using standard browser controls or magnification software",
            ],
        },
        limitations: {
            title: "Limitations",
            text: "We are aware that, despite our best efforts, there may be limitations to the accessibilty of both the platform and website. Below is a description of known limitations. Please contact us if you discover an issue not listed below. Known limitations of the platform:",
            list: [
                "Tab selection not working on the calendar menu",
                "Not all screen readers can read placeholder text",
            ],
        },
        evaluation: {
            title: "Evaluation report",
            text: "An evaluation report can be found here link. Assessment of both the platform and website was carried out by self-evaluation.",
        },
        contact: {
            title: "Contact us",
            text: "We welcome feedback on the accessibility of Projectify. If you encounter any acccessibility barriers whilst using the platform or website, please email hello@projectify.com. ",
        },
    },
    "help": {
        "hero": {
            image: {
                alt: "Our mascot poly flying into the air using a jetpack",
            },
            header: {
                text: "Help and tips",
                subtext:
                    "Learn to fly through projects with speed and agility",
            },
        },
        "overview": "Overview",
        "help-sections": "Help sections",
        "go-to-section": "View this section",
        "basics": {
            title: "Basics",
            description: "Your first steps towards productivity",
            content: BasicsHelpPage,
        },
        "workspaces": {
            title: "Workspaces",
            description: "Independent spaces at your fingertips",
            content: WorkspacesHelpPage,
        },
        "workspace-boards": {
            title: "Workspace boards",
            description: "Separate projects from each other",
            content: WorkspaceBoardsHelpPage,
        },
        "workspace-board-sections": {
            title: "Workspace board sections",
            description: "Maximize the efficiency of your tasks",
            content: WorkspaceBoardSectionsHelpPage,
        },
        "tasks": {
            title: "Tasks",
            description: "All the ins and outs of task creation",
            content: TasksHelpPage,
        },
        "labels": {
            title: "Labels",
            description: "Create categories for your tasks",
            // TODO "Ways to use labels"
            content: LabelsHelpPage,
        },
        "workspace-users": {
            title: "Workspace users",
            description: "Collaboration starts with an invite",
            content: WorkspaceUsersHelpPage,
        },
        // TODO Bulk select
        "filters": {
            title: "Filters",
            description: "Streamline your workflow with filters",
            content: FiltersHelpPage,
        },
        "billing": {
            title: "Billing and accounts",
            description: "Payment and account information",
            content: BillingHelpPage,
        },
        "trial": {
            title: "Trial workspace",
            description: "How to set up a trial workspace",
            content: TrialHelpPage,
        },
        "quota": {
            title: "Workspace quotas",
            description: "Understand workspace resource quotas",
            content: QuotaHelpPage,
        },
        "roles": {
            title: "Roles",
            description: "Divide up roles between workspace users",
            content: RolesHelpPage,
        },
        "skip": "Skip ahead to",
    },
    "navigation": {
        header: {
            "development-preview": "Development preview",
            "logo": {
                alt: "Projectify",
            },
            "solutions": "Solutions",
            "help": "Help",
            "pricing": "Pricing",
            "log-in": "Log in",
            "start-a-free-trial": "Start a free trial",
            "continue-to-dashboard": "Continue to dashboard",
        },
        footer: {
            logo: {
                alt: "Projectify",
                heading: "Project management at pace.",
            },
            cta: "Start a free trial",
            nav: {
                product: {
                    title: "Product",
                    pricing: "Pricing",
                },
                resources: {
                    "title": "Resources",
                    "help-and-tips": "Help and tips",
                },
                company: {
                    "title": "Company",
                    "accessibility-statement": "Accessibility statement",
                    "contact-us": "Contact us",
                    "corporate-info": "Corporate information",
                },
                legal: {
                    "title": "Legal",
                    "privacy": "Privacy Policy",
                    "tos": "Terms of Service",
                    "free-software": "Free Software",
                },
            },
            epilogue: {
                "copyright": "Copyright 2021-2024 JWP Consulting GK",
                "free-software":
                    "The Projectify application is free software, and you are welcome to redistribute it under certain conditions;",
                "details": "see here for details",
                "build":
                    "This version was built on {buildDate} from commit {commitHash} on branch {branchName} committed on {commitDate}.",
            },
        },
    },
    "roles": {
        observer: "Observer",
        member: "Member",
        maintainer: "Maintainer",
        owner: "Owner",
    },
    "typography": {
        anchor: {
            "new-tab": "(Opens in new tab)",
        },
    },
};
export default messages;
