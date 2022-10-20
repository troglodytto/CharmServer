from rest_framework import generics, permissions

from User.serializers import UserSerializer


# Create your views here.
class ProfileAPI(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
