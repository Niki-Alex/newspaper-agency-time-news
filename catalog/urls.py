from django.urls import path

from .views import (
    home_page,
    TopicListView,
    RedactorListView,
    NewspaperListView,
)

urlpatterns = [
    path("", home_page, name="home-page"),
    path("topic/", TopicListView.as_view(), name="topic-list"),
    path("redactor/", RedactorListView.as_view(), name="redactors-list"),
    path("newspaper/", NewspaperListView.as_view(), name="newspapers-list"),
]

app_name = "catalog"
