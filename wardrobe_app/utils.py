from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.utils.translation import gettext as _


class UserLoginRequiredMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        messages.warning(self.request, _("You are not logged in! Please log in."))
        return redirect('login')


class UserPermissionMixin:

    def dispatch(self, request, *args, **kwargs):
        auth = request.user.is_authenticated
        username_in_kwargs = kwargs.get('username')
        user_match = (kwargs.get('username') == request.user.username)
        if auth and username_in_kwargs and not user_match:
            messages.warning(
                request, _("You don't have permission to view or edit other user.")
            )
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


def validate_image(image):
    max_size_mb = 15
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(_(f"Image size should not exceed {max_size_mb} MB."))


def image_upload_path(instance, filename):
    extension = filename.split('.')[-1]
    model_name = instance.__class__.__name__.lower()
    folder = f"{model_name}s"
    if instance.name:
        name = instance.name
    else:
        name = f"{model_name}-{instance.pk or 'unassigned'}"
    return f"{folder}/{name}.{extension.lower()}"
