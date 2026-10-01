from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from wardrobe_app import utils
from wardrobe_app.users.forms import (EmailOrUsernameAuthenticationForm,
                                      UserCreateForm, UserDeleteForm,
                                      UserUpdateForm)
from wardrobe_app.users.models import User


class UserProfileView(
    utils.UserLoginRequiredMixin,
    utils.UserPermissionMixin,
    SuccessMessageMixin, DetailView
):
    model = User
    template_name = 'pages/users/profile.html'
    context_object_name = 'user'
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs["username"])


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'layouts/base_form.html'
    authentication_form = EmailOrUsernameAuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _("Log in"),
            'button_text': _("Log in")
        })
        return context

    def get_success_url(self):
        return reverse_lazy(
            'user_profile', kwargs={'username': self.request.user.username}
        )

    def get_success_message(self, *args, **kwargs):
        return _("You are logged in")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(
            request,
            messages.INFO,
            _("You are logged out")
        )
        return super().dispatch(request, *args, **kwargs)


class UserFormCreateView(
    SuccessMessageMixin, CreateView
):
    model = User
    form_class = UserCreateForm
    template_name = 'layouts/base_form.html'

    def get_success_message(self, *args, **kwargs):
        return _("User is registered successfully")

    def get_success_url(self):
        return reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _("Sign Up"),
            'button_text': _("Sign Up")
        })
        return context


class UserFormUpdateView(
    utils.UserLoginRequiredMixin, utils.UserPermissionMixin,
    SuccessMessageMixin, UpdateView
):
    model = User
    form_class = UserUpdateForm
    template_name = 'layouts/base_form.html'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'username': self.object.username})

    def get_success_message(self, *args, **kwargs):
        return _("User is updated successfully")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _("Update user"),
            'button_text': _("Update")
        })
        return context


class UserPasswordChangeView(
    utils.UserLoginRequiredMixin, utils.UserPermissionMixin,
    SuccessMessageMixin, PasswordChangeView
):
    form_class = PasswordChangeForm
    template_name = 'layouts/base_form.html'

    def get_success_url(self):
        return reverse_lazy(
            'user_profile', kwargs={'username': self.request.user.username}
        )

    def get_success_message(self, *args, **kwargs):
        return _("Password is changed successfully")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _("Change password"),
            'button_text': _("Change")
        })
        return context


class UserFormDeleteView(
    utils.UserLoginRequiredMixin, utils.UserPermissionMixin,
    SuccessMessageMixin, DeleteView
):
    form_class = UserDeleteForm
    model = User
    template_name = 'layouts/base_form.html'
    success_url = reverse_lazy('index')

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_success_message(self, *args, **kwargs):
        return _("Account deleted successfully")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'delete_prompt': (
                _("Are you sure you want to delete your account?")),
            'button_text': _("Yes, delete")
        })
        return context

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.add_message(
                self.request,
                messages.ERROR,
                _("This account cannot be deleted")
            )
            return redirect('user_profile', username=self.request.user.username)
