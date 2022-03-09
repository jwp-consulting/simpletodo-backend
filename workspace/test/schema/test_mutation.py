"""Test workspace mutations."""
from datetime import (
    datetime,
)

from django.utils import (
    timezone,
)

import pytest

from ... import (
    factory,
    models,
)


@pytest.mark.django_db
class TestChangeSubTaskDoneMutation:
    """Test ChangeSubTaskDoneMutation."""

    query = """
mutation ChangeSubTaskDone($uuid: ID!) {
  changeSubTaskDone(input: {subTaskUuid: $uuid, done: true}) {
    subTask {
      done
    }
  }
}
"""

    def test_query(
        self,
        graphql_query_user,
        workspace_user,
        sub_task,
    ):
        """Test query."""
        assert sub_task.done is False
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(sub_task.uuid),
            },
        )
        assert result == {
            "data": {
                "changeSubTaskDone": {
                    "subTask": {
                        "done": True,
                    },
                },
            },
        }


@pytest.mark.django_db
class TestMoveWorkspaceBoardSectionMutation:
    """Test MoveWorkspaceBoardSectionMutation."""

    query = """
mutation MoveWorkspaceBoardSection($uuid: ID!) {
  moveWorkspaceBoardSection(
    input:{workspaceBoardSectionUuid: $uuid, order: 1 }
  ) {
    workspaceBoardSection {
      uuid
      order
    }
  }
}
"""

    def test_query(
        self,
        workspace_board_section,
        graphql_query_user,
        workspace_user,
    ):
        """Test the query."""
        factory.WorkspaceBoardSectionFactory(
            workspace_board=workspace_board_section.workspace_board,
        )
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board_section.uuid),
            },
        )
        assert result == {
            "data": {
                "moveWorkspaceBoardSection": {
                    "workspaceBoardSection": {
                        "uuid": str(workspace_board_section.uuid),
                        "order": 1,
                    },
                },
            },
        }


@pytest.mark.django_db
class TestMoveTaskMutation:
    """Test MoveTaskMutation."""

    query = """
mutation MoveTask($taskUuid: ID!, $sectionUuid: ID!) {
  moveTask(input: {taskUuid: $taskUuid,
      workspaceBoardSectionUuid: $sectionUuid, order: 2}) {
    task {
      title
    }
  }
}

"""

    def test_move(
        self,
        task,
        other_task,
        workspace_board_section,
        graphql_query_user,
        workspace_user,
    ):
        """Test moving."""
        result = graphql_query_user(
            self.query,
            variables={
                "taskUuid": str(task.uuid),
                "sectionUuid": str(workspace_board_section.uuid),
            },
        )
        assert result == {
            "data": {
                "moveTask": {
                    "task": {
                        "title": task.title,
                    }
                }
            }
        }


@pytest.mark.django_db
class TestAddUserToWorkspaceMutation:
    """Test AddUserToWorkspaceMutation."""

    query = """
mutation AddUserToWorkspace($uuid: ID!, $email: String!) {
  addUserToWorkspace(input: {uuid: $uuid, email: $email}) {
    workspace {
      uuid
    }
  }
}
"""

    def test_query(
        self,
        task,
        other_user,
        graphql_query_user,
        workspace,
        workspace_user,
    ):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace.uuid),
                "email": other_user.email,
            },
        )
        assert result == {
            "data": {
                "addUserToWorkspace": {
                    "workspace": {
                        "uuid": str(workspace.uuid),
                    },
                },
            },
        }

    def test_query_unauthorized(
        self,
        task,
        other_user,
        graphql_query_user,
        workspace,
    ):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace.uuid),
                "email": other_user.email,
            },
        )
        assert "errors" in result

    def test_no_user(
        self,
        task,
        graphql_query_user,
        workspace,
        workspace_user,
    ):
        """Test query."""
        assert workspace.users.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace.uuid),
                "email": "hello@example.com",
            },
        )
        assert result == {
            "data": {
                "addUserToWorkspace": {
                    "workspace": {
                        "uuid": str(workspace.uuid),
                    },
                },
            },
        }
        assert workspace.users.count() == 1
        assert workspace.workspaceuserinvite_set.count() == 1


