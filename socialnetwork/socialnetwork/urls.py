from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.UserSignUpView.as_view(), name='signup'),
    path('login/', views.UserLogInView.as_view(), name='login'),
    path('logout/', views.UserLogOutView.as_view(), name='logout'),
    path('users/', views.UserSearchView.as_view(), name='user_search'),
    path('friend-requests/', views.FriendRequestCreateView.as_view(), name='friend_request_create'),
    path('friend-requests/<int:pk>/accept/', views.FriendRequestAcceptView.as_view(), name='friend_request_accept'),
    path('friend-requests/<int:pk>/reject/', views.FriendRequestRejectView.as_view(), name='friend_request_reject'),
    path('friends/', views.FriendListView.as_view(), name='friend_list'),
    path('friend-requests/pending/', views.PendingFriendRequestListView.as_view(), name='pending_friend_request_list'),
]