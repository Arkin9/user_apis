"""Serializers for the user API View."""
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serilizer for the user object."""

    class Meta:
        model = User
        fields = ['email', 'contact_number', 'password', 'name', 'profile_image', 'birthdate']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length':5}
        }

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return User.objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""

    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password,
        )

        if not user:
            msg = 'Unable to authenticate with provided credientials.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ForgetPasswordSerializer(serializers.Serializer):
    """Serializer for forget password."""

    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise ValidationError("User with this email does not exist.")
        return value


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for reset password. """

    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError('New password and confirm password do not match.')
        return data

    def validate_token(self, value):
        try:
            user  = User.objects.get(email=self.context.get('email'))
            if not default_token_generator.check_token(user, value):
                raise serializers.ValidationError('Invalid token.')
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found.')
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for change password."""

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError('New password and confirm password do not match.')
        return data
