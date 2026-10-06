from django.db import models
from django.utils.translation import gettext_lazy as _

from wardrobe_app.users.models import User
from wardrobe_app.utils import image_upload_path, validate_image


class ClothingItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='clothing_items',
    )
    name = models.CharField(
        _("name"),
        max_length=100,
    )
    description = models.TextField(
        _("description"),
        blank=True,
    )
    image = models.ImageField(
        upload_to=image_upload_path,
        validators=[validate_image],
        help_text=_("Upload JPEG or PNG image up to 15MB.")
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("clothing item")
        verbose_name_plural = _("clothing items")
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.name:
            num = 1
            name = f"ClothingItem-{num}"
            while ClothingItem.objects.filter(
                user=self.user,
                name=name,
            ).exists():
                num += 1
                name = f"ClothingItem-{num}"
            self.name = name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
