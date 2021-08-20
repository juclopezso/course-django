from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

  def setUp(self):
    self.client = Client()
    # creates admin user
    self.admin_user = get_user_model().objects.create_superuser(
      email='admin@test.com', password='Pass123'
    )
    self.client.force_login(self.admin_user)
    # creates normal user
    self.user = get_user_model().objects.create_user(
      email='user@test.com', password='Pass123', name='Juan Test'
    )

  def test_users_listed(self):
    """Test normal users are listed"""
    url = reverse('admin:core_user_changelist')
    res = self.client.get(url)

    self.assertContains(res, self.user.email)
    self.assertContains(res, self.user.name)

  # def test_user_change_page(self):
  #   """Test edit page by user"""
  #   # /admin/core/user/1
  #   url = reverse('admin:core_user_change', args=[self.user.id])
  #   res = self.client.get(url)

  #   self.assertEqual(res.status_code, 200)
