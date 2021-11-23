from django.urls import path
from . import views


urlpatterns = [
    path('movielist/', views.MovieList.as_view()),
    path('movielist/recommend/', views.MovieRecommend.as_view()),
    path('movielist/<int:pk>/', views.MovieDetail.as_view()),
    path('movielist/<int:pk>/like/', views.MovieLike.as_view()),
    path('movielist/<int:pk>/dislike/', views.MovieDislike.as_view()),
    path('movielist/search/', views.MovieSearch.as_view()),
]


