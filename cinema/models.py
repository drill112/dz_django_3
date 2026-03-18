from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    release_year = models.PositiveIntegerField(verbose_name='Год выпуска')
    duration = models.PositiveIntegerField(verbose_name='Длительность (мин)')
    genre = models.CharField(max_length=100, verbose_name='Жанр')
    poster = models.CharField(max_length=255, verbose_name='Постер')

    def __str__(self):
        return self.title


class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='sessions', verbose_name='Фильм')
    date_time = models.DateTimeField(verbose_name='Дата и время')
    hall_number = models.PositiveIntegerField(verbose_name='Номер зала')

    def __str__(self):
        return f"{self.movie.title} - {self.date_time}"


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews', verbose_name='Фильм')
    user_name = models.CharField(max_length=100, verbose_name='Имя пользователя')
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.PositiveIntegerField(verbose_name='Оценка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return f"{self.user_name} - {self.movie.title}"