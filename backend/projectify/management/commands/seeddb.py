# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021-2024 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
Seeddb command.

The various --n-* arguments can be used to ensure that the database contains at
least N of each object.

For workspaces that already exist, we don't touch them.

For new workspaces, we add quantities of objects, as specified in the arguments

Assuming your development database is called projectify, you can do a full test
run by running
dropdb projectify && \
    createdb projectify && \
    poetry run ./manage.py migrate && \
    poetry run ./manage.py seeddb
"""
from argparse import (
    ArgumentParser,
)
from datetime import (
    timezone,
)
from itertools import (
    count,
    groupby,
)
from random import (
    choice,
    randint,
    sample,
)
from typing import (
    Any,
    TypedDict,
)

from django.core.management.base import (
    BaseCommand,
)
from django.db import (
    transaction,
)

from faker import (
    Faker,
)

from projectify.corporate.models import (
    Customer,
)
from projectify.corporate.types import CustomerSubscriptionStatus
from projectify.user.models import (
    User,
)
from projectify.user.services.internal import (
    user_create,
    user_create_superuser,
)
from projectify.workspace.models import (
    ChatMessage,
    Label,
    Section,
    Task,
    TaskLabel,
    Workspace,
    WorkspaceBoard,
)
from projectify.workspace.models.const import WorkspaceUserRoles
from projectify.workspace.models.sub_task import (
    SubTask,
)
from projectify.workspace.models.workspace_user import (
    WorkspaceUser,
)

Altogether = TypedDict(
    "Altogether",
    {
        "workspace": Workspace,
        "workspace_users": list[WorkspaceUser],
        "labels": list[Label],
        "projects": list[WorkspaceBoard],
        "sections": list[Section],
        "number": "count[int]",
    },
)

WORKSPACE_TITLE_MIN_LENGTH = 20
WORKSPACE_TITLE_MAX_LENGTH = 200

WORKSPACE_BOARD_MIN_SECTIONS = 2
WORKSPACE_BOARD_MAX_SECTIONS = 15
WORKSPACE_BOARD_TITLE_MIN_LENGTH = 20
WORKSPACE_BOARD_TITLE_MAX_LENGTH = 100

SECTION_TITLE_MIN_LENGTH = 20
SECTION_TITLE_MAX_LENGTH = 200

TASK_TITLE_MIN_LENGTH = 40
TASK_TITLE_MAX_LENGTH = 250
TASK_DESCRIPTION_SENTENCES = 10
TASK_MIN_LABEL_COUNT = 0
TASK_MAX_LABEL_COUNT = 10
TASK_MIN_CHAT_MESSAGE_COUNT = 0
TASK_MAX_CHAT_MESSAGE_COUNT = 10

SUB_TASKS_MIN_COUNT = 0
SUB_TASKS_MAX_COUNT = 10
SUB_TASK_TITLE_MIN_LENGTH = 40
SUB_TASK_TITLE_MAX_LENGTH = 250


class Command(BaseCommand):
    """Command."""

    fake: Faker
    n_users: int
    n_workspaces: int
    n_projects: int
    n_labels: int
    n_tasks: int
    n_add_users: int

    def create_users(self) -> list["User"]:
        """Create users."""
        existing_users = User.objects.count()
        if existing_users == 0:
            user_create_superuser(
                email="admin@localhost",
                password="password",
            )
            self.stdout.write("Created superuser")
            guest = user_create(
                email="guest@localhost",
                password="password",
            )
            guest.is_active = True
            guest.save()
            self.stdout.write("Created and manually activated normal user")
        remaining_users = self.n_users - User.objects.count()
        new_users = User.objects.bulk_create(
            [
                User(
                    email=self.fake.email(),
                    preferred_name=self.fake.name() if randint(0, 1) else None,
                    is_staff=False,
                    is_superuser=False,
                )
                for _ in range(remaining_users)
            ]
        )
        self.stdout.write(f"Created {len(new_users)} new users")
        return list(User.objects.all())

    def create_tasks(self, altogether: list[Altogether]) -> None:
        """
        Create tasks.

        Takes in a combination of workspaces, boards and sections and creates
        all tasks at once.
        """
        # We store all the combinations in a list here (using tee was
        # evaluated for a second)
        task_combos = list(
            (together, section, _order)
            for together in altogether
            for section in together["sections"]
            for _order in range(randint(self.n_tasks // 2, self.n_tasks))
        )
        tasks = Task.objects.bulk_create(
            [
                Task(
                    title=self.fake.text(
                        randint(TASK_TITLE_MIN_LENGTH, TASK_TITLE_MAX_LENGTH),
                    ),
                    description=self.fake.paragraph(
                        TASK_DESCRIPTION_SENTENCES
                    ),
                    workspace_board_section=section,
                    due_date=self.fake.date_time(tzinfo=timezone.utc),
                    workspace=together["workspace"],
                    _order=_order,
                    number=next(together["number"]),
                    assignee=choice(together["workspace_users"])
                    # 2 out of 3 tasks have an assignee
                    if randint(0, 2)
                    else None,
                )
                for (together, section, _order) in task_combos
            ]
        )
        self.stdout.write(f"Created {len(tasks)} tasks")

        # That way we can zip it back together and create the task labels
        # and still have a reference to the labels that were used for this
        # task
        something: list[tuple[Altogether, Task]] = list(
            zip([together for together, _, _ in task_combos], tasks)
        )
        task_labels = TaskLabel.objects.bulk_create(
            [
                TaskLabel(
                    task=task,
                    label=label,
                )
                for together, task in something
                for label in sample(
                    # Make sure we don't go over the amount of labels we have
                    # actually created for this workspace
                    together["labels"],
                    min(
                        len(together["labels"]),
                        randint(TASK_MIN_LABEL_COUNT, TASK_MAX_LABEL_COUNT),
                    ),
                )
            ]
        )
        self.stdout.write(f"Created {len(task_labels)} task labels")

        sub_tasks = SubTask.objects.bulk_create(
            [
                SubTask(
                    title=self.fake.text(
                        randint(
                            SUB_TASK_TITLE_MIN_LENGTH,
                            SUB_TASK_TITLE_MAX_LENGTH,
                        )
                    ),
                    description=self.fake.paragraph(),
                    task=task,
                    done=self.fake.pybool(),
                    _order=_order,
                )
                for task in tasks
                for _order in range(
                    randint(SUB_TASKS_MIN_COUNT, SUB_TASKS_MAX_COUNT)
                )
            ]
        )
        self.stdout.write(f"Created {len(sub_tasks)} sub tasks")

        chat_messages = ChatMessage.objects.bulk_create(
            [
                ChatMessage(
                    task=task,
                    text=self.fake.paragraph(),
                    author=choice(together["workspace_users"]),
                )
                for together, task in something
                for _ in range(
                    randint(
                        TASK_MIN_CHAT_MESSAGE_COUNT,
                        TASK_MAX_CHAT_MESSAGE_COUNT,
                    )
                )
            ]
        )
        self.stdout.write(f"Created {len(chat_messages)} chat messages")
        self.stdout.write(f"Populated {len(tasks)} tasks")

    def create_workspaces(
        self,
        users: list[User],
    ) -> list[Workspace]:
        """Create workspaces."""
        existing_workspaces = Workspace.objects.count()
        self.stdout.write(
            f"There are already {existing_workspaces} workspaces"
        )
        remaining_workspaces = max(0, self.n_workspaces - existing_workspaces)

        workspaces: list[Workspace] = Workspace.objects.bulk_create(
            [
                Workspace(
                    title=self.fake.text(
                        randint(
                            WORKSPACE_TITLE_MIN_LENGTH,
                            WORKSPACE_TITLE_MAX_LENGTH,
                        )
                    ),
                    description=self.fake.paragraph(),
                )
                for _ in range(remaining_workspaces)
            ]
        )
        self.stdout.write(f"Created {len(workspaces)} new workspaces")

        workspaces_workspace_users = WorkspaceUser.objects.bulk_create(
            [
                WorkspaceUser(
                    workspace=workspace,
                    user=user,
                    role=WorkspaceUserRoles.OWNER
                    if user.email == "admin@localhost"
                    else WorkspaceUserRoles.MEMBER,
                )
                for workspace in workspaces
                for user in sample(users, self.n_add_users)
            ]
        )
        self.stdout.write(
            f"Added {len(workspaces_workspace_users)} users to "
            f"{len(workspaces)} new workspaces"
        )
        workspaces_labels = Label.objects.bulk_create(
            [
                Label(
                    name=self.fake.catch_phrase(),
                    color=randint(0, 6),
                    workspace=workspace,
                )
                for workspace in workspaces
                for _ in range(self.n_labels)
            ]
        )
        self.stdout.write(f"Created {len(workspaces_labels)} labels")

        workspaces_projects = WorkspaceBoard.objects.bulk_create(
            [
                WorkspaceBoard(
                    title=self.fake.text(
                        randint(
                            WORKSPACE_BOARD_TITLE_MIN_LENGTH,
                            WORKSPACE_BOARD_TITLE_MAX_LENGTH,
                        )
                    ),
                    description=self.fake.paragraph(),
                    workspace=workspace,
                    due_date=self.fake.date_time(tzinfo=timezone.utc),
                )
                for workspace in workspaces
                for _ in range(self.n_projects)
            ]
        )
        self.stdout.write(
            f"Created {len(workspaces_projects)} projects"
        )

        workspaces_sections = Section.objects.bulk_create(
            [
                Section(
                    project=project,
                    title=title,
                    _order=_order,
                )
                for _, projects in groupby(
                    workspaces_projects, key=lambda b: b.workspace
                )
                for project in projects
                for _order, title in enumerate(
                    self.fake.text(
                        randint(
                            SECTION_TITLE_MIN_LENGTH,
                            SECTION_TITLE_MAX_LENGTH,
                        )
                    )
                    for _ in range(
                        randint(
                            WORKSPACE_BOARD_MIN_SECTIONS,
                            WORKSPACE_BOARD_MAX_SECTIONS,
                        )
                    )
                )
            ]
        )
        self.stdout.write(
            f"Created {len(workspaces_sections)} workspace " "board sections"
        )

        # The idea here is that instead of going into each nested object in
        # a for loop, we create them altogether at once.
        # So:
        # Create all workspaces
        # Assign all users to all new workspaces
        # Create all labels for all new workspaces
        # Create all projects for all new workspaces
        # etc.
        altogether: list[Altogether] = [
            {
                "workspace": workspace,
                "workspace_users": list(workspace_users),
                "labels": list(labels),
                "projects": list(projects),
                "sections": list(sections),
                "number": count(1),
            }
            for (
                (workspace, workspace_users),
                (_, labels),
                (_, projects),
                (_, sections),
            ) in zip(
                groupby(workspaces_workspace_users, key=lambda u: u.workspace),
                groupby(workspaces_labels, key=lambda label: label.workspace),
                groupby(
                    workspaces_projects, key=lambda b: b.workspace
                ),
                groupby(
                    workspaces_sections,
                    key=lambda b: b.project.workspace,
                ),
            )
        ]

        self.create_tasks(altogether)

        # Now we just have to adjust each workspace's highest task number
        for together in altogether:
            together["workspace"].highest_task_number = next(
                together["number"]
            )
            together["workspace"].save()
        return workspaces

    def create_corporate_accounts(
        self, seats: int, workspaces: list[Workspace]
    ) -> None:
        """Create corporate accounts."""
        customers = Customer.objects.bulk_create(
            [
                Customer(
                    workspace=workspace,
                    subscription_status=CustomerSubscriptionStatus.CUSTOM,
                    seats=seats,
                )
                for workspace in workspaces
            ]
        )
        self.stdout.write(f"Created customers for {len(customers)} workspaces")

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Add arguments."""
        parser.add_argument(
            "--n-users",
            type=int,
            default=40,
            help="Ensure N users are created",
        )
        parser.add_argument(
            "--n-workspaces",
            type=int,
            default=5,
            help="Ensure N workspaces are present",
        )
        parser.add_argument(
            "--n-projects",
            type=int,
            default=20,
            help="Ensure N projects are added to a new workspace",
        )
        parser.add_argument(
            "--n-add-users",
            type=int,
            default=15,
            help="Ensure N users are added to new workspaces",
        )
        parser.add_argument(
            "--n-labels",
            type=int,
            default=20,
            help="Ensure N labels are added to a new workspace",
        )
        parser.add_argument(
            "--n-tasks",
            type=int,
            default=40,
            help="Ensure up to N tasks are in new section",
        )

    @transaction.atomic
    def handle(self, *args: object, **options: Any) -> None:
        """Handle."""
        self.fake = Faker()
        self.n_users = options["n_users"]
        self.n_workspaces = options["n_workspaces"]
        self.n_projects = options["n_projects"]
        self.n_labels = options["n_labels"]
        self.n_tasks = options["n_tasks"]
        self.n_add_users = options["n_add_users"]
        if self.n_add_users > self.n_users:
            self.stdout.write(
                f"You are trying to add more users to each workspace "
                f"({self.n_add_users} users) than are "
                f"requested to be created in the first place. "
                f"({self.n_users} users) "
                f"The amount of users created will be increase to "
                f"{self.n_add_users}."
            )
            self.n_users = max(self.n_users, self.n_add_users)
        users = self.create_users()
        workspaces = self.create_workspaces(users)
        self.create_corporate_accounts(
            seats=self.n_users, workspaces=workspaces
        )
