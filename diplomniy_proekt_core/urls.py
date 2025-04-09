from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView
from django.template.defaulttags import url
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, )
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from films import views
from users_reviews.views import (RegisterView, register, reviews_create, ReviewsListView, ReviewsRetrievView,
                                 ReviewsUpdateView, ReviewsDestroyView, rating_create)

urlpatterns = [

    #path(r'^$', views.index, name='index'),
    #path(r'^login/$', LoginView.as_view(template_name='login.html'), name='login'),
    #path(r'^logout/$', LogoutView.as_view(), name='logout'),
    #path('', include('social_django.urls', namespace='social')),

    path('', views.main, name='main'),
    path('admin/', admin.site.urls),
    path('base/', views.base),
    path('films/', views.film_list, name='films_list'),

    path('', include('films.urls')),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('api-auth/', include('rest_framework.urls')),
    path('delete/<int:film_id>/', views.delete_film, name='delete_film'),
    path('details/<int:film_id>/', views.film_details, name='film_details'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('register/', register, name='register'),

    path('', include('users_reviews.urls')),
    path('login/', ReviewsListView.as_view(), name='comment-list'),
    path('reviews_create/<int:film_id>/', reviews_create, name='reviews_create'),
    path('rating_create/<int:film_id>/', rating_create, name='rating_create'),
    path('reviews/', ReviewsListView.as_view(), name='comment-list'),
    path('reviews/<int:pk>/', ReviewsRetrievView.as_view(), name='comment-retrieve'),
    path('reviews/<int:pk>/update/', ReviewsUpdateView.as_view(), name='comment-update'),
    path('reviews/<int:pk>/delete/', ReviewsDestroyView.as_view(), name='comment-destroy'),

    path('', include('social_django.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
]

SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']