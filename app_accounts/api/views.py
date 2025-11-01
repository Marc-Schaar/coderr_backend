from django.contrib.auth import authenticate


from rest_framework import  status, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app_accounts.models import User,Profile
from .serializers import RegistrationSerializer, UserSerializer, ProfileDetailSerializer, ProfileListSerializer
from .permissions import IsOwnerOrReadOnly


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating a user profile.
    Uses the primary key for lookup and restricts updates to the profile owner.
    """
    queryset= Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    lookup_field = "pk"
    permission_classes = [IsOwnerOrReadOnly]

class ProfileBusinessListView(generics.ListAPIView):
    """
    API view for listing all business user profiles.
    Returns a list of profiles where the user type is 'business'.
    """
    queryset= Profile.objects.filter(user__type="business")
    serializer_class = ProfileListSerializer

class ProfileCustomerListView(generics.ListAPIView):
    """
    API view for listing all customer user profiles.
    Returns a list of profiles where the user type is 'customer'.
    """
    queryset= Profile.objects.filter(user__type="customer")
    serializer_class = ProfileListSerializer

class LoginView(ObtainAuthToken):
    """
    API endpoint for user authentication.
    Accepts username and password, authenticates the user, and returns an authentication token on success.
    Returns error messages for invalid credentials or non-existent usernames.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user_obj = User.objects.get(username=username)
        except:
            return Response(
                {"error": "Username ist nicht vergeben"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=user_obj.username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            }
            headers = {"Status-Message": "Erfolgreiche Anmeldung."}
            return Response(data, headers=headers, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Ungültige Anfragedaten."}, status=status.HTTP_400_BAD_REQUEST
            )

class RegesistrationView(APIView):
    """
    API endpoint for user registration.
    Accepts user data, validates and creates a new user, and returns an authentication token on success.
    Returns error messages for invalid or incomplete registration data.
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
                "token": token.key,
                "username": saved_account.username,
                "email": saved_account.email,
                "user_id": saved_account.id,
            }

            headers = {"Status-Message": "User wurde erfolgreich erstellt"}
            return Response(data, headers=headers, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "Ungültige Anfragedaten."}, status=status.HTTP_400_BAD_REQUEST
            )