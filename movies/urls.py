from django.urls import path
from . import views


urlpatterns = [
    path('movielist/', views.MovieList.as_view()),
    path('movielist/<int:pk>/', views.MovieDetail.as_view()),
    path('movielist/<int:pk>/like/', views.MovieLike.as_view()),
    path('movielist/<int:pk>/dislike/', views.MovieDislike.as_view()),
    path('movielist/search/', views.MovieSearch.as_view()),
]



# from django.urls import path
# from snippets import views

# urlpatterns = [
#     # path('snippets/', views.snippet_list),
#     # path('snippets/<int:pk>/', views.snippet_detail),
#     path('snippets/', views.SnippetList.as_view()),
#     path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
#     path('users/', views.UserList.as_view()),
#     path('users/<int:pk>/', views.UserDetail.as_view()),
# ]