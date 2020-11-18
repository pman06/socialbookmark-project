from django.urls import path
from . import views

app_name = "images"

urlpatterns = [
    path('create/', views.image_create_view, name='create'),
]