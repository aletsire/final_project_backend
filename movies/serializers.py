from rest_framework import serializers
from django.contrib.auth.models import User

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
    fields =('id', 'title', 'genre_ids', 'backdrop_path', 'poster_path', )


class MovieSerializer(serializers.ModelSerializer):
      
  # # genre_ids = serializers.StringRelatedField(many=True)
  genre_ids = GenreSerializer(many=True)
  # # class ReviewSerializer()
  class Meta:
    model = Movie
    fields ='__all__'

  # dictionary = serializers.DictField(child = serializers.DictField())