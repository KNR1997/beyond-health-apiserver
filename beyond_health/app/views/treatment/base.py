# Third party imports
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiRequest

# Module imports
from beyond_health.app.base import BaseViewSet
from beyond_health.app.serializers.treatment import TreatmentListSerializer
from beyond_health.db.models import Treatment
from beyond_health.utils.openapi import (
    UNAUTHORIZED_RESPONSE,
    FORBIDDEN_RESPONSE,
    ID_PARAMETER,
    TREATMENT_NOT_FOUND_RESPONSE,
    create_paginated_response,
)


class TreatmentViewSet(BaseViewSet):
    model = Treatment
    serializer_class = TreatmentListSerializer

    search_fields = ["name"]
    filterset_fields = []
    ordering_fields = ['name', 'category', 'is_active', 'created_at']

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    @extend_schema(
        operation_id="create_treatment",
        summary="Create treatment",
        description="Create a treatment",
        tags=["Treatments"],
        responses={
            201: OpenApiResponse(
                description="Treatment created",
                response=TreatmentListSerializer
            )},
        request=OpenApiRequest(request=TreatmentListSerializer),
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        operation_id="list_treatments",
        summary="List or retrieve treatments",
        description="Retrieve all treatments.",
        tags=["Treatments"],
        parameters=[],
        responses={
            200: create_paginated_response(
                TreatmentListSerializer,
                "PaginatedTreatmentResponse",
                "Paginated list of treatments",
                "Paginated Treatments",
            ),
            401: UNAUTHORIZED_RESPONSE,
            403: FORBIDDEN_RESPONSE,
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        operation_id="get_treatment",
        summary="Get treatment",
        description="Get a treatment by slug.",
        tags=["Treatments"],
        parameters=[ID_PARAMETER],
        responses={
            201: OpenApiResponse(
                description="Treatment",
                response=TreatmentListSerializer
            ),
            401: UNAUTHORIZED_RESPONSE,
            403: FORBIDDEN_RESPONSE,
            404: TREATMENT_NOT_FOUND_RESPONSE,
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="update_treatment",
        summary="Update treatment",
        description="Update a treatment",
        tags=["Treatments"],
        parameters=[ID_PARAMETER],
        responses={
            204: OpenApiResponse(
                description="Treatment updated",
                response=TreatmentListSerializer
            )},
        request=OpenApiRequest(request=TreatmentListSerializer),
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        operation_id="delete_treatment",
        summary="Delete treatment",
        description="Delete a treatment by slug",
        tags=["Treatments"],
        parameters=[ID_PARAMETER],
        responses={204: OpenApiResponse(description="Treatment deleted")},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
