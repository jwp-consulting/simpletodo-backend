"""Corporate views."""
import logging

from django.conf import (
    settings,
)
from django.http import (
    HttpResponse,
)
from django.views.decorators.csrf import (
    csrf_exempt,
)

from rest_framework import (
    generics,
)

import stripe

from . import (
    models,
    serializers,
)


endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

logger = logging.getLogger(__name__)


class WorkspaceCustomerRetrieve(generics.RetrieveAPIView):
    """Retrieve customer for a workspace."""

    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer

    def get_queryset(self):
        """Filter by request user."""
        return self.queryset.filter_by_user(self.request.user)

    def get_object(self):
        """Get customer."""
        return self.get_queryset().get_by_workspace_uuid(
            self.kwargs["workspace_uuid"]
        )


def update_subscription(customer, subscription):
    """Update a stripe subscription."""
    logger.info("Customer %s updated subscription: %s", customer, subscription)
    customer.set_number_of_seats(subscription.quantity)


@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe Webhooks."""
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        logger.exception("Invalid payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        logger.exception("Invalid signature")
        return HttpResponse(status=400)

    # Handle events
    if event.type == "checkout.session.completed":
        session = event["data"]["object"]
        customer_uuid = session.metadata.customer_uuid
        customer = models.Customer.objects.get_by_uuid(customer_uuid)
        customer.assign_stripe_customer_id(session.customer)
        customer.activate_subscription()
    elif event.type == "customer.subscription.updated":
        subscription = event["data"]["object"]
        customer_id = subscription.customer
        customer = models.Customer.objects.get_by_stripe_customer_id(
            customer_id
        )
        update_subscription(customer, subscription)
    else:
        logger.warning("Unhandled event type %s", event.type)

    return HttpResponse(status=200)
