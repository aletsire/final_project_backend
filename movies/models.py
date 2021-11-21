from django.db import models
from django.conf import settings

# Create your models here.

class Genre(models.Model):
    genre_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.pk}: {self.name}'

class Movie(models.Model):
    adult = models.BooleanField(null=True)
    backdrop_path = models.CharField(max_length=255, null=True)
    genre_ids  = models.ManyToManyField(Genre, related_name='movies')
    id = models.IntegerField(primary_key=True)
    original_language = models.CharField(max_length=50, null=True)
    original_title = models.CharField(max_length=255, null=True)
    overview = models.TextField(null=True)
    popularity = models.FloatField(null=True)
    poster_path = models.TextField(null=True)
    release_date = models.DateTimeField(null=True)
    title = models.CharField(max_length=255, null=True)
    video = models.BooleanField(null=True)
    vote_average = models.FloatField(null=True)
    vote_count = models.IntegerField(null=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislike_movies')
    
    def __str__(self):
        return f'{self.pk}: {self.title}'


