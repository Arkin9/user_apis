from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from django.core.mail import send_mail
from django.conf import settings
from user.utils import (
    email_new_registration, email_forget_password, email_password_reset_success,
    email_password_change_success
)
from user.serializers import (
    UserSerializer, AuthTokenSerializer, ForgetPasswordSerializer,
    ResetPasswordSerializer, ChangePasswordSerializer
)

# Create your views here.

User = get_user_model()

class CreateUserView(CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

    def perform_create(self, serializer):

        user = serializer.save()
        email_new_registration(user)
        return user

    def create(self, request, *args, **kwargs):

        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "User registered successfully."},
            status=status.HTTP_201_CREATED
        )


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ForgetPasswordView(APIView):
    """APIView for forget password"""

    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            # SEND EMAIL
            email_forget_password(user, token)

            return Response(
                {"message": "Password reset email has been sent."},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ResetPasswordView(APIView):
    """APIView for reset password"""

    def post(self, request, token):
        serializer = ResetPasswordSerializer(
            data=request.data,
            context={'email': request.data.get('email')}
        )

        if serializer.is_valid():
            user = User.objects.get(email=request.data.get('email'))
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()

            email_password_reset_success(user)

            return Response(
                {"message": "Password has been reset successfully."},
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ChangePasswordView(APIView):
    """APIView for changepassword."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response(
                    {'message': 'Old password is incorrect.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(new_password)
            user.save()

            email_password_change_success(user)

            update_session_auth_hash(request, user)
            return Response(
                {'message': 'Password changed successfully'},
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
