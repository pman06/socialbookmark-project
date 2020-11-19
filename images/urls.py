from django.urls import path
from . import views

app_name = "images"

urlpatterns = [
    path('create/', views.image_create_view, name='create'),
    path('details/<int:id>/<slug:slug>/', views.image_detail, name ='detail'),
    path('like/', views.image_like_view, name='like'),
    path('', views.image_list_view, name='list'),
]
