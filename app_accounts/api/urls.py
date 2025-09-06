from django.urls import include, path
from .views import RegesistrationView

urlpatterns = [
   path("registration/", RegesistrationView.as_view(), name="registration-list"),
]