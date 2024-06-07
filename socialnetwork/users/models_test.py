from django.test import TestCase
from django.contrib.auth import get_user_model

# from socialnetwork.users.models import CustomUser

class CustomUserManagerTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        email = 'test@example.com'
        name = 'Test User'
        password = 'testpassword'
        user = User.objects.create_user(email=email, name=name, password=password)

        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_create_user_no_email(self):
        User = get_user_model()
        with self.assertRaises(ValueError):
            User.objects.create_user(None, 'Test User', 'password123')


    def test_create_superuser(self):
        User = get_user_model()
        email = 'admin@example.com'
        password = 'adminpassword'
        user = User.objects.create_superuser(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_superuser)