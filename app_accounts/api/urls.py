from django.urls import include, path
from .views import RegesistrationView, LoginView

urlpatterns = [
   path("registration/", RegesistrationView.as_view(), name="registration-list"),
   path("login/",LoginView.as_view(), name="login-list")
]