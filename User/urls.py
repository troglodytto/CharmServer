from django.urls import path

from User.views import ProfileAPI

urlpatterns = [
    path("user/profile", ProfileAPI.as_view()),
]
