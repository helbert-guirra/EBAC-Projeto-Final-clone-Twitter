from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User


class UserRegistrationTest(TestCase):

    def test_register_page_loads(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_register_creates_user(self):
        response = self.client.post(reverse("register"), {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "senhaforte123!",
            "password2": "senhaforte123!",
        })
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_redirects_to_feed(self):
        response = self.client.post(reverse("register"), {
            "username": "testuser2",
            "email": "test2@test.com",
            "password1": "senhaforte123!",
            "password2": "senhaforte123!",
        })
        self.assertRedirects(response, reverse("feed"))


class UserLoginTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="helbert",
            password="senhaforte123!"
        )

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_with_correct_credentials(self):
        response = self.client.post(reverse("login"), {
            "username": "helbert",
            "password": "senhaforte123!",
        })
        self.assertRedirects(response, reverse("feed"))

    def test_login_with_wrong_password(self):
        response = self.client.post(reverse("login"), {
            "username": "helbert",
            "password": "senhaerrada",
        })
        self.assertEqual(response.status_code, 200)  # fica na página de login


class ProfileTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="helbert",
            password="senhaforte123!"
        )
        self.client.login(username="helbert", password="senhaforte123!")

    def test_profile_page_loads(self):
        response = self.client.get(reverse("profile", kwargs={"username": "helbert"}))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_page_loads(self):
        response = self.client.get(reverse("edit_profile"))
        self.assertEqual(response.status_code, 200)

    def test_follow_toggle(self):
        other = User.objects.create_user(username="outro", password="senhaforte123!")
        response = self.client.post(reverse("follow_toggle", kwargs={"user_id": other.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.following.filter(pk=other.pk).exists())

    def test_unfollow_toggle(self):
        other = User.objects.create_user(username="outro", password="senhaforte123!")
        self.user.following.add(other)
        response = self.client.post(reverse("follow_toggle", kwargs={"user_id": other.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user.following.filter(pk=other.pk).exists())