@pytest.mark.django_db
class TestRemoveUserFromWorkspaceMutation:
    """Test RemoveUserFromWorkspaceMutation."""

    query = """
mutation RemoveUserFromWorkspace($uuid: ID!, $email: String!) {
  removeUserFromWorkspace(input: {uuid: $uuid, email: $email}) {
    workspace {
      uuid
    }
  }
}
"""

    def test_query(
        self,
        task,
        other_user,
        graphql_query_user,
        workspace,
        workspace_user,
    ):
        """Test query."""
        workspace.add_user(other_user)
        assert workspace.users.count() == 2
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace.uuid),
                "email": other_user.email,
            },
        )
        assert result == {
            "data": {
                "removeUserFromWorkspace": {
                    "workspace": {
                        "uuid": str(workspace.uuid),
                    },
                },
            },
        }
        assert workspace.users.count() == 1

    def test_query_unauthorized(
        self,
        task,
        other_user,
        graphql_query_user,
        workspace,
    ):
        """Test query."""
        workspace.add_user(other_user)
        assert workspace.users.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace.uuid),
                "email": other_user.email,
            },
        )
        assert "errors" in result
        assert workspace.users.count() == 1


@pytest.mark.django_db
class TestAssignTaskMutation:
    """Test AssignTaskMutation."""

    query = """
mutation AssignTask($uuid: ID!, $email: String) {
  assignTask(input: {uuid: $uuid, email: $email}) {
    task {
      assignee {
        email
      }
    }
  }
}
"""

    def test_query(
        self,
        task,
        other_user,
        other_workspace_user,
        graphql_query_user,
        workspace_user,
    ):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
                "email": other_user.email,
            },
        )
        assert result == {
            "data": {
                "assignTask": {
                    "task": {
                        "assignee": {
                            "email": other_user.email,
                        },
                    },
                },
            },
        }

    def test_unassign(
        self,
        task,
        other_user,
        other_workspace_user,
        graphql_query_user,
        workspace_user,
    ):
        """Test query."""
        task.assign_to(other_user)
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
                "email": None,
            },
        )
        assert result == {
            "data": {
                "assignTask": {
                    "task": {
                        "assignee": None,
                    },
                },
            },
        }


# Add Mutations
@pytest.mark.django_db
class TestAddLabelMutation:
    """Test AddLabelMutation."""

    query = """
mutation AddLabel($workspaceUuid: ID!) {
    addLabel(input: {
        workspaceUuid: $workspaceUuid,
        color: 1, name: "important"
    }) {
        label {
            name
            color
            workspace {
                uuid
            }
        }
    }
}
"""

    def test_query(self, workspace, workspace_user, graphql_query_user):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "workspaceUuid": str(workspace.uuid),
            },
        )
        assert result == {
            "data": {
                "addLabel": {
                    "label": {
                        "name": "important",
                        "color": 1,
                        "workspace": {
                            "uuid": str(workspace.uuid),
                        },
                    },
                },
            }
        }


@pytest.mark.django_db
class TestAddSubTaskMutation:
    """Test AddSubTaskMutation."""

    query = """
mutation AddSubTask($uuid: ID!) {
  addSubTask(
    input:{taskUuid: $uuid, title:"Hello world", description: "Foo bar"}) {
    subTask {
      title
    }
  }
}
"""

    def test_query(self, graphql_query_user, task, workspace_user):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
            },
        )
        assert result == {
            "data": {
                "addSubTask": {
                    "subTask": {
                        "title": "Hello world",
                    },
                },
            },
        }

    def test_query_unauthorized(self, graphql_query_user, task):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
            },
        )
        assert "errors" in result


