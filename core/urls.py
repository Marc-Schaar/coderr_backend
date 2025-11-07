from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("app_accounts.api.urls")),
    path("api/", include("app_offers.api.urls")),
    path("api/", include("app_orders.api.urls")),
    path("api/", include("app_reviews.api.urls")),
    path("api/", include("app_platform.api.urls")),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
