from products.models import Variant, VariantOption


def get_variant_options(variant_id):
    try:
        # Retrieve the Variant instance
        variant = Variant.objects.get(pk=variant_id)

        # Get all VariantOption objects associated with this Variant
        variant_options = VariantOption.objects.filter(variant=variant)

        # Return the queryset of VariantOption objects
        return variant_options

    except Variant.DoesNotExist:
        # Handle case where Variant with the provided ID does not exist
        return None
    except Exception as e:
        # Handle other exceptions
        return None
