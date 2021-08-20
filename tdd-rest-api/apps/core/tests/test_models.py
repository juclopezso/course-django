from django.db.models.fields import SmallIntegerField
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.core import models

# run the test on the commando line using: python manage.py test


def sample_user(email='test@test.com', password='test1234'):
  """Create sample user"""
  return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):

  def test_user_create_with_email(self):
    """Test creation of user with email and email has to be normalized"""
    email = 'juAn@GmaiL.com'
    password = 'Test123'
    user = get_user_model().objects.create_user(
      email=email,
      password=password
    )

    # email has to be normalized
    self.assertEqual(user.email, email.lower())
    self.assertTrue(user.check_password(password))
  
  def test_new_user_invalid_email(self):
    """Test invalid email on new users"""
    with self.assertRaises(ValueError):
      get_user_model().objects.create_user(None, 'Pass123')
  
  def test_create_super_user(self):
    """Test creation of super user"""
    email = 'juan@test.com'
    password = 'Test123'
    user = get_user_model().objects.create_superuser(
      email=email,
      password=password
    )

    # email has to be normalized
    self.assertTrue(user.is_superuser)
    self.assertTrue(user.is_staff)
  
  def test_create_tag_str(self):
    """Test creation of a Tag"""
    tag = models.Tag.objects.create(
      user=sample_user(),
      name='Tag test'
    )

    self.assertEqual(str(tag), tag.name)