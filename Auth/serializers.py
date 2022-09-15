from rest_framework import serializers
from firebase_admin import auth
from Auth.models import User


class LoginSerializer(serializers.Serializer):
    id_token = serializers.CharField()

    def validate(self, data):
        try:
            user = auth.verify_id_token(data["id_token"])
            return user
        except auth.InvalidIdTokenError as error:
            raise serializers.ValidationError(
                {"message": "Invalid IdToken", "details": error}
            )

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["name"],
            email=validated_data["email"],
            profile_image=validated_data["picture"],
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
