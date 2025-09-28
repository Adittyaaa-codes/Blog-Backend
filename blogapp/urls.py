from django.urls import path
from .views import BlogView

urlpatterns = [
    path('home/', BlogView.as_view(), name='home page'),
    path('home/<uuid:pk>/', BlogView.as_view(), name='blog-detail'),  # New route for UUID
]