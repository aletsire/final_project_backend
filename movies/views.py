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
import random
from django.db.models import Q
from collections import OrderedDict
import itertools




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

    # def post(self, request, format=None):
    #     serializer = MovieSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(owner=request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


    # def put(self, request, pk, format=None):
    #     movie = self.get_object(pk)
    #     # if request.
    #     serializer = MovieSerializer(movie, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     snippet.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# class MovieSearch(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#     # print(queryset, serializer_class)
#     filter_backends = [filters.SearchFilter]
#     # print(filter_backends)
#     search_fields = ['title', 'original_title', 'overview']
    
    
class MovieSearch(generics.ListAPIView):
    # queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_queryset(self):
        print(self.request.GET['search'])
        q_word = self.request.GET['search']
        print(q_word)
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




# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer