# Refactor

## Introduce full_clean to all BaseModels

Justus 2024-02-08

Since we don't rely on serializers for full_clean, we are not calling it
anymore (woops) and getting IntegrityErrors instead of ValidationErrors when
we violate constraints. This can happen for example when the label name vs
workspace pk constraint is violated.

At the time of writing, I have augmented workspaces.models.label.Label and
user.models.user.User with a full_clean() calling save() override. This shall
be added to other Model instances as well. Calling full_clean has an impact on
query count, so a lot of test case numbers will have to be adjusted.

# Done

## Use correct User type for typing

Maybe: Type AbstractBaseUser to be the django.contrib.auth.models User instead

How it was solved: we just couple the applications to user.models.User

## Remove factories

Remove all factories. They make tests slow, and we don't really need
so much extra things. Creating instances in conftests should be enough.
For more complicated things, we can write some `create_*` functions
in a /factory.py file for each app.

Factories were removed, there is no more factory dependency.

## Permissions (2023-10-20)

No permission checking is done beyond testing whether a user has access to a
resource based on whether they belong to a workspace or not. Especially roles
are not correctly considered at this point.

Some of the missing authorization (as of 2023-11-27)

- Task update
- Any read

This is all done now, we have a validate_perm function that we call from the
service layer. (Might have to do a double check on this one)
