from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from wardrobe_app.clothes.models import ClothingItem
from wardrobe_app.users.models import User


class ClothingItemTestMixin:

    def create_user(
        self,
        username='testuser',
        email='test@example.com',
    ):
        return User.objects.create_user(
            username=username,
            email=email,
            password='TestPassword123',
        )

    def create_image(self, name='shirt.jpg'):
        image = Image.new('RGB', (100, 100), 'white')
        image_file = BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)
        return SimpleUploadedFile(
            name,
            image_file.read(),
            content_type='image/jpeg',
        )

    def create_clothing_item(
        self,
        user,
        name='White Shirt',
    ):
        return ClothingItem.objects.create(
            user=user,
            name=name,
            description='A white shirt.',
            image=self.create_image(),
        )


class TestClothingItemList(ClothingItemTestMixin, TestCase):

    def setUp(self):
        self.user = self.create_user()

    def test_user_can_view_own_clothing_items(self):
        item = self.create_clothing_item(self.user)

        self.client.force_login(self.user)

        response = self.client.get(
            reverse('clothing_item_list')
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, item.name)

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(
            reverse('clothing_item_list')
        )

        self.assertRedirects(
            response,
            reverse('login'),
        )

    def test_user_only_sees_own_clothing_items(self):
        other_user = self.create_user(
            username='otheruser',
            email='other@example.com',
        )

        own_item = self.create_clothing_item(
            self.user,
            name='My Shirt',
        )
        other_item = self.create_clothing_item(
            other_user,
            name='Other Shirt',
        )

        self.client.force_login(self.user)

        response = self.client.get(
            reverse('clothing_item_list')
        )

        self.assertContains(response, own_item.name)
        self.assertNotContains(response, other_item.name)


class TestClothingItemDetail(ClothingItemTestMixin, TestCase):

    def setUp(self):
        self.user = self.create_user()
        self.item = self.create_clothing_item(self.user)

    def test_user_can_view_own_clothing_item(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                'clothing_item_detail',
                kwargs={'pk': self.item.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.name)

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(
            reverse(
                'clothing_item_detail',
                kwargs={'pk': self.item.pk},
            )
        )

        self.assertRedirects(
            response,
            reverse('login'),
        )

    def test_user_cannot_view_other_users_clothing_item(self):
        other_user = self.create_user(
            username='otheruser',
            email='other@example.com',
        )

        other_item = self.create_clothing_item(other_user)

        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                'clothing_item_detail',
                kwargs={'pk': other_item.pk},
            )
        )

        self.assertEqual(response.status_code, 404)


class TestClothingItemCreate(ClothingItemTestMixin, TestCase):

    def setUp(self):
        self.user = self.create_user()

    def test_user_can_create_clothing_item(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('clothing_item_create'),
            {
                'name': 'Blue Jeans',
                'description': 'My favorite jeans.',
                'image': self.create_image('jeans.jpg'),
            },
        )

        item = ClothingItem.objects.get(
            name='Blue Jeans'
        )

        self.assertRedirects(
            response,
            reverse(
                'clothing_item_detail',
                kwargs={'pk': item.pk},
            ),
        )

        self.assertEqual(item.user, self.user)
        self.assertEqual(
            item.description,
            'My favorite jeans.',
        )

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(
            reverse('clothing_item_create')
        )

        self.assertRedirects(
            response,
            reverse('login'),
        )


class TestClothingItemUpdate(ClothingItemTestMixin, TestCase):

    def setUp(self):
        self.user = self.create_user()
        self.item = self.create_clothing_item(self.user)

    def test_user_can_update_own_clothing_item(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                'clothing_item_update',
                kwargs={'pk': self.item.pk},
            ),
            {
                'name': 'Updated Shirt',
                'description': 'Updated description.',
            },
        )

        self.assertRedirects(
            response,
            reverse(
                'clothing_item_detail',
                kwargs={'pk': self.item.pk},
            ),
        )

        self.item.refresh_from_db()

        self.assertEqual(
            self.item.name,
            'Updated Shirt',
        )
        self.assertEqual(
            self.item.description,
            'Updated description.',
        )

    def test_user_cannot_update_other_users_clothing_item(self):
        other_user = self.create_user(
            username='otheruser',
            email='other@example.com',
        )

        other_item = self.create_clothing_item(other_user)

        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                'clothing_item_update',
                kwargs={'pk': other_item.pk},
            ),
            {
                'name': 'Hacked Item',
                'description': 'Hacked description.',
            },
        )

        self.assertEqual(response.status_code, 404)

        other_item.refresh_from_db()

        self.assertEqual(
            other_item.name,
            'White Shirt',
        )
        self.assertEqual(
            other_item.description,
            'A white shirt.',
        )


class TestClothingItemDelete(ClothingItemTestMixin, TestCase):

    def setUp(self):
        self.user = self.create_user()
        self.item = self.create_clothing_item(self.user)

    def test_user_can_delete_own_clothing_item(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                'clothing_item_delete',
                kwargs={'pk': self.item.pk},
            )
        )

        self.assertRedirects(
            response,
            reverse('clothing_item_list'),
        )

        self.assertFalse(
            ClothingItem.objects.filter(
                pk=self.item.pk
            ).exists()
        )

    def test_user_cannot_delete_other_users_clothing_item(self):
        other_user = self.create_user(
            username='otheruser',
            email='other@example.com',
        )

        other_item = self.create_clothing_item(other_user)

        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                'clothing_item_delete',
                kwargs={'pk': other_item.pk},
            )
        )

        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            ClothingItem.objects.filter(
                pk=other_item.pk
            ).exists()
        )
