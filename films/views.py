from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.template import loader
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from social_core.backends.utils import load_backends

from films.models import Film, Film_details, Genre, Tags
from films.serializers import FilmSerializer, Film_detailsSerializer, GenreSerializer, TagSerializer
from users_reviews.models import Reviews, Ratings


def main(request):
    posters_list = Film_details.objects.select_related('film').values('poster', 'film').all()
    film_list = Film_details.objects.all().select_related('film')
    print(film_list)
    return render(request, 'films/main.html', {'posters_list': posters_list,'film_list': film_list})

'''
def login(request):
    return render(request, 'login.html')
'''


@login_required
def index(request):
    return HttpResponse('OK, Google!')

"""
@login_required
def home(request):
    return render(request, 'home.html')
"""

def login(request):
    social_backends = load_backends()
    context = {'social_backends': social_backends}
    return render(request, 'login.html', context)


def base(request):
    return render(request, 'films/base.html')


def film_details(request, film_id):
    film = Film_details.objects.get(id=film_id)
    reviews = Reviews.objects.filter(film=film_id)
    try:
        #rating = Ratings.objects.get(film_id=film_id, user_id=request.user).latest(field_name=id)
        rating = Ratings.objects.get(film_id=film_id, user_id=request.user)
    except:
        rating = 0
    return render(request, 'films/film_details.html', {'film': film, 'reviews': reviews, 'rating': rating})


def posters(request, film_id):
    posters_list = Film_details.objects.all().posters
    return render(request, 'films/main.html', {'posters_list': posters_list})


def film_list(request):
    film_list = Film_details.objects.all().select_related('film')
    return render(request, 'films/films.html', {'film_list': film_list})


@require_POST
def delete_film(film_id):
    film = get_object_or_404(Film, pk=film_id)
    film.delete()
    return redirect('films')


class SearchResultsView(ListView):
    model = Film
    template_name = 'films/search_results.html'

    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        film_list = Film.objects.filter(
            Q(title__icontains=query)
        )
        return film_list


class FilmViewSet(viewsets.ModelViewSet):  # Класс-контроллер, для создания набора контроллеров на осное VieSet
    queryset = Film.objects.all()  # Набор данных для работы в контроллерах
    serializer_class = FilmSerializer  # класс-сериализатор


class Film_detailsViewSet(viewsets.ModelViewSet):  # Класс-контроллер, для создания набора контроллеров на осное VieSet
    queryset = Film_details.objects.all()  # Набор данных для работы в контроллерах
    serializer_class = Film_detailsSerializer  # класс-сериализатор


class GenreViewSet(viewsets.ModelViewSet):  # Класс-контроллер, для создания набора контроллеров на осное VieSet
    queryset = Genre.objects.all()  # Набор данных для работы в контроллерах
    serializer_class = GenreSerializer  # класс-сериализатор


class TagViewSet(viewsets.ModelViewSet):  # Класс-контроллер, для создания набора контроллеров на осное VieSet
    queryset = Tags.objects.all()  # Набор данных для работы в контроллерах
    serializer_class = TagSerializer  # класс-сериализатор


from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
