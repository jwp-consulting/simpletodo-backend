# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test TaskLabel model."""

import pytest

from ... import models


# TODO rename TestTaskLabelQuerySet
@pytest.mark.django_db
class TestLabelQuerySet:
    """Test LabelQuerySet."""

    def test_filter_by_task_pks(
        self, label: models.Label, task: models.Task
    ) -> None:
        """Test filter_by_task_pks."""
        task.labels.add(label)
        task_label = models.TaskLabel.objects.get(task=task)
        qs = models.TaskLabel.objects.filter_by_task_pks([task.pk])
        task_labels = [task_label]
        assert list(qs) == task_labels


@pytest.mark.django_db
class TestTaskLabel:
    """Test TaskLabel model."""

    def test_factory(
        self,
        task_label: models.TaskLabel,
        task: models.Task,
        label: models.Label,
    ) -> None:
        """Test factory."""
        assert task_label.task == task
        assert task_label.label == label
