from django.urls import include, path
from .views import RegesistrationView, LoginView, ProfileDetailView

urlpatterns = [
   path("registration/", RegesistrationView.as_view(), name="registration-list"),
   path("login/",LoginView.as_view(), name="login-list"),
   path("profile/<int:pk>",ProfileDetailView.as_view(), name="profile-detail")
]