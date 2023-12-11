"""Corporate factories."""
import factory
from factory import (
    django,
)

from . import (
    models,
)


class CustomerFactory(django.DjangoModelFactory):
    """Customer factory."""

    workspace = factory.SubFactory("workspace.factory.WorkspaceFactory")
    seats = factory.Faker("pyint", min_value=1, max_value=98)
    subscription_status = models.CustomerSubscriptionStatus.ACTIVE
    stripe_customer_id = "stripe_customer_id"

    class Meta:
        """Meta."""

        model = models.Customer
