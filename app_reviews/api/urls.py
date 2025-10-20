from django.urls import include, path
from .views import ReviewListView

urlpatterns = [
    path("reviews/", ReviewListView.as_view(), name="reviews-list")
]
