# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022, 2023 JWP Consulting GK
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
"""Test stripe webhook."""
from unittest import (
    mock,
)

from django.urls import (
    reverse,
)

import pytest
from rest_framework.test import APIClient

from projectify.corporate.types import CustomerSubscriptionStatus

from ...models import Customer


@pytest.mark.django_db
class TestStripeWebhook:
    """Test incoming webhooks from Stripe."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to resource."""
        return reverse("corporate:stripe-webhook")

    def test_checkout_session_completed(
        self,
        unpaid_customer: Customer,
        client: APIClient,
        resource_url: str,
    ) -> None:
        """Test the handling of a checkout session."""
        header = {"HTTP_STRIPE_SIGNATURE": "dummy_sig"}

        event = mock.MagicMock()
        event.type = "checkout.session.completed"
        event["data"]["object"].customer = "unique_stripe_id"
        event["data"]["object"].metadata.customer_uuid = unpaid_customer.uuid

        with mock.patch("stripe.Webhook.construct_event") as construct_event:
            construct_event.return_value = event
            response = client.post(resource_url, **header)
        assert response.status_code == 200
        unpaid_customer.refresh_from_db()
        assert (
            unpaid_customer.subscription_status
            == CustomerSubscriptionStatus.ACTIVE
        )
        assert unpaid_customer.stripe_customer_id == "unique_stripe_id"

    def test_customer_subscription_updated(
        self, paid_customer: Customer, client: APIClient, resource_url: str
    ) -> None:
        """Test customer.subscription.updated."""
        header = {"HTTP_STRIPE_SIGNATURE": "dummy_sig"}
        new_seats = paid_customer.seats + 1

        event = mock.MagicMock()
        event.type = "customer.subscription.updated"
        event["data"]["object"].customer = paid_customer.stripe_customer_id
        event["data"]["object"].quantity = new_seats

        with mock.patch("stripe.Webhook.construct_event") as construct_event:
            construct_event.return_value = event
            response = client.post(resource_url, **header)
        assert response.status_code == 200
        paid_customer.refresh_from_db()
        assert paid_customer.seats == new_seats

    def test_customer_subscription_cancelled(
        self,
        paid_customer: Customer,
        client: APIClient,
        resource_url: str,
    ) -> None:
        """Test cancelling Subscription when payment fails."""
        header = {"HTTP_STRIPE_SIGNATURE": "dummy_sig"}
        event = mock.MagicMock()
        event.type = "invoice.payment_failed"
        event["data"]["object"].customer = paid_customer.stripe_customer_id
        event["data"]["object"].next_payment_attempt = None
        with mock.patch("stripe.Webhook.construct_event") as construct_event:
            construct_event.return_value = event
            response = client.post(resource_url, **header)
        assert response.status_code == 200
        paid_customer.refresh_from_db()
        assert (
            paid_customer.subscription_status
            == CustomerSubscriptionStatus.CANCELLED
        )