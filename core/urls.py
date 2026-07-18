from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("app_accounts.api.urls")),
    path("api/", include("app_offers.api.urls")),
    path("api/", include("app_orders.api.urls")),
    path("api/", include("app_reviews.api.urls")),
    path("api/", include("app_platform.api.urls")),
]

# Static files are served by WhiteNoise (see MIDDLEWARE) in both dev and
# production. Media (user uploads) has no equivalent, so it's served
# explicitly here regardless of DEBUG - there's no separate media host.
urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
