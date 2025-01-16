# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Task CRUD views."""

import logging
from typing import Any, Literal, Optional, Union
from uuid import UUID

from django import forms
from django.forms.formsets import TOTAL_FORM_COUNT
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods, require_POST

from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from projectify.lib.error_schema import DeriveSchema
from projectify.lib.schema import extend_schema
from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.views import platform_view
from projectify.workspace.models.label import Label
from projectify.workspace.models.section import Section
from projectify.workspace.models.task import Task
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.selectors.section import (
    SectionDetailQuerySet,
    section_find_for_user_and_uuid,
)
from projectify.workspace.selectors.task import (
    TaskDetailQuerySet,
    task_find_by_task_uuid,
)
from projectify.workspace.serializers.task_detail import (
    TaskCreateSerializer,
    TaskDetailSerializer,
    TaskUpdateSerializer,
)
from projectify.workspace.services.sub_task import (
    ValidatedData,
    ValidatedDatum,
    ValidatedDatumWithUuid,
)
from projectify.workspace.services.task import (
    task_create_nested,
    task_delete,
    task_move_after,
    task_move_in_direction,
    task_update_nested,
)

logger = logging.getLogger(__name__)


def get_object(
    request: Union[Request, AuthenticatedHttpRequest], task_uuid: UUID
) -> Task:
    """Get object for user and uuid."""
    user = request.user
    obj = task_find_by_task_uuid(
        who=user, task_uuid=task_uuid, qs=TaskDetailQuerySet
    )
    if obj is None:
        raise NotFound(
            _("Task with uuid {task_uuid} not found").format(
                task_uuid=task_uuid
            )
        )
    return obj


class TaskCreateForm(forms.Form):
    """Form for task creation."""

    title = forms.CharField(
        label=_("Task title"),
        widget=forms.TextInput(attrs={"placeholder": _("Task title")}),
    )
    assignee = forms.ModelChoiceField(required=False, queryset=None)
    # Django stub for ModelMultipleChoiceField does not accept None
    labels = forms.ModelMultipleChoiceField(required=False, queryset=None)  # type: ignore[arg-type]
    due_date = forms.DateTimeField(required=False)
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": _("Enter a description for your task")}
        ),
    )

    def __init__(self, workspace: Workspace, *args: Any, **kwargs: Any):
        """Populate available assignees."""
        super().__init__(*args, **kwargs)
        self.fields[
            "assignee"
        ].queryset = workspace.teammember_set.select_related("user")
        self.fields["labels"].queryset = workspace.label_set.all()


class TaskCreateSubTaskForm(forms.Form):
    """Form for creating sub tasks as part of task creation."""

    title = forms.CharField()
    done = forms.BooleanField(required=False)


TaskCreateSubTaskForms = forms.formset_factory(TaskCreateSubTaskForm, extra=0)


class TaskUpdateSubTaskForm(forms.Form):
    """Form for creating sub tasks as part of task creation."""

    title = forms.CharField()
    done = forms.BooleanField(required=False)
    uuid = forms.UUIDField(required=False, widget=forms.HiddenInput)
    delete = forms.BooleanField(
        required=False,
        label=_("Delete task"),
        initial=False,
    )


TaskUpdateSubTaskForms = forms.formset_factory(TaskUpdateSubTaskForm, extra=0)


@platform_view
def task_create_sub_task_form(
    request: AuthenticatedHttpRequest,
    sub_tasks: int,
) -> HttpResponse:
    """Return a single form for a sub task."""
    formset = TaskCreateSubTaskForms().empty_form
    formset.prefix = f"form-{sub_tasks}"
    new_sub_tasks = sub_tasks + 1
    return render(
        request,
        "workspace/task_create/sub_task.html",
        {"empty_formset": formset, "formset_total": new_sub_tasks},
    )


