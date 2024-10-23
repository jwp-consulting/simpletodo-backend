# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022-2024 JWP Consulting GK
"""
Corporate app rules.

The order of rules follows the ordering of models.
"""

import rules

from projectify.workspace.rules import (
    is_at_least_owner,
)

# Customer
rules.add_perm("corporate.can_create_customer", is_at_least_owner)
rules.add_perm("corporate.can_read_customer", is_at_least_owner)
rules.add_perm("corporate.can_update_customer", is_at_least_owner)
rules.add_perm("corporate.can_delete_customer", is_at_least_owner)
