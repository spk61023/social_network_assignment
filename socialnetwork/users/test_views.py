from django.urls import reverse
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser, FriendRequest
from .serializers import UserSerializer
import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.parametrize(
    "samesite_strict,did_already_redirect,expect_redirect",
    [
        (True, False, True),
        (True, True, False),
        (False, False, False),
    ],
)
def test_samesite_strict(
    client,
    samesite_strict,
    settings,
    google_provider_settings,
    did_already_redirect,
    expect_redirect,
    db,
):
    settings.SESSION_COOKIE_SAMESITE = "Strict" if samesite_strict else "Lax"
    query = "?state=123"
    resp = client.get(
        reverse("google_callback") + query + ("&_redir" if did_already_redirect else "")
    )
    if expect_redirect:
        assertTemplateUsed(resp, "socialaccount/login_redirect.html")
        assert (
            resp.context["redirect_to"]
            == reverse("google_callback") + query + "&_redir="
        )
    else:
        assertTemplateUsed(resp, "socialaccount/authentication_error.html")

class FriendListViewTestCase(APITestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(email='user1@example.com', password='password1')
        self.user2 = CustomUser.objects.create_user(email='user2@example.com', password='password2')
        self.user3 = CustomUser.objects.create_user(email='user3@example.com', password='password3')
        self.friend_request = FriendRequest.objects.create(sender=self.user2, receiver=self.user1, accepted=True)
        self.url = reverse('friend-list')

    def test_friend_list_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, UserSerializer(self.user2).data)

    def test_friend_list_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_friend_list_empty(self):
        self.client.force_authenticate(user=self.user3)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def tearDown(self):
        CustomUser.objects.all().delete()
        FriendRequest.objects.all().delete()