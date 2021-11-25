from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.serializers  import UserSerializer

from movies.models import Movie, Genre
import re


class GenreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Genre
    fields = '__all__'



class MovieListSerializer(serializers.ModelSerializer):
   
  # genre_ids = serializers.StringRelatedField(many=True)   
  # genre_ids = GenreSerializer(many=True)
  # class ReviewSerializer()
  class Meta:
    model = Movie
    fields =('id', 'title', 'genre_ids', 'backdrop_path', 'poster_path','backdrop_path_thumbnail', 'poster_path_thumbnail', )


class MovieSerializer(serializers.ModelSerializer):
      
  # # genre_ids = serializers.StringRelatedField(many=True)
  genre_ids = GenreSerializer(many=True)
  # # class ReviewSerializer()
  like_users = UserSerializer(read_only=True, many=True)
  dislike_users = UserSerializer(read_only=True, many=True)
  class Meta:
    model = Movie
    fields ='__all__'

  # dictionary = serializers.DictField(child = serializers.DictField())