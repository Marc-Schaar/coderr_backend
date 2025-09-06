from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import  status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer, UserSerializer


class RegesistrationView(APIView):
    """
    User registration endpoint.

    POST:
        Registers a new user using the RegistrationSerializer.
        On success, returns the created user's info and auth token.
        On failure, returns validation errors.
    """
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                "username": saved_account.username,
                "email": saved_account.email,
                "token": token.key,
                "user_id": saved_account.id,
            }

            headers = {"Status-Message": "User wurde erfolgreich erstellt"}
            return Response(data, headers=headers, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "Ungültige Anfragedaten."}, status=status.HTTP_400_BAD_REQUEST
            )