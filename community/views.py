from community import serializers
from community.models import Review, Comment
from movies.models import Movie
from community.serializers import ReviewSerializer,  ReviewListSerializer, CommentSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import filters
from django.db.models import Q


class ReviewList(APIView):
    def get(self, request, format=None):
        reviews = Review.objects.all()
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # print('포스트 들어옴')
        permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        serializer = ReviewSerializer(data=request.data)
        # print(serializer)
        # print('시리얼라이저 완료')
        if serializer.is_valid():
            serializer.save(user=request.user, movie=Movie.objects.get(pk=request.data['movie']['id']))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)


class ReviewClap(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def post(self, request, pk):
        review = generics.get_object_or_404(Review, pk = pk)
        if request.user != review.user:     # 리뷰 작성자와 clap보내는 사람이 같지않도록
            if review.claps.filter(pk=request.user.pk).exists():
                review.claps.remove(request.user)
            else:
                review.claps.add(request.user)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    


class CommentList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # def get_object(self, pk):
    #     try:
    #         return Comment.objects.get(pk=pk)
    #     except Comment.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk, format=None):
    #     comment = self.get_object(pk=pk)
    #     serializer = CommentSerializer(comment)
    #     return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = CommentSerializer(data=request.data)
        # print(pk)
        if serializer.is_valid():
            serializer.save(user=request.user, review = Review.objects.get(pk=pk))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        
        # queryset = self.get_queryset()
        # serializer_class = CommentSerializer(queryset)
        print(request.data['id'])
        comment = generics.get_object_or_404(Comment, pk = request.data['id'])
        # print(comment.pk)
        # print(request.user)
        serializer = CommentSerializer(comment, data=request.data)
        if request.user == comment.user:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        # comment = self.get_object(pk=pk)
        comment = generics.get_object_or_404(Comment, pk = request.data['id'])
        print(request.user)
        print(comment)
        if request.user == comment.user:
            print(comment)
            Comment.objects.get(pk=request.data['id']).delete()
            # comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

# class ReviewSearch(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     # print(queryset, serializer_class)
#     filter_backends = [filters.SearchFilter]
#     # print(filter_backends)
#     search_fields = ['title', 'Review__user']
#     # search_fields = ['title', 'movie__ms', 'user__us']


class ReviewSearch(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        print(self.request.GET['search'])
        q_word = self.request.GET['search']
        print(q_word)
        if q_word:

            object_list = Review.objects.filter(
                Q(user__username__icontains=q_word) |
                Q(title__icontains=q_word) |
                Q(movie__title__icontains=q_word) |
                Q(content__icontains=q_word)
            )
        else:
            object_list = Review.objects.all()
        return object_list