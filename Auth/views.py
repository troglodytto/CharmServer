from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_205_RESET_CONTENT
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from User.models import User

from Auth.serializers import LoginSerializer


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = User.find_or_create(serializer=serializer)
        token = RefreshToken.for_user(user)

        response = Response(
            {
                "is_active": user.is_active,
                "profile_image": validated_data["picture"],
                "email": user.email,
                "username": validated_data["name"],
                "access_token": str(token.access_token),
                "refresh_token": str(token),
                "max_age": settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            },
            HTTP_200_OK,
        )

        return response


class LogoutAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = Response(
            {"message": "Logout successful"}, HTTP_205_RESET_CONTENT
        )

        return response


class RefreshAPI(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response(
            {
                **response.data,
                "max_age": settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            },
            response.status_code,
        )
