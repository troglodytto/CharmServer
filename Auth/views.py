from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.tokens import RefreshToken

# from django.db import Do
from Auth.models import User
from Auth.serializers import LoginSerializer, UserSerializer


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = User.find_or_create(serializer=serializer)
        token = RefreshToken.for_user(user)

        return Response(
            {
                "is_active": user.is_active,
                "access_token": str(token.access_token),
                "refresh_token": str(token),
                "expires_in": 900,
                "profile_image": validated_data["picture"],
                "email": user.email,
                "user_name": validated_data["name"],
            },
            HTTP_200_OK,
        )


class ProfileAPI(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user
