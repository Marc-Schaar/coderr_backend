from rest_framework import serializers
from app_accounts.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model exposing id, email, and username fields.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "type",
        ]


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for User model exposing first_name, last_name, and username fields.
    """

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")


class ProfileListSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile model exposing related user information (username, first_name, last_name, type),
    uploaded file, and upload timestamp in a formatted manner.
    """

    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(
        source="user.first_name", required=False, allow_blank=True
    )
    last_name = serializers.CharField(
        source="user.last_name", required=False, allow_blank=True
    )
    type = serializers.CharField(source="user.type", read_only=True)
    uploaded_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "uploaded_at",
            "type",
        ]


class ProfileDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile model providing detailed user-related fields (username, first_name, last_name, email, type),
    profile-specific fields, and custom update logic to handle nested user updates.
    """

    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(
        source="user.first_name", required=False, allow_blank=True
    )
    last_name = serializers.CharField(
        source="user.last_name", required=False, allow_blank=True
    )
    email = serializers.EmailField(source="user.email", required=False)
    type = serializers.CharField(source="user.type", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        ]

    def update(self, instance, validated_data):
        user_data = {}
        if "user" in validated_data:
            user_data = validated_data.pop("user")

        if "first_name" in validated_data:
            instance.user.first_name = validated_data.pop("first_name")
        if "last_name" in validated_data:
            instance.user.last_name = validated_data.pop("last_name")
        if "email" in validated_data:
            instance.user.email = validated_data.pop("email")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
        instance.user.save()

        return instance


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration handling username, email, password, repeated password, and user type.
    Includes validation for password match and uniqueness of username and email,
    and creates a new user with the provided data.
    """

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "repeated_password", "type"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError("Passwort stimmt nicht überein")
        return data

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username existiert bereits")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email existiert bereits")
        return value

    def create(self, validated_data):
        validated_data.pop("repeated_password")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            type=validated_data.get("type"),
        )
        return user