@platform_view
@require_http_methods(["GET", "POST"])
def task_create(
    request: AuthenticatedHttpRequest, section_uuid: UUID
) -> HttpResponse:
    """Create a task. Render form error if unsuccessful."""
    section = section_find_for_user_and_uuid(
        user=request.user, section_uuid=section_uuid, qs=SectionDetailQuerySet
    )
    if section is None:
        raise Http404(_("Section not found"))
    if request.method == "GET":
        return render(
            request,
            "workspace/task_create.html",
            {
                "form": TaskCreateForm(workspace=section.project.workspace),
                "formset": TaskCreateSubTaskForms(),
                "section": section,
            },
        )
    form = TaskCreateForm(section.project.workspace, request.POST)
    formset = TaskCreateSubTaskForms(request.POST)
    all_valid = form.is_valid() and formset.is_valid()
    if not all_valid:
        return render(
            request,
            "workspace/task_create.html",
            {"form": form, "formset": formset, "section": section},
            status=400,
        )

    sub_tasks: list[ValidatedDatum] = [
        {"title": d["title"], "done": d["done"], "_order": i}
        for i, d in enumerate(formset.cleaned_data)
        if d.get("title")
    ]

    task_create_nested(
        who=request.user,
        section=section,
        title=form.cleaned_data["title"],
        description=form.cleaned_data.get("description"),
        assignee=form.cleaned_data.get("assignee"),
        due_date=form.cleaned_data.get("due_date"),
        labels=form.cleaned_data["labels"],
        sub_tasks={"create_sub_tasks": sub_tasks, "update_sub_tasks": []},
    )
    return redirect(
        reverse("dashboard:projects:detail", args=(section.project.uuid,))
    )


@platform_view
def task_detail(
    request: AuthenticatedHttpRequest, task_uuid: UUID
) -> HttpResponse:
    """View a task. Accept POST for task updates."""
    task = task_find_by_task_uuid(
        who=request.user, task_uuid=task_uuid, qs=TaskDetailQuerySet
    )
    if task is None:
        raise Http404(_(f"Could not find task with uuid {task_uuid}"))
    context = {"task": task}
    return render(request, "workspace/task_detail.html", context)


class TaskUpdateForm(forms.Form):
    """Form for task creation."""

    title = forms.CharField(
        label=_("Task title"),
        widget=forms.TextInput(attrs={"placeholder": _("Task title")}),
    )
    assignee = forms.ModelChoiceField(required=False, queryset=None)
    # Django stub for ModelMultipleChoiceField does not accept None
    labels = forms.ModelMultipleChoiceField(required=False, queryset=None)  # type: ignore[arg-type]
    due_date = forms.DateTimeField(required=False)
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": _("Enter a description for your task")}
        ),
    )
    submit = forms.CharField(required=False)
    submit_stay = forms.CharField(required=False)
    add_sub_task = forms.CharField(required=False)

    def __init__(self, *args: Any, workspace: Workspace, **kwargs: Any):
        """Populate available assignees."""
        super().__init__(*args, **kwargs)
        self.fields[
            "assignee"
        ].queryset = workspace.teammember_set.select_related("user")
        self.fields["labels"].queryset = workspace.label_set.all()


def determine_action(
    request: AuthenticatedHttpRequest,
) -> Optional[Literal["get", "submit", "submit_stay", "add_sub_task"]]:
    """Determine what update view action should be taken."""
    if request.method == "GET":
        return "get"
    if "submit" in request.POST:
        return "submit"
    elif "submit_stay" in request.POST:
        return "submit_stay"
    elif "add_sub_task" in request.POST:
        return "add_sub_task"
    return None


