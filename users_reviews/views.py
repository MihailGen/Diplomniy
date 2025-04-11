from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .forms import *
from .forms import UserRegisterForm
from .models import Reviews, Ratings
from .serializers import RegisterSerializer, ReviewsSerializer, RatingsSerializer

User = get_user_model()


@require_POST
def reviews_create(request, film_id):
    reviews = Reviews.objects.create(user=request.user, reviews_body=request.POST.get('reviews'), film_id=film_id)
    reviews.save()
    return redirect('film_details', film_id)


@require_POST
def rating_create(request, film_id):
    rating = Ratings.objects.create(user=request.user, rating=request.POST.get('rating'), film_id=film_id)
    rating.save()
    return redirect('film_details', film_id)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')
            return redirect('films_list')
    else:
        form = UserRegisterForm()
        return render(request, 'users_reviews/profile.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')
            return redirect('films_list')
    else:
        form = UserRegisterForm()
        return render(request, 'users_reviews/register.html', {'form': form})


@login_required
def profile_page(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile_page')
    else:
        form = UserProfileForm(instance=user)
        return render(request, 'users_reviews/profile.html', {'form': form})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ReviewsListView(generics.ListAPIView):
    # Класс-контроллер для просомтра списка объектов модели Reviews
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


class ReviewsRetrievView(generics.RetrieveAPIView):
    # Класс-контроллер для просмотра отдельного объекта модели Reviews
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


class ReviewsUpdateView(generics.UpdateAPIView):
    # Класс-контроллер для редактирования объектов модели Reviews
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


class ReviewsDestroyView(generics.DestroyAPIView):
    # Класс-контроллер для удаления объектов модели Reviews
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


# Ratings Views
class RatingsCreateView(generics.CreateAPIView):
    # Класс-контроллер для создани объектов модели Ratings
    queryset = Ratings.objects.all()
    serializer_class = RatingsSerializer


class RatingsListView(generics.ListAPIView):
    # Класс-контроллер для просомтра списка объектов модели Ratings
    queryset = Ratings.objects.all()
    serializer_class = RatingsSerializer


class RatingsRetrievView(generics.RetrieveAPIView):
    # Класс-контроллер для просмотра отдельного объекта модели Ratings
    queryset = Ratings.objects.all()
    serializer_class = RatingsSerializer


class RatingsUpdateView(generics.UpdateAPIView):
    # Класс-контроллер для редактирования объектов модели Ratings
    queryset = Ratings.objects.all()
    serializer_class = RatingsSerializer


class RatingsDestroyView(generics.DestroyAPIView):
    # Класс-контроллер для удаления объектов модели Ratings
    queryset = Ratings.objects.all()
    serializer_class = RatingsSerializer
