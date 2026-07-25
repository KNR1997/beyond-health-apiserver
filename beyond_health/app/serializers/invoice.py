from rest_framework import serializers

from beyond_health.db.models import Invoice, InvoiceLineItem
from beyond_health.app.serializers.payment import PaymentListSerializer


class InvoiceListSerializer(serializers.ModelSerializer):
    # enrollment = InvoiceEnrollmentDetailsSerializer()

    class Meta:
        model = Invoice
        fields = [
            "id",
            "invoice_number",
            "issue_date",
            "subtotal",
            "status",
            "created_at",
            # "enrollment",
        ]


class InvoiceLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLineItem
        fields = [
            "id",
            "charge",
            "description",
            "quantity",
            "unit_price",
            "line_total",
        ]


class InvoiceDetailsSerializer(serializers.ModelSerializer):
    payment = PaymentListSerializer()
    line_items = InvoiceLineItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            "id",
            "invoice_number",
            "issue_date",
            "due_date",
            "subtotal",
            "discount_amount",
            "tax_amount",
            "total_amount",
            "notes",
            "status",

            "payment",
            "line_items"
        ]