@platform_view
@require_http_methods(["GET", "POST"])
def task_update_view(
    request: AuthenticatedHttpRequest, task_uuid: UUID
) -> HttpResponse:
    """Update task. Render errors."""
    task = task_find_by_task_uuid(
        who=request.user, task_uuid=task_uuid, qs=TaskDetailQuerySet
    )
    if task is None:
        raise Http404(_(f"Could not find task with uuid {task_uuid}"))
    project = task.section.project
    workspace = project.workspace

    action = determine_action(request)

    if action == "add_sub_task":
        post = request.POST.copy()
        sub_task_count_raw: str = post.get("form-" + TOTAL_FORM_COUNT, "0")
        try:
            sub_task_count = int(sub_task_count_raw)
        except ValueError as e:
            logger.error(
                "Unexpected error when getting total form count", exc_info=e
            )
            sub_task_count = 0
        post["form-TOTAL_FORMS"] = str(sub_task_count + 1)
        logger.info("Adding sub task")
        form = TaskUpdateForm(data=post, workspace=workspace)
        formset = TaskUpdateSubTaskForms(data=post)
        context = {"form": form, "task": task, "formset": formset}
        return render(request, "workspace/task_update.html", context)

    task_initial = {
        "title": task.title,
        "assignee": task.assignee,
        "labels": task.labels.all(),
        "due_date": task.due_date,
        "description": task.description,
    }
    sub_tasks = task.subtask_set.all()
    sub_tasks_initial = [
        {"title": sub_task.title, "done": sub_task.done, "uuid": sub_task.uuid}
        for sub_task in sub_tasks
    ]
    if action == "get":
        form = TaskUpdateForm(initial=task_initial, workspace=workspace)
        formset = TaskUpdateSubTaskForms(initial=sub_tasks_initial)
        context = {"form": form, "task": task, "formset": formset}
        return render(request, "workspace/task_update.html", context)

    form = TaskUpdateForm(
        data=request.POST, initial=task_initial, workspace=workspace
    )
    form.full_clean()
    formset = TaskUpdateSubTaskForms(
        data=request.POST,
        initial=sub_tasks_initial,
    )
    formset.full_clean()
    if not form.is_valid() or not formset.is_valid():
        context = {"form": form, "task": task, "formset": formset}
        return render(request, "workspace/task_update.html", context)

    cleaned_data = form.cleaned_data
    formset_cleaned_data = formset.cleaned_data
    update_sub_tasks: list[ValidatedDatumWithUuid] = [
        {
            "title": f["title"],
            "done": f["done"],
            "_order": i,
            "uuid": f["uuid"],
        }
        for i, f in enumerate(formset_cleaned_data)
        if f and f["uuid"] and not f["delete"]
    ]
    create_sub_tasks: list[ValidatedDatum] = [
        {
            "title": f["title"],
            "done": f["done"],
            "_order": i,
        }
        for i, f in enumerate(formset_cleaned_data)
        if f and not f["uuid"] and not f["delete"]
    ]
    task_update_nested(
        who=request.user,
        task=task,
        title=cleaned_data["title"],
        description=cleaned_data["description"],
        due_date=cleaned_data["due_date"],
        assignee=cleaned_data["assignee"],
        labels=[],
        sub_tasks={
            "update_sub_tasks": update_sub_tasks,
            "create_sub_tasks": create_sub_tasks,
        },
    )
    if action == "submit_stay":
        n = reverse("dashboard:tasks:detail", args=(task.uuid,))
    elif action == "submit":
        n = reverse("dashboard:projects:detail", args=(project.uuid,))
    else:
        n = reverse("dashboard:projects:detail", args=(project.uuid,))
    return redirect(n)


# Form
class TaskMoveForm(forms.Form):
    """Form that captures whether task shall be moved up or down."""

    up = forms.CharField(required=False)
    down = forms.CharField(required=False)


@require_POST
def task_move(
    request: AuthenticatedHttpRequest, task_uuid: UUID
) -> HttpResponse:
    """Move a task depending on form input."""
    task = get_object(request, task_uuid)
    form = TaskMoveForm(request.POST)
    if not form.is_valid():
        # TODO
        raise Exception()
    direction: Literal["up", "down"]
    if form.cleaned_data["up"]:
        direction = "up"
    elif form.cleaned_data["down"]:
        direction = "down"
    else:
        # TODO
        raise Exception()

    task = task_move_in_direction(
        who=request.user, task=task, direction=direction
    )

    if request.htmx:
        return render(
            request,
            "workspace/project_detail/section.html",
            {"section": task.section},
        )

    return redirect("workspace:projects:view", task.section.project.uuid)


# Create
class TaskCreate(APIView):
    """Create a task."""

    @extend_schema(
        request=TaskCreateSerializer,
        responses={201: TaskDetailSerializer, 400: DeriveSchema},
    )
    def post(self, request: Request) -> Response:
        """Handle POST."""
        serializer = TaskCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        section: Section = validated_data["section"]

        sub_tasks: ValidatedData
        if "sub_tasks" in validated_data:
            sub_tasks = validated_data.pop("sub_tasks")
        else:
            sub_tasks = {"create_sub_tasks": [], "update_sub_tasks": []}

        labels: list[Label] = validated_data.pop("labels")
        task = task_create_nested(
            who=request.user,
            section=section,
            title=validated_data["title"],
            description=validated_data.get("description"),
            assignee=validated_data.get("assignee"),
            due_date=validated_data.get("due_date"),
            labels=labels,
            sub_tasks=sub_tasks,
        )
        output_serializer = TaskDetailSerializer(instance=task)
        return Response(
            data=output_serializer.data, status=status.HTTP_201_CREATED
        )


