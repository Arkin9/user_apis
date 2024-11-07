from django.urls import path
from user.views import CreateUserView, CreateTokenView, UserListView

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('', UserListView.as_view(), name='list')
]
