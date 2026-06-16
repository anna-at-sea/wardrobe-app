from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


# class UserLoginRequiredMixin(LoginRequiredMixin):

#     def handle_no_permission(self):
#         messages.warning(self.request, "You are not logged in! Please log in.")
#         return redirect('login')


class UserPermissionMixin:

    def dispatch(self, request, *args, **kwargs):
        auth = request.user.is_authenticated
        username_in_kwargs = kwargs.get('username')
        user_match = (kwargs.get('username') == request.user.username)
        if auth and username_in_kwargs and not user_match:
            messages.warning(
                request, "You don't have permission to view or edit other user."
            )
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)
