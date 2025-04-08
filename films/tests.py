from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from users_reviews.models import Reviews
from .models import Film, Film_details, Genre, Tags


class TaskTests(TestCase):
    def setUp(self):
        self.film = Film.objects.create(title="Test Film", director="Феллини", release_date="1977-04-20")
        self.tags = Tags.objects.create(name="Тег для теста")
        self.film_details = Film_details.objects.create(film=self.film, year='1977-04-20', runtime='90',
                                                        writer='Andersen', actors='Demmi Moor, Angelika Fellini',
                                                        plot='One man told for...', language='italian', country='Italy',
                                                        awards='Oskar for Test', poster='', box_office='10000000')
        self.genre = Genre.objects.create(film=self.film, genre='драма')

        User = get_user_model()
        self.user = User.objects.create_superuser(password='testuser', email="user@inbox.ru")
        self.client.login(password='testuser', email="user@inbox.ru")
        self.reviews = Reviews.objects.create(film=self.film, user=self.user, reviews_body='Очень хороший фильм!!!')

    #path('details/<int:film_id>/', views.film_details, name='film_details'),
    def test_film_details(self):
        url = reverse('film_details', args=[self.film.pk])  # эндпоинт с именем 'search_results'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_view_film(self):  # Тест на просмотр фильма. Работает!
        film = Film.objects.get(id=self.film.id)
        self.assertEqual(film.title, "Test Film")
        self.assertEqual(film.director, "Феллини")
        self.assertEqual(film.release_date.strftime('%Y-%m-%d'), "1977-04-20")

    def test_edit_film(self):  # Тест на редактирование фильма. Работает!
        self.film.title = "Updated Title"
        self.film.save()
        updated_film = Film.objects.get(id=self.film.id)
        self.assertEqual(updated_film.title, "Updated Title")

    def test_delete_film(self):  # Тест на удаление фильма. Работает!
        film_id = self.film.id
        self.film.delete()
        with self.assertRaises(Film.DoesNotExist):
            Film.objects.get(id=film_id)

    def test_add_details_to_film(self):  # Тест на добавление информации к фильму. Работает!
        film_details = Film_details.objects.create(film=self.film, year='1977-04-20', runtime='90',
                                                   writer='Andersen', actors='Demmi Moor, Angelika Fellini',
                                                   plot='One man told for...',
                                                   language='italian', country='Italy', awards='Oskar for Test',
                                                   poster='', box_office='1000')
        self.film.refresh_from_db()
        self.assertIn(film_details.film.title, self.film.title)

    def test_add_tags_to_film_details(self):  # Тест на добавление тега к фильму. Работает!
        self.film_details.tags.add(self.tags)
        self.tags.refresh_from_db()
        self.assertIn(self.tags, self.film_details.tags.all())

    def test_search_results(self):  # Тест на поиск фильма. Работает!
        url = reverse('search_results')  # эндпоинт с именем 'search_results'
        response = self.client.get(url, query_params={'q': 'Test Film'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_films(self):  # Тест на создание фильма. Работает!
        url = reverse('films_list')  # есть эндпоинт с именем 'films_list'
        data = dict(title="Test Film", director="Феллини", release_date="1977-04-20")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rating_create(self): # Тест на создание рейтинга. Работает!
        url = reverse('rating_create', args=[self.film.pk])
        data = dict(film=self.film, user=self.user.pk, rating='1')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_reviews_create(self): # Тест на создание рицензии. Работает!
        url = reverse('reviews_create', args=[self.film.pk])
        data = dict(film=self.film, user='1', reviews_body='Очень, ну очень хороший фильм!!!')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def tearDown(self):  # очистка лишних данных после выполнения тестов
        Film.objects.all().delete()
        Film_details.objects.all().delete()
        Genre.objects.all().delete()
        Tags.objects.all().delete()
        Reviews.objects.all().delete()
