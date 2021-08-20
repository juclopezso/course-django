from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
  """Serializer for user model"""

  class Meta:
    model = get_user_model()
    fields = ('email', 'password', 'name')
    extra_kwargs = {
      'password': {
        'write_only': True,
        'min_length': 5
      }
    }

  def create(self, validated_data):
    """Create new user"""
    return get_user_model().objects.create_user(**validated_data)

  def update(self, instance, validated_data):
    """Update the auth user"""
    password = validated_data.pop('password', None) # password set to password or none
    user = super().update(instance, validated_data)

    if password:
      user.set_password(password)

    user.save()

    return user

  
class AuthTokenSerializer(serializers.Serializer):
  """Serializer for user authentication"""
  email = serializers.CharField()
  password = serializers.CharField(
    style={'input_type': 'password'},
    trim_whitespace=False
  )

  def validate(self, attrs):
    """Validate and authentica user"""
    email = attrs.get('email')
    password = attrs.get('password')

    user = authenticate(
      request=self.context.get('request'),
      username=email,
      password=password
    )

    if not user:
      msg = _('Unable to authenticate with the provided credentials')
      raise serializers.ValidationError(msg, code='authorization')

    attrs['user'] = user
    return attrs