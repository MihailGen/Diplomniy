from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from rest_framework.permissions import IsAuthenticated

from films.models import Film


class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, username, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.username = username
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, username=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        # print(email)
        return self._create_user(email, password, username, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=120, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


# модель "Рецензия"
class Reviews(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='Рецензия')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Рецензия')
    reviews_body = models.TextField(null=True, blank=True, verbose_name='Рецензия')
    permission_classes = [IsAuthenticated]

    class Meta:
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'

    def __str__(self):
        return f'Рецензия на фильм: {self.film}'


# модель "Рейтинг"
class Ratings(models.Model):
    RATING_CHOICES = [(1, "Неудовлетворительно"), (2, "Почти удовлетворительно"), (3, "Удовлетворительно"),
                      (4, "Весьма удовлетворительно"), (5, "Хорошо"), (6, "Весьма хорошо"), (7, "Очень хорошо"),
                      (8, "Почти отлично"), (9, "Отлично"), (10, "Превосходно")]
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='Рейтинг')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Рейтинг')
    rating = models.IntegerField(choices=RATING_CHOICES)
    permission_classes = [IsAuthenticated]

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинг'

    def __str__(self):
        return f'Рейтинг фильма "{self.film}": - {self.rating}'


# модель "Рейтинг"
class Favourites(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='Избранное')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Избранное')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return f'Избранное для {self.user}: - {self.film}'
