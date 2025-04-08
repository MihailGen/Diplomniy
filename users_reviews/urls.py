from django.urls import path, include
from .views import register, reviews_create
from users_reviews import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/', views.profile_page, name='profile'),
]