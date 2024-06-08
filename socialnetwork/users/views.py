from rest_framework import generics, permissions, filters, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.throttling import AnonRateThrottle
from django.contrib.auth import get_user_model,logout
from .models import CustomUser, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions


User = get_user_model()

class UserSignUpView(generics.CreateAPIView):
    """
    API view for user sign up.
    Allows users to create a new account.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLogInView(TokenObtainPairView):
    """
    API view for user login.
    Allows users to obtain a JSON Web Token (JWT) for authentication.
    """
    serializer_class = TokenObtainPairSerializer

class UserLogOutView(generics.GenericAPIView):
    """
    API view for user logout.
    Allows users to log out and invalidate their JWT.
    """
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

class UserSearchView(generics.ListAPIView):
    """
    API view for user search.
    Allows users to search for other users by email or name.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'name']
    
class FriendRequestCreateView(generics.CreateAPIView):
    """
    API view for creating a friend request.
    Allows users to send a friend request to another user.
    """
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    throttle_classes = [AnonRateThrottle, ScopedRateThrottle]
    throttle_scope = 'friend_requests'
    permission_classes = [permissions.IsAuthenticated]
    # handle to_user should not be same as from_user


    def perform_create(self, serializer):
        to_user = serializer.validated_data.get('to_user')
        if to_user == self.request.user:
            raise exceptions.ValidationError("Cannot send friend request to yourself.")
        serializer.save(from_user=self.request.user)

class FriendRequestAcceptView(generics.UpdateAPIView):
    """
    API view for accepting a friend request.
    Allows users to accept a friend request they have received.
    """
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def update(self, request, *args, **kwargs):
        friend_request = self.get_object()
        friend_request.accepted = True
        friend_request.save()

        serializer = self.get_serializer(friend_request)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FriendRequestRejectView(generics.DestroyAPIView):
    """
    API view for rejecting a friend request.
    Allows users to reject a friend request they have received.
    """
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

class FriendListView(generics.ListAPIView):
    """
    API view for retrieving a user's friends list.
    Allows authenticated users to retrieve a list of their friends.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):          
        if self.request.user.is_authenticated:
            accepted_requests = FriendRequest.objects.filter(to_user=self.request.user, accepted=True)
            if accepted_requests.exists():
                return accepted_requests
            else:
                raise exceptions.NotFound("You have no friends.")
        else:
            return FriendRequest.objects.none()


class PendingFriendRequestListView(generics.ListAPIView):
    """
    API view for retrieving a user's pending friend requests.
    Allows authenticated users to retrieve a list of friend requests they have received but not yet accepted.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return self.request.user.received_requests.filter(accepted=False)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "No pending friend requests."})