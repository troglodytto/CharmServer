from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/v1/admin/", admin.site.urls),
    path("api/v1/", include("Auth.urls")),
    path("api/v1/", include("User.urls")),
]