# Read + Update + Delete
class TaskRetrieveUpdateDelete(APIView):
    """Retrieve a task."""

    @extend_schema(
        responses={200: TaskDetailSerializer},
    )
    def get(self, request: Request, task_uuid: UUID) -> Response:
        """Handle GET."""
        instance = get_object(request, task_uuid)
        serializer = TaskDetailSerializer(instance=instance)
        return Response(data=serializer.data)

    @extend_schema(
        request=TaskUpdateSerializer,
        responses={200: TaskDetailSerializer, 400: DeriveSchema},
    )
    def put(self, request: Request, task_uuid: UUID) -> Response:
        """
        Override update behavior. Return using different serializer.

        The idea is that we accept abbreviated nested fields, but return
        the data whole. (ws board section, sub tasks, labels, etc.)
        """
        # Copied from
        # https://github.com/encode/django-rest-framework/blob/d32346bae55f3e4718a185fb60e9f7a28e389c85/rest_framework/mixins.py#L65
        # We probably don't have to get the full object here!
        instance = get_object(request, task_uuid)
        serializer = TaskUpdateSerializer(
            instance,
            data=request.data,
            # Mild code duplication from
            # https://github.com/encode/django-rest-framework/blob/d32346bae55f3e4718a185fb60e9f7a28e389c85/rest_framework/generics.py#L113
            # :)
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        labels: list[Label] = validated_data.pop("labels")

        sub_tasks: ValidatedData
        if "sub_tasks" in validated_data:
            sub_tasks = validated_data.pop("sub_tasks")
        else:
            sub_tasks = {"create_sub_tasks": [], "update_sub_tasks": []}

        task_update_nested(
            who=request.user,
            task=instance,
            title=validated_data["title"],
            description=validated_data.get("description"),
            assignee=validated_data.get("assignee"),
            due_date=validated_data.get("due_date"),
            labels=labels,
            sub_tasks=sub_tasks,
        )

        instance = get_object(request, task_uuid)
        response_serializer = TaskDetailSerializer(instance=instance)
        return Response(
            status=status.HTTP_200_OK, data=response_serializer.data
        )

    @extend_schema(
        responses={204: None},
    )
    def delete(self, request: Request, task_uuid: UUID) -> Response:
        """Delete task."""
        instance = get_object(request, task_uuid)
        task_delete(task=instance, who=self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


# RPC
class TaskMoveToSection(APIView):
    """Move a task to the beginning of a section."""

    class TaskMoveToSectionSerializer(serializers.Serializer):
        """Accept the target section uuid."""

        section_uuid = serializers.UUIDField()

    @extend_schema(
        request=TaskMoveToSectionSerializer,
        responses={200: TaskDetailSerializer, 400: DeriveSchema},
    )
    def post(self, request: Request, task_uuid: UUID) -> Response:
        """Process the request."""
        user = request.user
        serializer = self.TaskMoveToSectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        task = task_find_by_task_uuid(who=user, task_uuid=task_uuid)
        if task is None:
            raise NotFound(_("Task for this UUID not found"))
        section = section_find_for_user_and_uuid(
            section_uuid=data["section_uuid"],
            user=user,
        )
        if section is None:
            raise serializers.ValidationError(
                {"section_uuid": _("No section was found for the given uuid")}
            )
        task_move_after(task=task, who=user, after=section)
        task = task_find_by_task_uuid(
            who=user, task_uuid=task_uuid, qs=TaskDetailQuerySet
        )
        output_serializer = TaskDetailSerializer(instance=task)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


# TODO inaccuracy: Might want to be able to move in front of a given task as
# well
class TaskMoveAfterTask(APIView):
    """Move a task right behind another task."""

    class TaskMoveAfterTaskSerializer(serializers.Serializer):
        """Accept a task uuid after which this task should be moved."""

        task_uuid = serializers.UUIDField()

    @extend_schema(
        request=TaskMoveAfterTaskSerializer,
        responses={200: TaskDetailSerializer, 400: DeriveSchema},
    )
    def post(self, request: Request, task_uuid: UUID) -> Response:
        """Process the request."""
        user = request.user
        serializer = self.TaskMoveAfterTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        task = task_find_by_task_uuid(who=user, task_uuid=task_uuid)
        if task is None:
            raise NotFound(_("Task for this UUID not found"))
        after = task_find_by_task_uuid(task_uuid=data["task_uuid"], who=user)
        if after is None:
            raise serializers.ValidationError(
                {"after_task_uuid": _("No task was found for the given uuid")}
            )
        task_move_after(task=task, who=user, after=after)
        task = task_find_by_task_uuid(
            who=user, task_uuid=task_uuid, qs=TaskDetailQuerySet
        )
        output_serializer = TaskDetailSerializer(instance=task)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