@pytest.mark.django_db
class TestAddChatMessageMutation:
    """Test AddChatMessageMutation."""

    query = """
mutation AddChatMessage($uuid: ID!) {
  addChatMessage(input:{taskUuid: $uuid, text:"Hello world"}) {
    chatMessage {
      text
    }
  }
}
"""

    def test_query(self, graphql_query_user, task, workspace_user):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
            },
        )
        assert result == {
            "data": {
                "addChatMessage": {
                    "chatMessage": {
                        "text": "Hello world",
                    },
                },
            },
        }

    def test_query_unauthorized(self, graphql_query_user, task):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
            },
        )
        assert "errors" in result


@pytest.mark.django_db
class TestDuplicateTaskMutation:
    """Test DuplicateTaskMutation."""

    query = """
mutation DuplicateTask($uuid: ID!) {
    duplicateTask(input: {uuid: $uuid}) {
        task {
            uuid
        }
    }
}
"""

    def test_query(self, graphql_query_user, workspace_user, task):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
            },
        )
        new_task = models.Task.objects.last()
        assert result == {
            "data": {
                "duplicateTask": {
                    "task": {
                        "uuid": str(new_task.uuid),
                    }
                },
            },
        }


@pytest.mark.django_db
class TestAssignLabelMutation:
    """Test AssignLabelMutation."""

    query = """
mutation AssignLabel($taskUuid: ID!, $labelUuid: ID!, $assigned: Boolean!) {
    assignLabel(input: {
        taskUuid: $taskUuid, labelUuid: $labelUuid, assigned: $assigned
    }) {
        task {
            uuid
            labels {
                uuid
            }
        }
    }
}
"""

    def test_query_assign(
        self,
        graphql_query_user,
        task,
        label,
        workspace_user,
    ):
        """Test assigning."""
        result = graphql_query_user(
            self.query,
            variables={
                "taskUuid": str(task.uuid),
                "labelUuid": str(label.uuid),
                "assigned": True,
            },
        )
        assert result == {
            "data": {
                "assignLabel": {
                    "task": {
                        "uuid": str(task.uuid),
                        "labels": [
                            {
                                "uuid": str(label.uuid),
                            },
                        ],
                    }
                }
            }
        }

    def test_query_unassign(
        self,
        graphql_query_user,
        task,
        label,
        workspace_user,
    ):
        """Test unassigning."""
        task.add_label(label)
        result = graphql_query_user(
            self.query,
            variables={
                "taskUuid": str(task.uuid),
                "labelUuid": str(label.uuid),
                "assigned": False,
            },
        )
        assert result == {
            "data": {
                "assignLabel": {
                    "task": {
                        "uuid": str(task.uuid),
                        "labels": [],
                    }
                }
            }
        }


# Update Mutations
@pytest.mark.django_db
class TestUpdateWorkspaceMutation:
    """Test UpdateWorkspaceMutation."""

    query = """
mutation UpdateWorkspace($uuid: ID!) {
  updateWorkspace(input: {uuid: $uuid, title: "foo", description: "bar"}) {
    workspace {
      uuid
      title
      description
    }
  }
}

"""

    def test_query(
        self,
        graphql_query_user,
        workspace,
        workspace_user,
    ):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace.uuid),
            },
        )
        assert result == {
            "data": {
                "updateWorkspace": {
                    "workspace": {
                        "uuid": str(workspace.uuid),
                        "title": "foo",
                        "description": "bar",
                    },
                },
            },
        }

    def test_query_unauthorized(
        self,
        graphql_query_user,
        workspace,
    ):
        """Test with unauthorized user."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace.uuid),
            },
        )
        assert result == {
            "data": {
                "updateWorkspace": None,
            },
            "errors": [
                {
                    "locations": [{"column": 3, "line": 3}],
                    "message": "Workspace matching query does not exist.",
                    "path": ["updateWorkspace"],
                },
            ],
        }


@pytest.mark.django_db
class TestArchiveWorkspaceBoardMutation:
    """Test ArchiveWorkspaceBoardMutation."""

    query = """
