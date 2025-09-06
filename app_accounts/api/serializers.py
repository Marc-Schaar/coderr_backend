from rest_framework import serializers
from app_accounts.models import User

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
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "created_at",
        ]

class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True) 
    password = serializers.CharField(write_only=True, required=True)
    repeated_password = serializers.CharField(write_only=True) 
    type = serializers.CharField(required=True)
   
    class Meta:
        model = User
        fields = ["username", "email", "password", "repeated_password", "type"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

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

