"""Corporate models."""
import uuid

from django.db import (
    models,
    transaction,
)
from django.utils.translation import gettext_lazy as _


class CustomerQuerySet(models.QuerySet):
    """Customer QuerySet."""

    def get_by_uuid(self, uuid):
        """Get Customer by UUID."""
        return self.get(uuid=uuid)

    def get_by_workspace_uuid(self, workspace_uuid):
        """Get workpsace by UUID."""
        return self.get(workspace__uuid=workspace_uuid)

    def filter_by_user(self, user):
        """Filter by user."""
        return self.filter(workspace__users=user)

    def get_for_user_and_uuid(self, user, uuid):
        """Get customer by user and uuid."""
        return self.filter_by_user(user).get(uuid=uuid)

    def get_by_stripe_customer_id(self, stripe_customer_id):
        """Get customer by stripe customer id."""
        return self.get(stripe_customer_id=stripe_customer_id)


class Customer(models.Model):
    """Customer model. One to one linked to workspace."""

    class SubscriptionStatus(models.TextChoices):
        """Subscription Choices."""

        ACTIVE = "ACT", _("Active")
        UNPAID = "UNP", _("Unpaid")
        CANCELLED = "CAN", _("Cancelled")

    workspace = models.OneToOneField(
        "workspace.Workspace",
        on_delete=models.CASCADE,
    )
    seats = models.PositiveIntegerField(default=1)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    subscription_status = models.CharField(
        max_length=3,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.UNPAID,
    )
    stripe_customer_id = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        # XXX
        # unique=True,
        # db_index=True,
    )

    objects = CustomerQuerySet.as_manager()

    def activate_subscription(self):
        """
        Activate customer subscription.

        Saves model instance.
        """
        self.subscription_status = Customer.SubscriptionStatus.ACTIVE
        self.save()

    def cancel_subscription(self):
        """
        Cancel customer subscription.

        Saves model instance.
        """
        self.subscription_status = Customer.SubscriptionStatus.CANCELLED
        self.save()

    def assign_stripe_customer_id(self, stripe_customer_id):
        """
        Assign stripe customer id.

        Saves model instance.
        """
        self.stripe_customer_id = stripe_customer_id
        self.save()

    def set_number_of_seats(self, seats):
        """
        Set the number of seats.

        Saves model instance.
        """
        if self.seats == seats:
            return
        self.seats = seats
        self.save()

    @property
    def active(self):
        """Return if active customer."""
        return self.subscription_status == Customer.SubscriptionStatus.ACTIVE

    @property
    @transaction.atomic
    def seats_remaining(self):
        """Return the number of seats remaining."""
        num_users = len(self.workspace.users.all())
        invites_qs = self.workspace.workspaceuserinvite_set.all()
        num_invites = len(invites_qs)
        return self.seats - num_users - num_invites
