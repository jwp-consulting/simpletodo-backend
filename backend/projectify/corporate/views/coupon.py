# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Coupon views."""

from uuid import UUID

from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions, serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from projectify.corporate.services.coupon import coupon_redeem
from projectify.lib.error_schema import DeriveSchema
from projectify.lib.schema import extend_schema
from projectify.workspace.selectors.workspace import (
    workspace_find_by_workspace_uuid,
)


class CouponRedeem(APIView):
    """Redeem a coupon for a workspace customer."""

    class CouponRedeemSerializer(serializers.Serializer):
        """Serializer that takes in a Coupon's code."""

        code = serializers.CharField()

    @extend_schema(
        request=CouponRedeemSerializer,
        responses={
            204: None,
            400: DeriveSchema,
        },
    )
    def post(self, request: Request, workspace_uuid: UUID) -> Response:
        """Handle POST."""
        workspace = workspace_find_by_workspace_uuid(
            workspace_uuid=workspace_uuid,
            who=request.user,
        )
        if workspace is None:
            raise exceptions.NotFound(
                _("No workspace was found for this workspace uuid")
            )

        serializer = self.CouponRedeemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Redeem coupon here
        coupon_redeem(who=request.user, code=data["code"], workspace=workspace)
        return Response(status=status.HTTP_204_NO_CONTENT)
