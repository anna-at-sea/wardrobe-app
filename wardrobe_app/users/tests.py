from django.test import TestCase
from django.urls import reverse

from wardrobe_app.users.models import User


class UserTestMixin:

    def create_user(self, username='testuser', email='test@example.com'):
        return User.objects.create_user(
            username=username,
            email=email,
            password='TestPassword123',
            first_name='Test',
            last_name='User',
        )


class TestUserProfileRead(UserTestMixin, TestCase):

    def setUp(self):
        self.user = self.create_user()

    def test_authenticated_user_can_view_own_profile(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                'user_profile',
                kwargs={'username': self.user.username}
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(
            reverse(
                'user_profile',
                kwargs={'username': self.user.username}
            )
        )

        self.assertRedirects(
            response,
            reverse('login')
        )

    def test_user_cannot_view_other_user_profile(self):
        other_user = self.create_user(
            username='otheruser',
            email='other@example.com'
        )

        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                'user_profile',
                kwargs={'username': other_user.username}
            )
        )

        self.assertRedirects(response, reverse('index'))


class TestUserCreate(UserTestMixin, TestCase):

    def test_user_can_register(self):
        response = self.client.post(
            reverse('user_create'),
            {
                'first_name': 'New',
                'last_name': 'User',
                'username': 'newuser',
                'email': 'new@example.com',
                'password1': 'TestPassword123',
                'password2': 'TestPassword123',
            }
        )

        self.assertRedirects(response, reverse('login'))

        user = User.objects.get(username='newuser')

        self.assertEqual(user.email, 'new@example.com')
        self.assertEqual(user.first_name, 'New')
        self.assertTrue(user.check_password('TestPassword123'))


class TestUserUpdate(UserTestMixin, TestCase):

    def setUp(self):
        self.user = self.create_user()

    def test_user_can_update_own_profile(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                'user_update',
                kwargs={'username': self.user.username}
            ),
            {
                'first_name': 'Updated',
                'last_name': 'Name',
                'username': 'updateduser',
                'email': 'updated@example.com',
            }
        )

        self.assertRedirects(
            response,
            reverse(
                'user_profile',
                kwargs={'username': 'updateduser'}
            )
        )

        self.user.refresh_from_db()

        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')

    def test_user_cannot_update_other_user(self):
        other_user = self.create_user(
            username='otheruser',
            email='other@example.com'
        )

        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                'user_update',
                kwargs={'username': other_user.username}
            ),
            {
                'first_name': 'Hacked',
                'last_name': 'User',
                'username': 'hacked',
                'email': 'hacked@example.com',
            }
        )

        self.assertRedirects(response, reverse('index'))

        other_user.refresh_from_db()

        self.assertEqual(other_user.first_name, 'Test')
        self.assertEqual(other_user.username, 'otheruser')


class TestUserPasswordChange(UserTestMixin, TestCase):

    def setUp(self):
        self.user = self.create_user()

    def test_user_can_change_password(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                'user_password_change',
                kwargs={'username': self.user.username}
            ),
            {
                'old_password': 'TestPassword123',
                'new_password1': 'NewPassword123',
                'new_password2': 'NewPassword123',
            }
        )

        self.assertRedirects(
            response,
            reverse(
                'user_profile',
                kwargs={'username': self.user.username}
            )
        )

        self.user.refresh_from_db()

        self.assertTrue(
            self.user.check_password('NewPassword123')
        )

    def test_user_cannot_change_other_user_password(self):
        other_user = self.create_user(
            username='otheruser',
            email='other@example.com'
        )

        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                'user_password_change',
                kwargs={'username': other_user.username}
            ),
            {
                'old_password': 'TestPassword123',
                'new_password1': 'NewPassword123',
                'new_password2': 'NewPassword123',
            }
        )

        self.assertRedirects(response, reverse('index'))

        other_user.refresh_from_db()

        self.assertTrue(
            other_user.check_password('TestPassword123')
        )


class TestUserDelete(UserTestMixin, TestCase):

    def setUp(self):
        self.user = self.create_user()

    def test_user_can_delete_own_account_with_correct_password(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                'user_delete',
                kwargs={'username': self.user.username}
            ),
            {
                'password_confirm': 'TestPassword123',
            }
        )

        self.assertRedirects(response, reverse('index'))

        self.assertFalse(
            User.objects.filter(pk=self.user.pk).exists()
        )

    def test_user_cannot_delete_account_with_wrong_password(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                'user_delete',
                kwargs={'username': self.user.username}
            ),
            {
                'password_confirm': 'WrongPassword123',
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            User.objects.filter(pk=self.user.pk).exists()
        )

        self.assertContains(response, 'Incorrect password.')

    def test_user_cannot_delete_other_user(self):
        other_user = self.create_user(
            username='otheruser',
            email='other@example.com'
        )

        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                'user_delete',
                kwargs={'username': other_user.username}
            ),
            {
                'password_confirm': 'TestPassword123',
            }
        )

        self.assertRedirects(response, reverse('index'))

        self.assertTrue(
            User.objects.filter(pk=other_user.pk).exists()
        )


class TestUserAuthentication(UserTestMixin, TestCase):

    def setUp(self):
        self.user = self.create_user()

    def test_user_can_login_with_username(self):
        response = self.client.post(
            reverse('login'),
            {
                'username': 'testuser',
                'password': 'TestPassword123',
            }
        )

        self.assertRedirects(
            response,
            reverse(
                'user_profile',
                kwargs={'username': self.user.username}
            )
        )

    def test_user_can_login_with_email(self):
        response = self.client.post(
            reverse('login'),
            {
                'username': 'test@example.com',
                'password': 'TestPassword123',
            }
        )

        self.assertRedirects(
            response,
            reverse(
                'user_profile',
                kwargs={'username': self.user.username}
            )
        )

    def test_user_cannot_login_with_wrong_password(self):
        response = self.client.post(
            reverse('login'),
            {
                'username': 'testuser',
                'password': 'WrongPassword123',
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Invalid username/email or password'
        )

    def test_user_can_logout(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('index'))

        response = self.client.get(
            reverse(
                'user_profile',
                kwargs={'username': self.user.username}
            )
        )

        self.assertRedirects(
            response,
            reverse('login')
        )
