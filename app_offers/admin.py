from django.contrib import admin

from .models import Offer, OfferDetails


class OfferDetailsInline(admin.TabularInline):
    model = OfferDetails
    extra = 0


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    inlines = [OfferDetailsInline]
    list_display = (
        "title",
        "user",
        "min_price",
        "min_delivery_time",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    search_fields = ("title", "description", "user__username")
    autocomplete_fields = ("user",)


@admin.register(OfferDetails)
class OfferDetailsAdmin(admin.ModelAdmin):
    list_display = ("title", "offer", "offer_type", "price", "delivery_time_in_days", "revisions")
    list_filter = ("offer_type",)
    search_fields = ("title", "offer__title")
