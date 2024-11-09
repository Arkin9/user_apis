from django.urls import path
from user.views import (
    CreateUserView, CreateTokenView, UserListView,
    ForgetPasswordView, ResetPasswordView, ChangePasswordView
)

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('', UserListView.as_view(), name='list'),
    path('forget-password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('reset-password/<str:token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]
