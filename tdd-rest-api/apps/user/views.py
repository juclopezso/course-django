from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.user.serializers import AuthTokenSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
  """Create new user"""
  serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
  """Create auth token for user"""
  serializer_class = AuthTokenSerializer
  renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
  """Manage authenticated user"""
  serializer_class = UserSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)

  def get_object(self):
    """Get and return auth user"""
    return self.request.user