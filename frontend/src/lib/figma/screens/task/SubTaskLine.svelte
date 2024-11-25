<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    // TODO missing:
    // proper input field
    // Wire into rest of application
    // Sub tasks need assignees
    import { _ } from "svelte-i18n";

    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Checkbox from "$lib/funabashi/select-controls/Checkbox.svelte";
    import type { SubTaskAssignment } from "$lib/types/stores";
    import type { CreateUpdateSubTask } from "$lib/types/workspace";

    // TODO we might want to create a separate sub task line for readonly.
    export let subTaskAssignment: SubTaskAssignment | undefined = undefined;
    export let subTask: Partial<CreateUpdateSubTask>;
    export let index: number | undefined = undefined;
    export let readonly = true;
    export let onInteract: (() => void) | undefined = undefined;
    export let onEnter: (() => void) | undefined = undefined;

    const id = crypto.randomUUID();
</script>

<div class="flex w-full flex-row items-center justify-between gap-2 px-2 py-1">
    <div class="flex grow flex-row items-center gap-2">
        <label for="checkbox-{id}" class="sr-only">
            {$_("task-screen.sub-tasks.done")}
        </label>
        <Checkbox
            bind:checked={subTask.done}
            disabled={readonly}
            contained={false}
            onClick={onInteract}
            id="checkbox-{id}"
        />
        <div class="grow">
            <label for={id} class="sr-only">
                {$_("task-screen.sub-tasks.enter-a-subtask")}
            </label>
            <InputField
                label={undefined}
                style={{ inputType: "text" }}
                placeholder={$_("task-screen.sub-tasks.enter-a-subtask")}
                name="sub-task-{id}"
                {id}
                bind:value={subTask.title}
                {readonly}
                onClick={onInteract}
                {onEnter}
            />
        </div>
    </div>
    {#if index !== undefined && subTaskAssignment && $subTaskAssignment}
        <div class="flex flex-row gap-2">
            <CircleIcon
                size="medium"
                icon="up"
                action={{
                    kind: "button",
                    action: subTaskAssignment.moveSubTaskUp.bind(null, index),
                    disabled: index < 1,
                }}
                ariaLabel={$_("task-screen.sub-tasks.move-up")}
            />
            <CircleIcon
                size="medium"
                icon="down"
                action={{
                    kind: "button",
                    action: subTaskAssignment.moveSubTaskDown.bind(
                        null,
                        index,
                    ),
                    disabled: index >= $subTaskAssignment.length - 1,
                }}
                ariaLabel={$_("task-screen.sub-tasks.move-down")}
            />
            <CircleIcon
                size="medium"
                icon="delete"
                action={{
                    kind: "button",
                    action: subTaskAssignment.removeSubTask.bind(null, index),
                }}
                ariaLabel={$_("task-screen.sub-tasks.remove")}
            />
        </div>
    {/if}
</div>
