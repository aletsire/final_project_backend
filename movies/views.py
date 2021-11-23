from django.db.models import query
from movies import serializers
from movies.models import Movie, Genre
from movies.serializers import MovieSerializer, MovieListSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework import filters
from django.contrib.auth import get_user_model
from bs4 import BeautifulSoup
from django.db.models import Q
from collections import OrderedDict
import itertools
import weather




class MovieList(APIView):

    # def get(self, request, format=None):
    #     movies = Movie.objects.all()
    #     genres = Genre.objects.all()
    #     genre_movie = []
    #     for genre in genres:

    #         tmp = genre.movies.all().values()
    #         print(tmp)
    #         genre_movie.append({genre.genre_id: tmp})

    #     return Response(genre_movie)


    def get(self, request, format=None):
        
        genre_movies=[]
        genres = Genre.objects.all()
        for genre in genres:
            genre_movie_queryset = genre.movies.all()[:10]
            genre_movie_serializer = MovieListSerializer(genre_movie_queryset, many=True)
            genre_movies.append({str(genre):genre_movie_serializer.data})
        return Response(genre_movies)


class MovieRecommend(APIView):
    def get(self, request, format=None):
        weather_json = weather.get_weather()
        weather_id = weather_json['weather'][0]['id']
        #향후 도시 추가할 것
        weather_description = weather_json['weather'][0]['description']
        weather_icon = "http://openweathermap.org/img/wn/" + weather_json['weather'][0]['icon'] +".png"
        weather_data = {"weather_id":weather_id, "weather_description":weather_description, "weather_icon":weather_icon}
        genre_id = weather.get_genre(weather_id)
        movies_queryset = Movie.objects.filter(genre_ids__in=[genre_id]).order_by('vote_average')[:3]
        movies_serializer = MovieSerializer(movies_queryset, many=True)
        weather_data["recommend_movies"]= movies_serializer.data
        return Response(weather_data)
        



class MovieDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)


class MovieLike(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def post(self, request, pk):
        movie = generics.get_object_or_404(Movie, pk = pk)
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
        else:
            if movie.dislike_users.filter(pk=request.user.pk).exists():
                movie.dislike_users.remove(request.user)
            movie.like_users.add(request.user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)


class MovieDislike(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def post(self, request, pk):
        movie = generics.get_object_or_404(Movie, pk = pk)
        if movie.dislike_users.filter(pk=request.user.pk).exists():
            movie.dislike_users.remove(request.user)
        else:
            if movie.like_users.filter(pk=request.user.pk).exists():
                movie.like_users.remove(request.user)
            movie.dislike_users.add(request.user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)


    
    
class MovieSearch(generics.ListAPIView):
    # queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_queryset(self):
        q_word = self.request.GET['search']
        if q_word:

            object_list = Movie.objects.filter(
                Q(title__icontains=q_word) |
                Q(genre_ids__name__icontains=q_word) |
                Q(original_title__icontains=q_word) |
                Q(overview__icontains=q_word)
            )
        else:
            object_list = Movie.objects.all()
        return object_list


