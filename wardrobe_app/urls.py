from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from wardrobe_app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('users/', include('wardrobe_app.users.urls')),
    path('clothes/', include('wardrobe_app.clothes.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
