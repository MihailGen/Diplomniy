from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from films.models import Film, Film_details, Genre, Tags
from films.serializers import FilmSerializer, Film_detailsSerializer, GenreSerializer, TagSerializer
from users_reviews.models import Reviews, Ratings


def base(request):
    return render(request, 'films/base.html')


def films(request):
    film_list = Film.objects.all().order_by('-release_date')
    return render(request, 'films/films.html', {'film_list': film_list})


def film_details(request, film_id):
    film = Film_details.objects.get(id=film_id)
    reviews = Reviews.objects.filter(film=film_id)

    try:
        rating = Ratings.objects.get(film_id=film_id, user_id=request.user)
    except:
        rating = 0

    print(rating)
    return render(request, 'films/film_details.html', {'film': film, 'reviews': reviews, 'rating': rating})


def film_list(request):
    #film_list = Film.objects.all().order_by('-release_date')
    film_list = Film_details.objects.all().select_related('film')
    #poster = Film_details.objects.filter('film').values('poster')

    return render(request, 'films/films.html', {'film_list': film_list})


@require_POST
def delete_film(film_id):
    # film = Film.objects.get(id=film_id)
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