mutation ArchiveWorkspaceBoard($uuid: ID!, $archived: Boolean!) {
    archiveWorkspaceBoard(input: {uuid: $uuid, archived: $archived}) {
        workspaceBoard {
            uuid
            archived
        }
    }
}
"""

    def test_archive(
        self,
        graphql_query_user,
        workspace_board,
        workspace_user,
    ):
        """Test archiving."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board.uuid),
                "archived": True,
            },
        )
        workspace_board.refresh_from_db()
        assert result == {
            "data": {
                "archiveWorkspaceBoard": {
                    "workspaceBoard": {
                        "uuid": str(workspace_board.uuid),
                        "archived": workspace_board.archived.isoformat(),
                    },
                },
            },
        }

    def test_unarchive(
        self,
        graphql_query_user,
        workspace_board,
        workspace_user,
    ):
        """Test unarchiving."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board.uuid),
                "archived": False,
            },
        )
        assert result == {
            "data": {
                "archiveWorkspaceBoard": {
                    "workspaceBoard": {
                        "uuid": str(workspace_board.uuid),
                        "archived": None,
                    },
                },
            },
        }


@pytest.mark.django_db
class TestUpdateWorkspaceBoardMutation:
    """Test UpdateWorkspaceBoardMutation."""

    query = """
mutation UpdateWorkspaceBoard($uuid: ID!, $deadline: DateTime) {
  updateWorkspaceBoard(input: {
    uuid: $uuid, title: "Foo", description: "Bar"
    deadline: $deadline})
  {
    workspaceBoard {
      title
      description
      deadline
    }
  }
}
"""

    def test_query(self, graphql_query_user, workspace_board, workspace_user):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board.uuid),
            },
        )
        assert result == {
            "data": {
                "updateWorkspaceBoard": {
                    "workspaceBoard": {
                        "title": "Foo",
                        "description": "Bar",
                        "deadline": None,
                    },
                },
            },
        }

    def test_set_deadline(
        self,
        graphql_query_user,
        workspace_board,
        workspace_user,
    ):
        """Test query."""
        now = timezone.now().isoformat()
        result = graphql_query_user(
            self.query,
            variables={
                "deadline": now,
                "uuid": str(workspace_board.uuid),
            },
        )
        assert result == {
            "data": {
                "updateWorkspaceBoard": {
                    "workspaceBoard": {
                        "title": "Foo",
                        "description": "Bar",
                        "deadline": now,
                    },
                },
            },
        }

    def test_query_unauthorized(self, graphql_query_user, workspace_board):
        """Test query when user not authorized."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board.uuid),
            },
        )
        assert "errors" in result


@pytest.mark.django_db
class TestUpdateWorkspaceBoardSectionMutation:
    """Test UpdateWorkspaceBoardSectionMutation."""

    query = """
mutation UpdateWorkspaceBoardSection($uuid: ID!) {
  updateWorkspaceBoardSection(input: {uuid: $uuid,\
       title: "Foo", description: "Bar"})
  {
    workspaceBoardSection {
      title
      description
    }
  }
}
"""

    def test_query(
        self,
        graphql_query_user,
        workspace_board_section,
        workspace_user,
    ):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board_section.uuid),
            },
        )
        assert result == {
            "data": {
                "updateWorkspaceBoardSection": {
                    "workspaceBoardSection": {
                        "title": "Foo",
                        "description": "Bar",
                    },
                },
            },
        }

    def test_query_unauthorized(
        self,
        graphql_query_user,
        workspace_board_section,
    ):
        """Test query when user not authorized."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board_section.uuid),
            },
        )
        assert "errors" in result


@pytest.mark.django_db
class TestUpdateTaskMutation:
    """Test TestUpdateTaskMutation."""

    query = """
