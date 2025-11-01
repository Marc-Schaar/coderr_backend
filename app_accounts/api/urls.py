from django.urls import include, path
from .views import (
    RegesistrationView,
    LoginView,
    ProfileDetailView,
    ProfileBusinessListView,
    ProfileCustomerListView,
)

urlpatterns = [
    path("registration/", RegesistrationView.as_view(), name="registration-list"),
    path("login/", LoginView.as_view(), name="login-list"),
    path("profile/<int:pk>", ProfileDetailView.as_view(), name="profile-detail"),
    path(
        "profile/business/",
        ProfileBusinessListView.as_view(),
        name="profile-business-list",
    ),
    path(
        "profile/customer/",
        ProfileCustomerListView.as_view(),
        name="profile-customer-list",
    ),
]
