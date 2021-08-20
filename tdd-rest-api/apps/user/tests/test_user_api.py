
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
  return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
  """Test for non auth users"""
  def setUp(self):
    self.client = APIClient()

  def test_create_valid_user(self):
    """Test create a valid user success"""
    payload = {
      'email': 'test@test.com',
      'name': 'Test name',
      'password': 'pass123'
    }

    res = self.client.post(CREATE_USER_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    user = get_user_model().objects.get(**res.data)
    self.assertTrue(user.check_password(payload['password']))
    # check password is not responded after saved
    self.assertNotIn('password', res.data)

  def test_user_exists(self):
    """Test create an existing user fail"""
    payload = {
      'email': 'test@test.com',
      'name': 'Test name',
      'password': 'pass123'
    }
    # create a user with test email
    get_user_model().objects.create_user(**payload)
    # create_user(**payload) using the endpoint
    res = self.client.post(CREATE_USER_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    user_exists = get_user_model().objects.filter(
      email=payload['email']
    ).exists()

    self.assertTrue(user_exists)

  def test_short_password(self):
    """Test password to short, must be 5 char min long"""
    payload = {
      'email': 'test@test.com',
      'name': 'Test name',
      'password': 'pas' # short password
    }
    res = self.client.post(CREATE_USER_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_token_user(self):
    """Test creation of token for the user"""
    payload = {
      'email': 'test@test.com',
      'name': 'Test name',
      'password': 'Pass123'
    }
    create_user(**payload)
    res = self.client.post(TOKEN_URL, payload)

    self.assertIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_200_OK)

  def test_create_token_invalid_credential(self):
    """Test don't create token when invalid credentials"""
    create_user(
      email='test@test.com',
      password='pass123'
    )
    payload = {
      'email': 'test@test.com',
      'password': 'wrongpass123'
    }

    res = self.client.post(TOKEN_URL, payload)

    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_token_no_user(self):
    """Test email or password where not found"""
    payload = {
      'email': 'test@test.com',
      'password': 'wrongpass123'
    }

    res = self.client.post(TOKEN_URL, payload)

    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_token_missing_field(self):
    """Test email and password are required"""
    payload = {
      'email': 'haha',
      'password': ''
    }

    res = self.client.post(TOKEN_URL, payload)

    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


  def test_retrieve_url_unathorized(self):
    """Test authentication for users"""
    res = self.client.get(ME_URL)
    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
  """Test for authenticated users"""
  def setUp(self):
    self.user = create_user(
      email="test@test.com",
      password="test1234",
      name="Test"
    )
    self.client = APIClient()
    self.client.force_authenticate(user=self.user)


  def test_retrieve_profile(self):
    """Test retrieving user profile success"""
    res = self.client.get(ME_URL)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, {
      'email': "test@test.com",
      'name': 'Test'
    })

  def test_post_me_not_allowes(self):
    """Test post not allowed"""
    res = self.client.post(ME_URL, {})
    self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

  def test_update_user_profile(self):
    """Test updating user profile"""
    payload = { 'name': 'New Test', 'password': 'paspaspas' }

    res = self.client.patch(ME_URL, payload)

    self.user.refresh_from_db()
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(self.user.name, payload['name'])
    self.assertTrue(self.user.check_password(payload['password']))