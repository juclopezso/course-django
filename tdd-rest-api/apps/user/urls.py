from django.urls import path

from apps.user import views


app_name = 'user'

urlpatterns = [
  path('token/', views.CreateTokenView.as_view(), name='token'),
  path('create/', views.CreateUserView.as_view(), name='create'),
  path('me/', views.ManageUserView.as_view(), name='me')
]
