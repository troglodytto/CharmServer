from django.urls import path

from Auth.views import LoginAPI, LogoutAPI, RefreshAPI

urlpatterns = [
    path("auth/login", LoginAPI.as_view()),
    path("auth/refresh", RefreshAPI.as_view()),
    path("auth/logout", LogoutAPI.as_view()),
]
