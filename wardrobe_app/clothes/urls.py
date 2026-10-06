from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.ClothingItemListView.as_view(),
        name='clothing_item_list',
    ),
    path(
        'create/',
        views.ClothingItemCreateView.as_view(),
        name='clothing_item_create',
    ),
    path(
        '<int:pk>/',
        views.ClothingItemDetailView.as_view(),
        name='clothing_item_detail',
    ),
    path(
        '<int:pk>/update/',
        views.ClothingItemUpdateView.as_view(),
        name='clothing_item_update',
    ),
    path(
        '<int:pk>/delete/',
        views.ClothingItemDeleteView.as_view(),
        name='clothing_item_delete',
    ),
]
