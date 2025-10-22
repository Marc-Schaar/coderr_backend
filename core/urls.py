from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app_accounts.api.urls')),
    path('api/', include('app_offers.api.urls')),
    path('api/', include('app_orders.api.urls')),
    path("api/", include("app_reviews.api.urls")),
    path('api/', include('app_platform.api.urls')),
]