mutation UpdateTaskMutation($uuid: ID!, $deadline: DateTime) {
  updateTask(
      input: {
        uuid: $uuid, title: "Foo", description: "Bar", deadline: $deadline
      }
  )
  {
    task {
      title
      description
    }
  }
}
"""

    def test_query(self, graphql_query_user, task, workspace_user):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
            },
        )
        assert result == {
            "data": {
                "updateTask": {
                    "task": {
                        "title": "Foo",
                        "description": "Bar",
                    },
                },
            },
        }

    def test_query_unauthorized(self, graphql_query_user, task):
        """Test query when user not authorized."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
            },
        )
        assert "errors" in result

    def test_assigning_deadline(
        self,
        graphql_query_user,
        task,
        workspace_user,
    ):
        """Test assigning a deadline."""
        deadline = timezone.now()
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
                "deadline": deadline.isoformat(),
            },
        )
        assert "errors" not in result, result
        task.refresh_from_db()
        assert task.deadline == deadline

    def test_assigning_deadline_missing_tz(
        self,
        graphql_query_user,
        task,
        workspace_user,
    ):
        """Test assigning a deadline."""
        deadline = datetime.now()
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
                "deadline": deadline.isoformat(),
            },
        )
        assert "errors" in result, result


@pytest.mark.django_db
class TestUpdateLabelMutation:
    """Test UpdateLabelMutation."""

    query = """
mutation UpdateLabel($uuid: ID!) {
    updateLabel(input: {uuid: $uuid, name: "Friendship", color: 199}) {
        label {
            name
            color
        }
    }
}
"""

    def test_query(self, graphql_query_user, label, workspace_user):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(label.uuid),
            },
        )
        assert result == {
            "data": {
                "updateLabel": {
                    "label": {
                        "name": "Friendship",
                        "color": 199,
                    },
                },
            },
        }


@pytest.mark.django_db
class TestUpdateSubTaskMutation:
    """Test TestUpdateSubTaskMutation."""

    query = """
mutation UpdateSubTaskMutation($uuid: ID!) {
  updateSubTask(input: {uuid: $uuid, title: "Foo", description: "Bar"})
  {
    subTask {
      title
      description
    }
  }
}
"""

    def test_query(self, graphql_query_user, sub_task, workspace_user):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(sub_task.uuid),
            },
        )
        assert result == {
            "data": {
                "updateSubTask": {
                    "subTask": {
                        "title": "Foo",
                        "description": "Bar",
                    },
                },
            },
        }

    def test_query_unauthorized(self, graphql_query_user, sub_task):
        """Test query when user not authorized."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(sub_task.uuid),
            },
        )
        assert "errors" in result


# Delete Mutations
@pytest.mark.django_db
class TestDeleteWorkspaceBoardMutation:
    """Test DeleteWorkspaceBoardMutation."""

    query = """
mutation DeleteWorkspaceBoard($uuid: ID!) {
  deleteWorkspaceBoard(input: {uuid: $uuid}) {
    workspaceBoard {
      uuid
    }
  }
}
"""

    def test_query(
        self,
        graphql_query_user,
        workspace_board,
        workspace_user,
    ):
        """Test query."""
        assert models.WorkspaceBoard.objects.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board.uuid),
            },
        )
        assert result == {
            "data": {
                "deleteWorkspaceBoard": {
                    "workspaceBoard": {
                        "uuid": str(workspace_board.uuid),
                    }
                }
            }
        }
        assert models.WorkspaceBoard.objects.count() == 0

    def test_query_unauthorized(self, graphql_query_user, workspace_board):
        """Test query."""
        assert models.WorkspaceBoard.objects.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board.uuid),
            },
        )
        assert result == {
            "data": {
                "deleteWorkspaceBoard": None,
            },
            "errors": [
                {
                    "locations": [{"column": 3, "line": 3}],
                    "message": "WorkspaceBoard matching query does not exist.",
                    "path": ["deleteWorkspaceBoard"],
                },
            ],
        }
        assert models.WorkspaceBoard.objects.count() == 1


@pytest.mark.django_db
class TestDeleteWorkspaceBoardSectionMutation:
    """Test DeleteWorkspaceBoardMutation."""

    query = """
