# Generated by Django 5.1.2 on 2025-03-27 20:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название фильма')),
                ('director', models.CharField(max_length=100, verbose_name='Директор фильма')),
                ('release_date', models.DateField(blank=True, null=True, verbose_name='Дата выхода на экран')),
            ],
            options={
                'verbose_name': 'Фильм',
                'verbose_name_plural': 'Фильмы',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название тега')),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'теги',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(choices=[('драма', 'Драма'), ('комедия', 'Комедия'), ('мелодрама', 'Мелодрама'), ('исторический', 'Исторический'), ('детектив', 'Детектив'), ('криминал', 'Криминал'), ('боевик', 'Боевик'), ('ужасы', 'Ужасы'), ('мюзикл', 'Мюзикл'), ('художественный', 'Художественный'), ('экшн', 'Экшн')], default='Художественный', max_length=200)),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Жанры', to='films.film')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='Film_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.DateField(blank=True, null=True, verbose_name='Год выхода на экран')),
                ('runtime', models.IntegerField(blank=True, null=True, verbose_name='Длительность (мин.)')),
                ('writer', models.CharField(max_length=100, verbose_name='Сценарист')),
                ('actors', models.CharField(max_length=100, verbose_name='Актёры')),
                ('plot', models.TextField(verbose_name='Сюжет')),
                ('language', models.CharField(max_length=100, verbose_name='Язык')),
                ('country', models.CharField(max_length=100, verbose_name='Страна')),
                ('awards', models.CharField(max_length=100, verbose_name='Призы и награды')),
                ('poster', models.CharField(max_length=100, verbose_name='Ссылка на картинку')),
                ('box_office', models.IntegerField(verbose_name='Бюджет')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Информация', to='films.film')),
                ('tags', models.ManyToManyField(related_name='Film_details', to='films.tags')),
            ],
            options={
                'verbose_name': 'информация о фильме',
                'verbose_name_plural': 'информация о фильмах',
            },
        ),
    ]
