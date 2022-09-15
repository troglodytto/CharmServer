from django.urls import path
from Auth.views import LoginAPI, ProfileAPI
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("auth/login", LoginAPI.as_view()),
    path("auth/refresh", TokenRefreshView.as_view()),
    path("auth/profile", ProfileAPI.as_view()),
]