mutation DeleteWorkspaceBoardSection($uuid: ID!) {
  deleteWorkspaceBoardSection(input: {uuid: $uuid}) {
    workspaceBoardSection {
      uuid
    }
  }
}
"""

    def test_query(
        self,
        graphql_query_user,
        workspace_board_section,
        workspace_user,
    ):
        """Test query."""
        assert models.WorkspaceBoardSection.objects.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board_section.uuid),
            },
        )
        assert result == {
            "data": {
                "deleteWorkspaceBoardSection": {
                    "workspaceBoardSection": {
                        "uuid": str(workspace_board_section.uuid),
                    }
                }
            }
        }
        assert models.WorkspaceBoardSection.objects.count() == 0

    def test_query_unauthorized(
        self,
        graphql_query_user,
        workspace_board_section,
    ):
        """Test query."""
        assert models.WorkspaceBoardSection.objects.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board_section.uuid),
            },
        )
        assert "errors" in result

    def test_still_has_tasks(
        self,
        graphql_query_user,
        workspace_board_section,
        workspace_user,
        task,
    ):
        """Assert section is not deleted if tasks still exist."""
        assert models.WorkspaceBoardSection.objects.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board_section.uuid),
            },
        )
        assert "still has tasks" in str(result)
        assert models.WorkspaceBoardSection.objects.count() == 1


@pytest.mark.django_db
class TestDeleteTask:
    """Test DeleteTask."""

    query = """
mutation DeleteTask($uuid: ID!) {
  deleteTask(input: {uuid: $uuid}) {
    task {
      uuid
    }
  }
}
"""

    def test_query(
        self,
        graphql_query_user,
        task,
        workspace_user,
        chat_message,
        sub_task,
    ):
        """Test query."""
        assert models.Task.objects.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
            },
        )
        assert result == {
            "data": {
                "deleteTask": {
                    "task": {
                        "uuid": str(task.uuid),
                    }
                }
            }
        }
        assert models.Task.objects.count() == 0

    def test_query_unauthorized(self, graphql_query_user, task):
        """Test query."""
        assert models.Task.objects.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
            },
        )
        assert "errors" in result


@pytest.mark.django_db
class TestDeleteLabel:
    """Test DeleteLabelMutation."""

    query = """
mutation DeleteLabel($uuid: ID!) {
    deleteLabel(input: {uuid: $uuid}) {
        label {
            uuid
        }
    }
}
"""

    def test_query(self, graphql_query_user, label, workspace_user):
        """Test query."""
        assert models.Label.objects.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(label.uuid),
            },
        )
        assert result == {
            "data": {
                "deleteLabel": {
                    "label": {
                        "uuid": str(label.uuid),
                    },
                },
            },
        }
        assert models.Label.objects.count() == 0


@pytest.mark.django_db
class TestDeleteSubTask:
    """Test DeleteSubTask."""

    query = """
mutation DeleteSubTask($uuid: ID!) {
  deleteSubTask(input: {uuid: $uuid}) {
    subTask {
      uuid
    }
  }
}
"""

    def test_query(self, graphql_query_user, sub_task, workspace_user):
        """Test query."""
        assert models.SubTask.objects.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(sub_task.uuid),
            },
        )

        assert result == {
            "data": {
                "deleteSubTask": {
                    "subTask": {
                        "uuid": str(sub_task.uuid),
                    }
                }
            }
        }
        assert models.SubTask.objects.count() == 0

    def test_query_unauthorized(self, graphql_query_user, task, sub_task):
        """Test query."""
        assert models.SubTask.objects.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(sub_task.uuid),
            },
        )
        assert "errors" in result
