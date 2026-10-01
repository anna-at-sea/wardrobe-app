from django.contrib import admin
from django.urls import include, path

from wardrobe_app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('users/', include('wardrobe_app.users.urls')),
    path('admin/', admin.site.urls),
]
