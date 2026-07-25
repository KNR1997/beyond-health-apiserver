from django.urls import path

from beyond_health.app.views.invoice.base import InvoiceViewSet

urlpatterns = [
    path(
        "invoices/",
        InvoiceViewSet.as_view({"get": "list"}),
        name="invoice",
    ),
    path(
        "invoices/<uuid:pk>/",
        InvoiceViewSet.as_view({
            "get": "retrieve",
            # "put": "update",
            "patch": "partial_update",
            # "delete": "destroy",
        }),
        name="invoice",
    ),

    # path(
    #     "invoices/<uuid:pk>/download/",
    #     InvoicePdfView.as_view(),
    #     name="invoice",
    # ),
]
